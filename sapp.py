import streamlit as st
import requests

st.title("Roof Satellite Imager")

address = st.text_input("Enter your address:")

if address:

  # Call Google Maps Geocoding API to get latitude and longitude
  api_key = "YOUR_API_KEY" 
  base_url = "https://maps.googleapis.com/maps/api/geocode/json"
  params = {"address": address, "key": api_key}
  
  res = requests.get(base_url, params=params)
  data = res.json()
  
  if data["status"] == "OK":
    lat = data["results"][0]["geometry"]["location"]["lat"]
    lon = data["results"][0]["geometry"]["location"]["lng"]

  else:
    st.error("Unable to find latitude and longitude for this address")
    
  # Call Google Static Maps API to get satellite view  
  zoom = 20 # Adjust zoom level
  satellite_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size=640x640&maptype=satellite&key={api_key}"

  res = requests.get(satellite_url)
  img = res.content

  st.image(img)

else:
  st.write("Enter an address above to get roof satellite view")
