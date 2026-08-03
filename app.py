import streamlit as st
import json
from pitch_generator import generate_pitch

st.title("AI Incubation Hub Pitch Generator")

name = st.text_input("Hub Name")
location = st.text_input("Location")
focus = st.text_area("Focus Areas (comma separated)")
problem = st.text_area("Problem Statement")
solution = st.text_area("Proposed Solution")
beneficiaries = st.text_area("Beneficiaries")
funding = st.text_input("Funding Needed")

if st.button("Generate Pitch"):
    data = {
        "name": name,
        "location": location,
        "focus": focus.split(","),
        "problem": problem,
        "solution": solution,
        "beneficiaries": beneficiaries,
        "funding": funding
    }

    pitch = generate_pitch(data)
    st.text_area("Generated Pitch", pitch, height=400)