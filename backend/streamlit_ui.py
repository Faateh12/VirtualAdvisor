import streamlit as st
import requests

st.set_page_config(page_title="AskMav", layout="centered")
st.markdown(
    """
    <h1 style="text-align: center;">AskMav</h1>
    """,
    unsafe_allow_html=True
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Gemini is thinking..."):
        response = requests.post(
            "http://localhost:5001/chat",
            json={"message": user_input},
            stream=True
        )

        collected = ""
        message_placeholder = st.empty()
        for chunk in response.iter_content(chunk_size=64):
            if chunk:
                decoded = chunk.decode("utf-8")
                collected += decoded
                message_placeholder.markdown(collected + "▌")  # Update during streaming

        # Append the final response to chat history after streaming is complete
        st.session_state.chat_history.append(("assistant", collected))
        message_placeholder.markdown("")  # Clear the placeholder

# Show chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)
