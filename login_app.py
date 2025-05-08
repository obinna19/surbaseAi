import streamlit as st
import sqlite3
from PIL import Image
import base64
import os
import subprocess
import main

#image_path = "C:\Users\Martin Amilo\c\gui\project\image\jpg\scenery.jpg"

st.set_page_config(
    page_title='Login Page',
     page_icon='©', 
     layout="wide"
)

# Database function ---
def init_db():
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT UNIQUE NOT NULL,
              password TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL
        )    
    """)
    conn.commit()
    # Insert a sample user
    try:
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ("admin", "password123", "martinamilo@gmail.com"))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # user already exists
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', 
              (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None 

# Background Image setup
def set_bg_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    bg_css = f'''
    <style>
    .stApp{{
        background-image: url(data:image/jpg;base64,{encoded_string});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    
    }}
    </style>

    
    '''
    st.markdown(bg_css, unsafe_allow_html=True)

# Main Application
def main():
    # initialize db
    init_db()

    # set background image (replace with ur image path)
    set_bg_image("scenery.jpg")

    # custom CSS for styling
    st.markdown("""
    <style>
    .login-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 0 0 10px rgba(0,0,0,0.1);
        margin: 2rem auto;
        max-width: 400px;    
    }     
    .stTextInput>div>div>input, .stTextInput>div>div>input:focus {
        background-color: rgba(255, 255, 255, 0.9);            
    }
    </style>

    """, unsafe_allow_html=True)

    # check authentication status
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated: 
        # login form
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; color: #333;'>Login</h1>", 
                        unsafe_allow_html=True)

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

                if submit: 
                    if authenticate(username, password):
                        st.session_state.authenticated = True
                        st.session_state['username'] = username

                        try:
                            subprocess.Popen(['streamlit', 'run', 'main.py'])
                            st.success("Login successful! Main application launching..")
                        except Exception as e:
                            st.error(f"Error launching main app: {e}")

                        st.rerun()
                    else:
                        st.error("Invalid username or password")

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.success("Already authenticated. Main app should be running.")
        # display after successful login
        #st.markdown("<h1 style='text-align: center; color: white;'>Welcome!</h1>", 
                    #unsafe_allow_html=True)
        #st.markdown("<div style='text-align: center; color: white;'> Youhave succeefully logged in</div>", 
                    #unsafe_allow_html=True)
        

    

if __name__ == "__main__":
    main()
     
    
