# TCP Chat Room {Client-Server Architecture}
import streamlit as st
import socket
import threading




def top_chat():
    st.title("TCP Chat Room")

    role = st.radio("Choose role:", ("Server", "Client"))
    host = st.text_input("IP Address", "127.0.0.1")
    port = st.number_input("Port", 12345)

    if role == "Server":
        if st.form_submit_button("Start Server"):
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, port))
            server.listen()
            st.success(f"Server listening on {host}:{port}")

            client, addr = server.accept()
            st.write(f"Connected to {addr}")

            def receive():
                while True:
                    msg = client.recv(1024).decode()
                    st.text(f"Client: {msg}")

            threading.Thread(target=receive).start()

            msg = st.text_input("Your message:")
            if msg:
                client.send(msg.encode())
    else:
        if st.form_submit_button("Connect"):
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            st.success("Connected!")

            msg = st.text_input("Your message:")
            if msg:
                client.send(msg.encode())

            def receive():
                while True:
                    msg = client.recv(1024).decode()
                    st.text(f"Server: {msg}")

            threading.Thread(target=receive).start()

# DDoS simulation tool
def ddos_simulator():
    st.title("DDos Simulator (Educational)")
    target_ip = st.text_input("Target IP", "127.0.0.1")
    target_port = st.number_input("Target Port", 80)
    num_requests = st.number_input("Number of Requests", 100)

    if st.form_submit_button("Simulator"):
        import random
        from threading import Thread

        def attack():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((target_ip, target_port))
                s.send(random._urandom(1024))
            except Exception as e:
                pass

        for _ in range(num_requests):
            Thread(target=attack).start()

        st.warning(f"Sent {num_requests} dummy packets to {target_ip}:{target_port}")


# Port Scanner
def port_scanner():
    st.title("Port Scanner")
    target = st.text_input("Target IP", "127.0.0.1")
    start_port = st.number_input("Start Port", 1)
    end_port = st.number_input("End Port", 100)

    if st.form_submit_button("Scan"):
        open_ports = []

        def scan_port(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                s.connect((target, port))
                open_ports.append(port)
                s.close()
            except:
                pass

        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(scan_port, range(start_port, end_port+1))

        st.write("Open ports:", open_ports)

# Email Client
def email_client():
    st.title("Secure Email Client")
    smtp_server = st.text_input("SMTP Server", "smtp.gmail.com")
    port = st.number_input("Port", 587)
    sender = st.text_input("Your Email")
    password = st.text_input("Password", type="password")
    receiver = st.text_input("Recipient")
    subject = st.text_input("Subject")
    body = st.text_area("Body")

    if st.form_submit_button("Send"):
        import smtplib
        from email.message import EmailMessage

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        msg.set_content(body)

        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
                st.success("Email sent!")
        except Exception as e:
            st.error(f"Error: {e}")

# IDS/IPS with Suricata
def suricata_ids():
    st.title("IDS/IPS Monitor")
    st.write("Suricata Integration Demo")

    if st.form_submit_button("Start Suricata"):
        import subprocess
        result = subprocess.run(["suricata", "-c", "/etc/suricata/suricata.yaml", "-i", "eth0"],
                            capture_output=True, text=True)
        st.text(result.stdout)

    uploaded_file = st.file_uploader("Upload PCAP file")
    if uploaded_file:
        with open("temp.pcap", "wb") as f:
            f.write(uploaded_file.getbuffer())
        result = subprocess.run(["suricata", "-r", "temp.pcap"],
                                capture_output=True, text=True)
        st.text_area("Analysis Results", result.stdout)

# Main App

#def main():
with st.form("cyber"):
    st.sidebar.title("Inference Engine")
    app = st.sidebar.radio("Choose App:",
                            ["TCP Chat Room", 
                             "DDoS Simulator", 
                             "Port Scanner",
                            "Email Client", 
                            "Suricata IDS/IPS"] )

    try:
        if app == "TCP Chat Room":
            top_chat()
        elif app == "DDoS Simulator":
            ddos_simulator()
        elif app == "Port Scanner":
            port_scanner()
        elif app == "Email Client":
            email_client()
        elif app == "Suricata IDS/IPS":
            suricata_ids()
    except Exception as e:
            app.rerun()

if __name__ == "__main__": 
    app.run()

