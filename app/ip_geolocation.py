import streamlit as st
import requests 
import pandas as pd 




# Title and description
st.title("IP Address Geolocation Mapper 🌍")
st.markdown("Enter an IP address to display its geographical location on the map.")

# Input IP address
ip_address = st.text_input("Enter IP Address:", placeholder="")

# Add your ipinfo.io API token here
API_TOKEN = "34e55b3fff37de"

if st.button("Locate IP"):
    if not ip_address:
        st.error("Please enter a valid IP address.")
    else:
        try:
            # make API request to ipinfo.io
            response= requests.get(f"https://ipinfo.io/{ip_address}/json?token={API_TOKEN}")
            data = response.json()

            if 'error' in data:
                st.error(f"Error: {data['error']['message']}")
            else:
                # Extract location information
                city = data.get('city', 'N/A')
                region = data.get('region', 'N/A')
                country = data.get('country', 'N/A')
                loc = data.get('loc', '').split(',')

                if len(loc) == 2:
                    latitude, longitude = map(float, loc)

                    #Create DataFrame for mapping
                    df = pd.DataFrame({
                        'latitude': [latitude],
                        'longitude': [longitude]
                    })

                    # Display infomation
                    st.success("Location found!")
                    st.subheader("Location Details:")
                    st.write(f"**IP Address:** {ip_address}")
                    st.write(f"**City:** {city}")
                    st.write(f"**State/Region:** {region}")
                    st.write(f"**Country:** {country}")

                    # Display Map
                    st.subheader("Geographical Location:")
                    st.map(df, zoom=12)

                else:
                    st.error("Could not retrieve valid cordinates for this IP address.")

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Instructions for getting API token
st.markdown("""
    ---
    **Note:**
    1. Get a free API token from [ipinfo.io](https://ipinfo.io/)
    2. Replace 'YOUR_API_TOKEN' in the code with your actual token
    3. Free tier allows 50000 requests/month
""")





