import streamlit as st
import requests
import json

FASTAPI_URL = "http://localhost:8000"  # Update if your FastAPI runs on a different port

st.title("Blockchain Event Tracker")

# Input fields
vehicle_id = st.text_input("Vehicle ID")
location = st.text_input("Location")
speed = st.number_input("Speed", value=0.0)
incident = st.text_input("Incident (optional)")

# Add event button
if st.button("Add Event"):
    data = {
        "vehicle_id": vehicle_id,
        "location": location,
        "speed": speed,
    }
    if incident:
        data["incident"] = incident

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(f"{FASTAPI_URL}/add_event", data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        st.success("Event added successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding event: {e}")

# Display blockchain
if st.button("Get Blockchain"):
    try:
        response = requests.get(f"{FASTAPI_URL}/get_chain")
        response.raise_for_status()
        chain_data = response.json()
        st.write("Blockchain:")
        st.write(chain_data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting blockchain: {e}")

# Check chain validity
if st.button("Is Chain Valid?"):
    try:
        response = requests.get(f"{FASTAPI_URL}/is_valid")
        response.raise_for_status()
        valid_data = response.json()
        st.write(f"Is Chain Valid? {valid_data['is_valid']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error checking chain validity: {e}")
