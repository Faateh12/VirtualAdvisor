from flask import Flask, request, Response, stream_with_context
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", streaming=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    message = HumanMessage(content=user_message)

    def stream_response():
        for chunk in chat_model.stream([message]):
            if chunk.content:
                yield chunk.content

    return Response(stream_with_context(stream_response()), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
