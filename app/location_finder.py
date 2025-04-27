import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

# Set page title and layout
#st.set_page_config(page_title="Location Finder", layout="wide")
st.title("🧭 Find Location on Map 🗺")

# Function to get coordinates from address
def get_coordinates(address):
    geolocator = Nominatim(user_agent="location_finder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude, location.address
    return None, None, None

# Create input form 
with st.form("location_finder"):
    address = st.text_input("Enter an address (e.g ., Eiffel Tower, Paris):",
                            value="Statue of Liberty")
    submitted = st.form_submit_button("Find Location")

if submitted:
    if address: 
        with st.spinner("Searching location..."):
            lat, lon, found_address = get_coordinates(address)

        if lat and lon:
            st.success("Location found!")

            # Create two columns for map and details
            col1, col2 = st.columns([2, 1])

            with col1:
                # create folium Map
                m = folium.Map(location=[lat, lon], zoom_start=16)
                folium.Marker(
                    [lat, lon],
                    popup=found_address,
                    tooltip="Click for address",
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

                # Display map
                folium_static(m, width=700, height=500)

            with col2:
                st.subheader("Location Details")
                st.write(f"**Address:** {found_address}")
                st.write(f"**Latitude:** {lat:.4f}")
                st.write(f"**Longitude:** {lon:.4f}")

                # Show raw coordinates
                st.code(f"Coordinates:\n{lat:.6f}, {lon:.6f}", language="text")

        else:
            st.error("Could not find location. Please try a different address.")

    else:
        st.warning("Please enter an address to search")



