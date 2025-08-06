from flask import Flask, request, Response, stream_with_context, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# No CORS needed for server-to-server communication

# Validate API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY must be set in .env file")

os.environ["GOOGLE_API_KEY"] = api_key

# Initialize chat models
chat_models = {
    "gemini-2.0-flash": ChatGoogleGenerativeAI(model="gemini-2.0-flash", streaming=True),
    "gemini-1.5-pro": ChatGoogleGenerativeAI(model="gemini-1.5-pro", streaming=True),
    "gemini-1.5-flash": ChatGoogleGenerativeAI(model="gemini-1.5-flash", streaming=True)
}

# College advisor system prompt
SYSTEM_PROMPT = """You are AskMav, a knowledgeable and friendly virtual college advisor. Your role is to help students with:

1. College selection and research
2. Admission requirements and processes
3. Academic program information
4. Scholarship and financial aid guidance
5. Career planning and major selection
6. Application essay assistance
7. Study abroad opportunities
8. Campus life questions

Guidelines:
- Be encouraging and supportive
- Provide accurate, up-to-date information
- Ask clarifying questions when needed
- Offer multiple perspectives and options
- Be concise but thorough
- Use a friendly, professional tone
- Include specific examples when helpful

Always prioritize the student's individual needs and circumstances in your advice."""

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "available_models": list(chat_models.keys())
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint with streaming response"""
    try:
        data = request.json
        user_message = data.get("message")
        model_name = data.get("model", "gemini-2.0-flash")
        include_context = data.get("include_context", True)
        
        # Validate input
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        if model_name not in chat_models:
            return jsonify({"error": f"Model {model_name} not available"}), 400
        
        logger.info(f"Chat request - Model: {model_name}, Message length: {len(user_message)}")
        
        # Prepare messages
        messages = []
        if include_context:
            messages.append(SystemMessage(content=SYSTEM_PROMPT))
        messages.append(HumanMessage(content=user_message))
        
        # Get the appropriate model
        chat_model = chat_models[model_name]
        
        def stream_response():
            """Generator function for streaming response"""
            try:
                full_response = ""
                for chunk in chat_model.stream(messages):
                    if chunk.content:
                        full_response += chunk.content
                        yield chunk.content
                
                # Log the full response for monitoring
                logger.info(f"Response generated - Length: {len(full_response)} characters")
                
            except Exception as e:
                logger.error(f"Error during streaming: {str(e)}")
                yield f"Error: {str(e)}"
        
        return Response(
            stream_with_context(stream_response()),
            content_type='text/plain',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            }
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify({
        "available_models": list(chat_models.keys()),
        "default_model": "gemini-2.0-flash"
    })

@app.route('/college-info/<string:topic>', methods=['GET'])
def get_college_info(topic):
    """Get specific college information topics"""
    college_info = {
        "admission-requirements": {
            "title": "General Admission Requirements",
            "content": [
                "High school diploma or equivalent",
                "Standardized test scores (SAT/ACT)",
                "Letters of recommendation",
                "Personal statement/essay",
                "Extracurricular activities",
                "GPA requirements (varies by institution)"
            ]
        },
        "financial-aid": {
            "title": "Financial Aid Options",
            "content": [
                "Federal Pell Grants",
                "State grants and scholarships",
                "Merit-based scholarships",
                "Need-based financial aid",
                "Work-study programs",
                "Student loans (federal and private)"
            ]
        },
        "application-timeline": {
            "title": "College Application Timeline",
            "content": [
                "Junior Year: Start college research, take standardized tests",
                "Summer before Senior Year: Visit colleges, work on essays",
                "Early Senior Year: Submit early applications (Nov 1-15)",
                "Winter Senior Year: Submit regular applications (Jan 1-15)",
                "Spring Senior Year: Receive decisions, make final choice"
            ]
        }
    }
    
    if topic in college_info:
        return jsonify(college_info[topic])
    else:
        return jsonify({"error": "Topic not found"}), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting AskMav backend on port {port}")
    logger.info(f"Available models: {list(chat_models.keys())}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )