import streamlit as st
import json
import datetime
from pathlib import Path
from streamlit_autorefresh import st_autorefresh


# set page configuration
#st.set_page_config(page_title="Group Chat", layout="wide")

# Auto-refresh every 2 secs
st_autorefresh(interval=2000, key="chat_refresh")

# file Path
MESSAGES_FILE = Path("maessages.json")

def load_messages():
    """Load messages fro JSON FIle"""
    if not MESSAGES_FILE.exists():
        return []
    try:
        return json.loads(MESSAGES_FILE.read_text())
    except json.JSONDecodeError:
        return []


def save_message(username, message):
    """Save a new message to the JSON File"""
    messages = load_messages()
    messages.append({
        "username": username,
        "message": message,
        "timestamp": datetime.datetime.now().isoformat()


    })
    MESSAGES_FILE.write_text(json.dumps(messages, indent=2))

# user authentication
if "username" not in st.session_state:
    with st.form("username_form"):
        username = st.text_input("Choose a username:")
        if st.form_submit_button("Join Chat"):
            if username.strip():
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Please enter a valid username")
    st.stop()

# Main chat interface
st.title(f"Group Chat - {st.session_state.username}")

# Display messages
messages = load_messages()
for msg in messages:
    timestamp = datetime.datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    with st.chat_message(msg["username"]):
        st.write(f"**{msg['username']}** ({timestamp})")
        st.write(msg['message'])

# Message input
with st.form("message_form", clear_on_submit=True):
    message = st.text_input("Type your message:", key="message_input")
    if st.form_submit_button("Send"):
        if message.strip():
            save_message(st.session_state.username, message.strip())
            st.rerun()
        else:
            st.error("Message cannot be empty")


