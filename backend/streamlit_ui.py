import streamlit as st
import requests
import time
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AskMav - Virtual College Advisor",
    page_icon="team-logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f4e79, #2d5aa0);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 10px 10px;
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: #fafafa;
    }
    
    .user-message {
        background: #e3f2fd;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background: #f3e5f5;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }
    
    .sidebar .block-container {
        padding-top: 2rem;
    }
    
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for additional features
with st.sidebar:
    st.markdown("""
    <h2>
        <img src="static/team-logo.png" alt="AskMav Logo" width="30" style="margin-right: 10px; vertical-align: middle;">
        AskMav Settings
    </h2>
    """, unsafe_allow_html=True)    
    # Model selection
    model_option = st.selectbox(
        "Choose AI Model:",
        ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
        index=0
    )
    
    # Chat settings
    st.subheader("Chat Settings")
    max_history = st.slider("Max Chat History", 10, 100, 50)
    
    # Quick prompts
    st.subheader("Quick Prompts")
    quick_prompts = [
        "What are the admission requirements for engineering programs?",
        "Help me choose between computer science and data science.",
        "What scholarships are available for first-generation college students?",
        "Explain the difference between liberal arts and technical colleges.",
        "What should I include in my college application essay?"
    ]
    
    selected_prompt = st.selectbox("Choose a quick prompt:", [""] + quick_prompts)
    
    # Export chat history
    if st.button("📥 Export Chat History"):
        if st.session_state.get("chat_history"):
            chat_data = {
                "timestamp": datetime.now().isoformat(),
                "chat_history": st.session_state.chat_history
            }
            st.download_button(
                "Download Chat History",
                json.dumps(chat_data, indent=2),
                file_name=f"askmav_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Clear chat
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main content area
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Header with logo placeholder
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <img src="static/team-logo.png" alt="AskMav Logo" width="100">
            <h1>AskMav</h1>
        </div>
        <p>Your Virtual College Advisor</p>
    </div>
    """, unsafe_allow_html=True)
    
    # To add your PNG logo, replace the emoji with:
    # st.image("path/to/your/logo.png", width=100)
    
    # Or use this method if you want to embed it in the HTML:
    # <img src="data:image/png;base64,{base64_encoded_logo}" width="100">

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

# Chat interface
with col2:
    # Display chat history in a container
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for role, msg, timestamp in st.session_state.chat_history:
            if role == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(msg)
                    st.caption(f"Sent at {timestamp}")
            else:
                with st.chat_message("assistant", avatar="team-logo.png"):
                    st.write(msg)
                    st.caption(f"Responded at {timestamp}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Welcome to AskMav! Ask me anything about college admissions, programs, scholarships, or academic planning.")

# Input handling
user_input = selected_prompt if selected_prompt else st.chat_input("Ask me anything about college...")

if user_input:
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input, current_time))
    
    # Show typing indicator
    with st.chat_message("assistant", avatar="team-logo.png"):
        with st.spinner("AskMav is thinking... 🤔"):
            try:
                # Make API request
                response = requests.post(
                    "http://localhost:5001/chat",
                    json={"message": user_input, "model": model_option},
                    stream=True,
                    timeout=30
                )
                
                if response.status_code == 200:
                    collected = ""
                    message_placeholder = st.empty()
                    
                    # Stream the response
                    for chunk in response.iter_content(chunk_size=64):
                        if chunk:
                            decoded = chunk.decode("utf-8")
                            collected += decoded
                            message_placeholder.markdown(collected + "▌")
                    
                    # Final response
                    message_placeholder.markdown(collected)
                    response_time = datetime.now().strftime("%H:%M:%S")
                    
                    # Add to history
                    st.session_state.chat_history.append(("assistant", collected, response_time))
                    
                    # Limit chat history
                    if len(st.session_state.chat_history) > max_history * 2:
                        st.session_state.chat_history = st.session_state.chat_history[-max_history*2:]
                
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
                st.info("Make sure your Flask backend is running on http://localhost:5001")
            
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

# Footer
with col2:
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>AskMav - Your Virtual College Advisor | Powered by Google Gemini</p>",
        unsafe_allow_html=True
    )

# Analytics (optional)
if st.session_state.chat_history:
    total_messages = len(st.session_state.chat_history)
    with st.sidebar:
        st.markdown("---")
        st.metric("Total Messages", total_messages)
        st.metric("User Messages", len([m for m in st.session_state.chat_history if m[0] == "user"]))