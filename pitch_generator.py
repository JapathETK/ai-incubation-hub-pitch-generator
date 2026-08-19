import json
import streamlit as st
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_pitch(data):
    """
    Generates a professional incubation hub pitch using OpenAI.
    """
    prompt = f"""
    Create a professional incubation hub pitch for funders and industry.

    Name: {data['name']}
    Location: {data['location']}
    Focus Areas: {data['focus']}
    Problem: {data['problem']}
    Solution: {data['solution']}
    Target Beneficiaries: {data['beneficiaries']}
    Funding Needed: {data['funding']}

    Include:
    - Executive Summary
    - Problem Statement
    - Proposed Solution
    - Market/Impact
    - Business Model
    - Funding Request
    - Expected Outcomes
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Cheaper model - ~$0.002 per pitch
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800  # Limit output length to control cost
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating pitch: {e}"

if __name__ == "__main__":
    try:
        with open("data/sample_input.json") as f:
            data = json.load(f)

        pitch = generate_pitch(data)

        with open("output_pitch.txt", "w") as f:
            f.write(pitch)

        print("✅ Pitch generated successfully! Check output_pitch.txt")
    except FileNotFoundError:
        print("❌ Error: sample_input.json not found. Please make sure it exists in the data/ folder.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")