import streamlit as st
import pandas as pd
from datetime import datetime
import os

def validate_ip(ip):
    # Basic ip validation (IPv4)
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False

def save_to_excel(data):
    file_path = './app/network_data.xlsx'
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        new_df = pd.DataFrame([data])
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_excel(file_path, index=False)

# Streamlit app configuration
#st.set_page_config(page_title="Network Information Form", layout="wide")

# Main form
with st.form("network_info_form"):
    st.header("Network Information Entry Form")

    # Form fields
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("Location*", max_chars=50)
        target_ip = st.text_input("Target IP*", placeholder="192.168.1.1")
        date = st.date_input("Date*", datetime.now())

    with col2:
        source_ip = st.text_input("Source IP*", placeholder="10.0.0.1")
        description = st.text_area("Description", height=100)
        time = st.time_input("Time*", datetime.now())


    # Mandatory fields check
    mandatory_fields = [location, target_ip, source_ip]
    mandatory_labels = ["Location", "Target IP", "Source IP"]

    # Form submission
    submitted = st.form_submit_button("Submit Entry")

    if submitted:
        errors = []

        # Validate mandatory fields
        for field, label in zip(mandatory_fields, mandatory_labels):
            if not field.strip():
                errors.append(f"{label} is required")

        # validate IP addresses
        if not validate_ip(target_ip):
            errors.append("Invalid Target IP address format")
        if not validate_ip(source_ip):
            errors.append("Invalid Source IP address format")

        if errors:
            for error in errors:
                st.error(error)
        else:
            # Create data dictionary
            timestamp = f"{date} {time}"
            entry_data = {
                "Timestamp": timestamp,
                "Location": location.strip(),
                "Target IP": target_ip.strip(),
                "Source IP": source_ip.strip(),
                "Description": description.strip()
            }

            # Save to excel
            save_to_excel(entry_data)
            st.success("Entry successfully saved!")
            st.balloons()

# Display existing data
if st.checkbox("Show existing entries"):
    try:
        existing_data = pd.read_excel('./app/network_data.xlsx')
        st.dataframe(existing_data)
    except FileNotFoundError:
        st.warning("No Data file found. Submit an entry to create a new file.")

# Instructions
st.sidebar.markdown("""
**Instrutions:**
1. Fill in all mandatory fields (marked with *)
2. Ensure IP addresses are in valid IPv4 format
3. Click 'Submit Entry' to save
4. Check 'Show existing entries' to view all records

Data is saved to 'network_data.xlsx' in the current directory.
""")

# Optional: Add download button
if os.path.exists('./app/network_data.xlsx'):
    with open('./app/network_data.xlsx', 'rb') as f:
        st.sidebar.download_button(
            label="Download Excel File",
            data=f,
            file_name='network_data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )


