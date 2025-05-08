import pandas as pd
import streamlit as st
import os
import subprocess
import webbrowser
from login_app import *


#st.title("Cybercrime Report Monitor🎡")
st.set_page_config(
    page_title= 'SurbaseAi',
    page_icon= '©',
    layout= "wide"
)
#st.logo()
about_page = st.Page(
    "./app/about.py", 
    title="About Page", 
    icon="😎",
    default=True,
)

complaint_page = st.Page(
    "./app/dashboard.py", 
    title="Dashboard", 
    icon="🦺",
)
security_page = st.Page(
    "./app/security_dashboard.py", 
    title="Security Summary", 
    icon="🚔",
    
)
ip_geolocation = st.Page(
    "./app/ip_geolocation.py", 
    title="IP Address Geolocation", 
    icon="🌍",
    
)
form_page = st.Page(
    "./app/network_form.py", 
    title="Network Report Form", 
    icon="📞",
    
)
messenger_page = st.Page(
    "./app/chat_app.py", 
    title="Messenger Chat", 
    icon="📮",
    
)
AI_page = st.Page(
    "./app/chatbot.py", 
    title="AI Assistant", 
    icon="🎯",
    
)
CS_page = st.Page(
    "./app/cybersecurity_apps.py", 
    title="CSI Forensics", 
    icon="🥼",
    
)
loc_page = st.Page(
    "./app/location_finder.py", 
    title="Trace Location / IP", 
    icon="🗺",
    
)
Rec_page = st.Page(
    "./app/attack_records.py", 
    title="Cyber Attack Records", 
    icon="📝",
    
)


# Navigation
#selected_page = st.navigation([about_page, complaint_page, security_page, ip_geolocation, form_page, chatbot_page ])

selected_page = st.navigation(
    {
        "UI/UX Info": [about_page, Rec_page],
        "Forensic Analysis": [complaint_page, security_page, ip_geolocation, form_page],
        "Inference Tools": [messenger_page, AI_page, CS_page, loc_page]
    }
    
)

if st.sidebar.button("logout"):

    st.session_state.authenticated = False
    try: 
        st.switch_page("login_app.py")
        st.rerun()
    except:
        pass
     

        
# ------ SHARED ON ALL PAGES ------
st.logo("image/jpg/logo.png")
st.sidebar.text("Made with ❤ by Martin")

selected_page.run()
