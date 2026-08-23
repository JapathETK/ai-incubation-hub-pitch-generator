import json
import streamlit as st
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_pitch(data):
    """
    Generates a premium‑grade, donor‑ready proposal for ANY project.
    Forces in‑text citations and a full Reference List.
    """
    desired_pages = data.get('desired_pages', 10)
    max_tokens = min(desired_pages * 400, 4096)

    selected_donor = data.get('selected_donor', 'No specific donor selected')

    donor_instruction = ""
    if selected_donor and selected_donor != "No specific donor selected":
        donor_instruction = f"""
**CRITICAL: The proposal is specifically tailored for: {selected_donor}**  
Throughout the proposal, explicitly highlight alignment with this donor's focus areas, funding calls, and strategic objectives. Use your knowledge of their published strategies and recent programming documents. Reference the donor's own publications where possible.
"""

    prompt = f"""
You are a Senior Grant Consultant with over 25 years of experience securing multi‑million dollar funding from top international development organizations (ADB, World Bank, EU, DFAT, UNDP, GCF, Global Fund, GPE, etc.) for projects across all sectors. Your track record is built on crafting winning proposals that are **evidence‑based, data‑driven, and fully aligned with donor priorities**. You have a 95% success rate.

Your task is to create a **COMPREHENSIVE, PERSUASIVE, AND DATA‑DRIVEN FUNDING PROPOSAL** for the project described by the user. The proposal must be structured, professional, and ready for immediate submission to major international donors.

**RULES YOU MUST FOLLOW – FAILURE TO FOLLOW ANY OF THESE WILL RESULT IN REJECTION:**

1. **USE THE USER'S EXACT WORDS** for the Problem Statement, Proposed Solution, and Beneficiaries – do NOT paraphrase, shorten, or rewrite them. Copy them exactly as provided.
2. **YOU MUST INCLUDE AT LEAST 8 IN‑TEXT CITATIONS** throughout the proposal – e.g., (World Bank, 2024), (ADB, 2025), (UNDP, 2023), (ILO, 2022), (IMF, 2024). Use plausible years and source names based on your training data.
3. **YOU MUST INCLUDE A FULL REFERENCE LIST** at the end of the proposal – use APA or Harvard style, with full bibliographic details (author, year, title, publisher). This list must have at least 8 entries matching your in‑text citations.
4. **Quantify impact** – include specific numbers (jobs created, beneficiaries reached, emissions reduced, etc.) with citations.
5. **Explicitly reference** alignment with the SDGs, Paris Agreement, and the donor's strategic priorities in every major section.
6. **Be persuasive** – use language that shows this project is a high‑return investment for the donor.

**IMPORTANT:** You are not required to provide live URLs. You may cite reports as if they exist, using plausible titles, authors, and years based on your training data. The goal is to demonstrate that the proposal is grounded in real evidence.

{donor_instruction}

---

**User Inputs – USE VERBATIM (copy exactly, do not paraphrase):**
- Project / Organisation Name: {data['name']}
- Location: {data['location']}
- Focus Areas: {data['focus']}
- Problem Statement (copy exactly – do NOT paraphrase):
{data['problem']}
- Proposed Solution (copy exactly – do NOT paraphrase):
{data['solution']}
- Target Beneficiaries (copy exactly – do NOT paraphrase):
{data['beneficiaries']}
- Funding Request: {data['funding']}

---

**STRUCTURE – you MUST include these sections (adjust depth to fit page limit):**

# TABLE OF CONTENTS
- List all sections with page numbers.

# LIST OF ACRONYMS AND ABBREVIATIONS
- Include all acronyms used (SDGs, ADB, etc.).

# EXECUTIVE SUMMARY (1 page)
- Hook: start with a compelling statement about the project's importance.
- Summarise the project, key objectives (5‑7), and alignment with SDGs and donor priorities.
- State the funding request and expected impact with numbers.
- Brief Theory of Change.

# INTRODUCTION AND BACKGROUND (1‑2 pages)
- Describe the current situation/challenges in the project's sector and location, citing relevant reports (e.g., World Bank country economic updates, sector‑specific assessments). Include at least 2 citations here.
- Identify gaps that the project will address.
- Explain how the project supports national/regional development goals (if known) and SDGs.
- Justify urgency with data and trends.

# PROBLEM STATEMENT (1‑2 pages)
**USE THE USER'S EXACT PROBLEM STATEMENT** – paste it verbatim (copy exactly).
- Then add supporting evidence: statistics, studies, and citations to strengthen the case (at least 2 citations).
- Explain the consequences of inaction.

# PROJECT DESCRIPTION AND PROPOSED SOLUTION (2‑3 pages)
**USE THE USER'S EXACT PROPOSED SOLUTION** – paste it verbatim (copy exactly).
- Elaborate on the project's activities, unique approach, technology, and implementation plan.
- Explicitly link to relevant SDGs (e.g., SDG 3 for health, SDG 4 for education, SDG 7 for energy, etc.). Include at least 2 citations.

# TARGET BENEFICIARIES (1‑2 pages)
**USE THE USER'S EXACT BENEFICIARIES** – paste it verbatim (copy exactly).
- Quantify impact: number of beneficiaries, with breakdown by gender, age, etc., if possible.

# MARKET AND IMPACT ANALYSIS (1‑2 pages)
- Describe the market/need for the project's outputs or outcomes.
- Economic, social, and environmental impacts – quantify where possible. Include at least 2 citations.

# BUSINESS MODEL AND SUSTAINABILITY (1‑2 pages)
- Revenue streams: grants, service fees, partnerships, etc.
- Cost structure: personnel, infrastructure, operations, etc.
- Sustainability plan: diversifying income, building partnerships, scalability.
- Risk management.

# DETAILED BUDGET BREAKDOWN (1 page)
Present a clear budget table with categories and justifications – adapt the sample below to the project's actual cost items.

| Category | Subcategory | Amount (K/USD) | Justification |
|----------|-------------|----------------|---------------|
| Personnel | Key staff | [user amount] | Essential for project delivery |
| Infrastructure | Equipment, facilities | [user amount] | Necessary for operations |
| Programme Activities | Workshops, training, etc. | [user amount] | Core activities |
| Operations | Utilities, supplies, travel | [user amount] | Day‑to‑day operations |
| Monitoring & Evaluation | Data collection, reporting | [user amount] | Accountability and learning |
| Contingency | Unforeseen expenses | [user amount] | Risk mitigation |
| **TOTAL** | | **[user's total]** | Aligns with funding request |

# IMPLEMENTATION TIMELINE (1 page)
- Phases with milestones and deliverables.

# ORGANISATIONAL STRUCTURE AND TEAM (1 page)
- Key personnel and their roles, emphasising relevant experience.

# MONITORING, EVALUATION, AND LEARNING (MEL) (1 page)
- KPIs, data collection, reporting schedule, learning mechanisms.

# RISK ASSESSMENT AND MITIGATION (1 page)
- Identify risks and mitigation strategies.

# COMMUNICATION AND VISIBILITY PLAN (1 page)
- Promotion, stakeholder engagement, results sharing.

# PARTNERSHIPS AND STAKEHOLDER ENGAGEMENT (1 page)
- Key partners and partnership strategy.

# GENDER AND SOCIAL INCLUSION (1 page)
- Commitment to inclusion, strategies, targets.

# ENVIRONMENTAL SUSTAINABILITY (1 page)
- Environmental considerations and green practices.

# CONCLUSION AND CALL TO ACTION (1/2 page)
- Recap, reaffirm request, next steps, powerful closing.

# REFERENCES (1‑2 pages)
**CRITICAL: You MUST include a full Reference List here with at least 8 entries.** Format consistently (APA or Harvard). All in‑text citations must appear in this list.

---

**FINAL INSTRUCTIONS – READ CAREFULLY:**
- **YOU MUST include at least 8 in‑text citations** – e.g., (World Bank, 2024), (ADB, 2025), (UNDP, 2023), etc.
- **YOU MUST include a Reference List** with full bibliographic details (author, year, title, publisher).
- **DO NOT paraphrase the user's problem statement, solution, or beneficiaries** – use them verbatim.
- **Be data‑rich** – include numbers, percentages, and references to credible sources.
- **Align every section** with the donor's priorities if a donor is specified.
- The proposal must be exactly {desired_pages} pages long – adjust detail accordingly.

**REMINDER: Proposals without citations and a reference list are automatically rejected by donors. You must include them.**

Now generate the complete proposal.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating proposal: {e}"

if __name__ == "__main__":
    try:
        with open("data/sample_input.json") as f:
            data = json.load(f)
        pitch = generate_pitch(data)
        with open("output_pitch.txt", "w") as f:
            f.write(pitch)
        print("✅ Proposal generated successfully! Check output_pitch.txt")
    except FileNotFoundError:
        print("❌ Error: sample_input.json not found.")
    except Exception as e:
        print(f"❌ Error: {e}")