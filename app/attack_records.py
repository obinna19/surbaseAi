import streamlit as st
import pandas as pd
import os
from datetime import datetime


# Define dropdown options
attack_type_options = [
    "Brute Force", "Cross-Site Scripting", "DDoS", "Malware",
    "Phishing", "Ransomware", "SQL Injection", "Zero-Day Exploit"
]

user_role_options = [
    "Employee", "Admin", "External User", "Contractor"
]

security_tools_options = [
    "Firewall", "Endpoint Detection", "MFA", "VPN",
    "Antivirus", "WAF", "SIEM", "IDS"
]

target_system_options = [
    "API", "Cloud Service", "Database", "Email Server",
    "IoT Device", "Network Switch", "User Account", "Web Server"
]

mitigation_method_options = [
    "Containment", "Reset Credentials", "Quarantine",
    "Patch", "Block IP"
]

month_options = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Create form
with st.form("attack_record_form", clear_on_submit=True):
    st.header("Cyber Attack Record Form")
    
    col1, col2 = st.columns(2)
    
    with col1:
        attack_type = st.selectbox("Attack Type*", attack_type_options)
        user_role = st.selectbox("User Role*", user_role_options)
        location = st.text_input("Location*")
        attack_ip = st.text_input("Attack IP Address*")
        target_ip = st.text_input("Target IP Address*")
        outcome = st.selectbox("Outcome*", ["Success", "Failure"])
        data_compromised = st.number_input("Data Compromised (GB)*", min_value=0.0, format="%.2f")
        attack_duration = st.number_input("Attack Duration (minutes)*", min_value=0)
        
    with col2:
        security_tools = st.multiselect("Security Tools Used*", security_tools_options)
        target_system = st.selectbox("Target System*", target_system_options)
        attack_severity = st.text_input("Attack Severity*")
        timestamp = st.text_input("Timestamp*", datetime.now())
        industry = st.text_input("Industry*")
        response_time = st.number_input("Response Time (minutes)*", min_value=0)
        mitigation_method = st.selectbox("Mitigation Method*", mitigation_method_options)
        month = st.selectbox("Month*", month_options)
        year = st.number_input("Year*", min_value=2000, max_value=2100, value=datetime.now().year)
        time = st.time_input("Time*", datetime.now().time())
    
    submitted = st.form_submit_button("Submit Record")
submitted
# Handle form submission
if submitted:
    # Basic validation for required text fields
    required_fields = {
        "Location": location,
        "Attack IP": attack_ip,
        "Target IP": target_ip,
        "Attack Severity": attack_severity,
        "Industry": industry,
    }
    
    missing_fields = [field for field, value in required_fields.items() if not value.strip()]
    
    if missing_fields:
        st.error(f"Missing required fields: {', '.join(missing_fields)}")
    else:
        # Prepare data for CSV
        new_record = {
            "attack_type": attack_type,
            "user_role": user_role,
            "location": location.strip(),
            "attack_ip": attack_ip.strip(),
            "target_ip": target_ip.strip(),
            "outcome": outcome,
            "data_compromised_GB": data_compromised,
            "attack_duration_min": attack_duration,
            "Security_tools_used": ", ".join(security_tools),
            "target_system": target_system,
            "attack_severity": attack_severity.strip(),
            "timestamp": timestamp,
            "industry": industry.strip(),
            "response_time_min": response_time,
            "mitigation_method": mitigation_method,
            "month": month,
            "year": year,
            "time": str(time),
        }
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame([new_record])
        
        if os.path.exists("./app/attack_records.csv"):
            df.to_csv("attack_records.csv", mode='a', header=False, index=False)
        else:
            df.to_csv("attack_records.csv", index=False)
        
        st.success("Record saved successfully! ✅")

# Display existing records
st.subheader("Saved Records")
if os.path.exists("./app/attack_records.csv"):
    records_df = pd.read_csv("./app/attack_records.csv")
    st.dataframe(records_df)
else:
    st.info("No records found. Submit a record to create the database.")