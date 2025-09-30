import streamlit as st
import os
from dotenv import load_dotenv
from autogen import AssistantAgent

# Load environment variables
load_dotenv()

# LLM configuration for Gemini
llm_config_gemini = {
    "config_list": [
        {
            "model": "gemini-2.0-flash",
            "api_type": "google",
            "api_key": os.getenv("GOOGLE_API_KEY"),
        }
    ]
}

# Initialize assistant
assistant = AssistantAgent("assistant", llm_config=llm_config_gemini)

# Streamlit page setup
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.sidebar.title("🤖 AI Chatbot")
st.sidebar.info("Ask anything and get responses in real-time from Gemini 2.0!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

chat_container = st.container()

# User input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", "")
    submit_button = st.form_submit_button(label="Send")

# Handle new user message
if submit_button and user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Generate assistant reply based on full conversation history
        response = assistant.generate_reply(messages=st.session_state.messages)

        # Extract only the assistant's text
        if isinstance(response, dict):
            assistant_text = response.get("content", "")
        else:
            assistant_text = str(response)

        # Remove TERMINATE markers if present
        assistant_text = assistant_text.replace("TERMINATE", "").strip()

    except Exception as e:
        assistant_text = f"Error: {e}"

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})

# Display chat history
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='text-align: right; background-color:#DCF8C6; padding:10px; "
                f"border-radius:10px; margin:5px 0'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='text-align: left; background-color:#F1F0F0; padding:10px; "
                f"border-radius:10px; margin:5px 0'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )
