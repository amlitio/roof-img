import streamlit as st
import requests
from PIL import Image

# Load API keys
st.secrets["gcp_key"]
st.secrets["anthropic_key"]

# Get location from address
def get_location(address):
  
  url = "https://maps.googleapis.com/maps/api/geocode/json"
  
  params = {
    "address": address,
    "key": st.secrets["gcp_key"]
  }
  
  res = requests.get(url, params=params)
  data = res.json()
  
  if data["status"] == "OK":
    location = data["results"][0]["geometry"]["location"]
    return location
  
  else:
    st.error("Unable to find location for address")
    return None

# Get satellite image  
def get_satellite(location):
  
  url = "https://maps.googleapis.com/maps/api/staticmap"

  params = {
    "center": f"{location['lat']},{location['lng']}",
    "zoom": 20,
    "size": "640x640",
    "maptype": "satellite",
    "key": st.secrets["gcp_key"] 
  }

  res = requests.get(url, params=params)

  return res.content

# Analyze roof image
def analyze_roof(image):

  url = "https://api.anthropic.com/v1/inference"
  headers = {"Authorization": f"Bearer {st.secrets['anthropic_key']}"}  

  payload = {
    "model": "claude",
    "prompt": f"Analyze this roof image and describe any potential damage, wear and tear, or issues you notice: {image}"
  }

  res = requests.post(url, json=payload, headers=headers)

  return res.json()["text"]

# Streamlit app
st.title("Roof Analysis App")

address = st.text_input("Enter address")

if address:

  location = get_location(address)

  if location is None:
    st.error("Unable to find location")

  else:

    image = get_satellite(location)
    
    st.subheader("Roof Image")
    st.image(image)

    analysis = analyze_roof(image)

    st.subheader("Roof Analysis")
    st.write(analysis)
    
else:
  st.write("Enter address above")
