import json
from openai import OpenAI

# Initialize client
client = OpenAI(api_key="YOUR_API_KEY")

def generate_pitch(data):
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

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    with open("data/sample_input.json") as f:
        data = json.load(f)

    pitch = generate_pitch(data)

    with open("output_pitch.txt", "w") as f:
        f.write(pitch)

    print("Pitch generated successfully! Check output_pitch.txt")