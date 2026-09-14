# pip install streamlit google-generativeai python-dotenv
# python -m venv venv
# \venv\Scripts\activate
# .env [environ]
# https://ai.google.dev/gemini-api/docs/get-started/python

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)



# Configure Gemini API
genai.configure(api_key=os.getenv("Api_key"))

# Model configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="""give a system instruction suitable for a forensic expert. 
                        your task is to engage in a conversation about development of 
                        a forensic system for cybercrime identification and prevention. 
                        then answer questions. use analogy and examples that are relevant.
                        use humor and make the conversation tailored to the objective of 
                        the model. ask questions so you can understand the user and improve 
                        on your findings. generate effective report. correlate logs of 
                        dataset if presented or asked to.""",
)

# Streamlit UI
# st.set_page_config(page_title="Science Tutor for Kids", page_icon="🔬")
st.title("🔬 SurbaseAI Bot")
st.subheader("Ask me anything about ....!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial bot greeting
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your science tutor. What would you like to learn about today?"
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your science question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Convert messages to Gemini history format
            history = []
            for msg in st.session_state.messages[:-1]:  # Exclude the current message
                if msg["role"] == "user":
                    history.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    history.append({"role": "model", "parts": [msg["content"]]})
            
            # Start chat session with history
            chat_session = model.start_chat(history=history)
            
            # Send message and get response
            response = chat_session.send_message(prompt)
            model_response = response.text
            
            # Display response
            st.markdown(model_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": model_response})

# Sidebar with additional information
with st.sidebar:
    st.header("About this tutor")
    st.markdown("""
    This SurbaseAI tutor is designed to:
    - Explain Forensic science concepts in simple terms
    - Use fun analogies and examples
    - Make learning enjoyable with humor
    - Suggest real-world observations and experiments
    - Ask questions to enhance your learning experience
    """)
    
    st.divider()
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Chat cleared! Let's start fresh. What would you like to learn?"
        })
        st.rerun()