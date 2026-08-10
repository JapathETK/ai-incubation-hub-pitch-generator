import streamlit as st
import json
import pandas as pd
from pitch_generator import generate_pitch

# --- Page Configuration ---
st.set_page_config(page_title="AI Pitch Generator", layout="wide")
st.title("🚀 AI Incubation Hub Pitch Generator")

# --- Donor Database (Expandable) ---
@st.cache_data
def load_donor_data():
    """Loads and caches the donor database."""
    return pd.DataFrame([
        {
            "Donor": "Incentive Fund",
            "Focus": "SME Development, Innovation",
            "Sector": "Government",
            "Website": "https://incentivefund.gov.pg",
            "Apply": "https://incentivefund.gov.pg/apply"
        },
        {
            "Donor": "CEFI Fintech Hub",
            "Focus": "Fintech Startups",
            "Sector": "Private",
            "Website": "https://www.cefi.com.pg",
            "Apply": "https://www.cefi.com.pg/incubation"
        },
        {
            "Donor": "UNDP PNG",
            "Focus": "Sustainable Development, Climate",
            "Sector": "International",
            "Website": "https://www.undp.org/papua-new-guinea",
            "Apply": "https://www.undp.org/papua-new-guinea/projects"
        },
        {
            "Donor": "World Bank PNG",
            "Focus": "Infrastructure, Agriculture",
            "Sector": "International",
            "Website": "https://www.worldbank.org/en/country/png",
            "Apply": "https://projects.worldbank.org/en/projects-operations/projects-list"
        },
        {
            "Donor": "Asian Development Bank",
            "Focus": "Economic Development, Energy",
            "Sector": "International",
            "Website": "https://www.adb.org/countries/papua-new-guinea",
            "Apply": "https://www.adb.org/projects"
        },
        # Add more donors here as needed
    ])

donors = load_donor_data()

# --- AI Donor Matching Function (The Minor Enhancement) ---
def ai_match_donor(pitch_text, donors_df):
    """
    Uses OpenAI to intelligently match the pitch with the most suitable donors.
    """
    # Prepare the donor list for the prompt
    donor_list = donors_df[['Donor', 'Focus']].to_string(index=False)

    prompt = f"""
You are an expert grant and funding advisor.

Your task is to analyze the following pitch and recommend the three most suitable donors from the provided list.

**Pitch Summary:**
{pitch_text[:1000]} # Limit length to avoid token issues

**Donor List:**
{donor_list}

**Instructions:**
1.  Return only the names of the top 3 donors.
2.  Provide a clear, concise reason for why each donor is a good match.
3.  Format your response as a simple list like the example below:

**Example Output Format:**
- **Donor A:** [Reason for match]
- **Donor B:** [Reason for match]
- **Donor C:** [Reason for match]
"""
    try:
        # Assuming your OpenAI client is initialized in pitch_generator.py
        # You might need to import it here if you haven't set up a separate client.
        # For this example, we'll create a new client instance using st.secrets.
        from openai import OpenAI
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or a more advanced model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error during AI matching: {e}. Please check your OpenAI credits or key."

# --- SIDEBAR: Donor Database ---
with st.sidebar:
    st.header("🏢 Donor Database")
    st.dataframe(donors[["Donor", "Focus", "Sector"]], use_container_width=True)
    st.caption("Click the 'Apply Now' button under the generated pitch to apply.")

# --- MAIN FORM ---
st.subheader("📝 Enter Your Innovation Hub Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Hub Name")
    location = st.text_input("Location")
    focus = st.text_area("Focus Areas (comma separated)")

with col2:
    problem = st.text_area("Problem Statement")
    solution = st.text_area("Proposed Solution")
    beneficiaries = st.text_area("Beneficiaries")
    funding = st.text_input("Funding Needed")

# --- FILE UPLOAD SECTION ---
st.subheader("📎 Upload Supporting Documents")
uploaded_files = st.file_uploader(
    "Upload videos, papers, or other supporting documents",
    type=["pdf", "docx", "jpg", "png", "mp4"],
    accept_multiple_files=True,
    help="Upload files to support your pitch"
)

# --- GENERATE PITCH & SHOW DONOR MATCHES ---
if st.button("🎯 Generate Pitch", type="primary"):
    if not name:
        st.warning("Please enter at least a Hub Name")
    else:
        with st.spinner("Generating your pitch and finding best-fit donors..."):
            # Prepare data for pitch generation
            data = {
                "name": name,
                "location": location,
                "focus": focus.split(",") if focus else [],
                "problem": problem,
                "solution": solution,
                "beneficiaries": beneficiaries,
                "funding": funding
            }

            # 1. Generate the pitch
            pitch = generate_pitch(data)

            # 2. Display the pitch
            st.subheader("📄 Generated Pitch")
            st.text_area("Your Pitch", pitch, height=400, key="generated_pitch")

            # 3. Show uploaded files
            if uploaded_files:
                st.subheader("📎 Uploaded Files")
                for file in uploaded_files:
                    st.write(f"- {file.name}")

            # --- ENHANCED DONOR MATCHING SECTION ---
            st.subheader("🏢 Suggested Donors for This Pitch")
            st.info("The AI has analyzed your pitch and selected the most relevant donors.")

            # --- Call the AI Donor Matching Function ---
            # Create a comprehensive pitch text for the AI to analyze
            full_pitch_text = f"Hub Name: {name}\nProblem: {problem}\nSolution: {solution}\nFocus Areas: {focus}\nFunding: {funding}"

            ai_donor_suggestions = ai_match_donor(full_pitch_text, donors)

            if "Error" in ai_donor_suggestions or "⚠️" in ai_donor_suggestions:
                st.error(ai_donor_suggestions)
                # Fallback to the simple keyword matching if AI fails
                st.warning("Using fallback matching method. Please check your OpenAI credits.")
                # ... (Keep the previous fallback logic if needed) ...
            else:
                # Display the AI-generated suggestions
                st.markdown(ai_donor_suggestions)

                # Optionally, add "Apply Now" buttons for the matched donors.
                # This part is more complex to parse from the AI output, so we'll keep the
                # buttons for all donors below.
                st.divider()
                st.subheader("📋 Full Donor List with Application Links")
                for idx, row in donors.iterrows():
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                        with col1:
                            st.markdown(f"**{row['Donor']}**")
                        with col2:
                            st.write(row['Focus'])
                        with col3:
                            st.link_button("🌐 Website", row["Website"])
                        with col4:
                            st.link_button("📝 Apply Now", row["Apply"])
                        st.divider()
