import streamlit as st
import requests
import os
from typing import Optional

# Set page title and icon
#st.set_page_config(page_title="AI Chatbot", page_icon="🎱")
st.title('SurbaseAI')

# API endpoints
API_ENDPOINTS = {
    "OpenAI ChatGPT": "https://api.openai.com/v1/chat/completions",
    "Anthropic Claude": "https://api.anthropic.com/v1/messages",
    "DeepSeek": "https://api.deepseek.com/v1/chat/completions"
}

# Model names
MODEL_NAMES = {
    "OpenAI ChatGPT": "gpt-3.5-turbo",
    "Anthropic Claude": "claude-3-opus-20240229",
    "DeepSeek": "deepseek-chat"
}


def get_openai_response(api_key: str, prompt: str, model: str, temperature: float = 0.7) -> Optional[str]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }

    try:
        response = requests.post(API_ENDPOINTS["OpenAI ChatGPT"], json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"OpenAI API Error: {str(e)}")
        return None

def get_claude_response(api_key: str, prompt: str, model: str, temperature: float = 0.7) -> Optional[str]:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": temperature
    }

    try:
        response = requests.post(API_ENDPOINTS["Anthropic Claude"], json=data, headers=headers)
        response.raise_for_status()
        return response.json()['content'][0]['text']
    except Exception as e:
        st.error(f"Claude API Error: {str(e)}")
        return None

def get_deepseek_response(api_key: str, prompt: str, model: str, temperature: float = 0.7) -> Optional[str]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }

    try:
        response = requests.post(API_ENDPOINTS["DeepSeek"], json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Deepseek API Error: {str(e)}")
        return None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

# sidebar for API configuration
with st.sidebar:
    st.header("Configuration")
    api_provider = st.selectbox("Choose AI Provider", list(API_ENDPOINTS.keys()))
    api_key = st.text_input(f"Enter {api_provider} API Key", type="password")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, help="Controls randomness: 0 = deterministic, 1 = creative")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar")
            st.stop()

        response = None
        with st.spinner("Thinking..."):
            if api_provider == "OpenAI ChatGPT":
                response = get_openai_response(api_key, prompt, MODEL_NAMES[api_provider], temperature)
            elif api_provider == "Anthropic Claude":
                response = get_claude_response(api_key, prompt, MODEL_NAMES[api_provider], temperature)
            elif api_provider == "DeepSeek":
                response = get_deepseek_response(api_key, prompt, MODEL_NAMES[api_provider], temperature)

        if response:
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error("Failed to get response from API")

