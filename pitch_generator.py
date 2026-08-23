import json
import streamlit as st
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_pitch(data):
    """
    Generates a world-class, donor-ready funding proposal with exceptional success rates.
    Aligns with PNG MTDP IV, 2050 Strategy for the Blue Pacific Continent, SDGs, and all major donor priorities.
    Now includes donor‑tailoring: if a donor is selected, the proposal highlights alignment with that donor.
    """
    # --- Read desired page count from data (default 10) ---
    desired_pages = data.get('desired_pages', 10)
    # Estimate tokens: ~300 per page, cap at 4096 for safety
    max_tokens = min(desired_pages * 300, 4096)

    # Get the selected donor (if any)
    selected_donor = data.get('selected_donor', None)

    # Build the prompt, including the donor if selected
    donor_instruction = ""
    if selected_donor:
        donor_instruction = f"""
**The proposal is specifically tailored for: {selected_donor}**  
Throughout the proposal, explicitly highlight alignment with this donor's focus areas, funding calls, and strategic objectives.
"""

    prompt = f"""
You are a Senior Grant Consultant with over 25 years of experience securing multi-million dollar funding from top international development organizations (ADB, World Bank, EU, DFAT, UNDP, GCF, Global Fund, GPE) for projects in the Pacific region. Your track record is built on crafting winning proposals that align with national development plans, regional strategies, and donor priorities. You have a 95% success rate in securing funding for your clients.

Your task is to create a **COMPREHENSIVE, PERSUASIVE, AND DATA-DRIVEN FUNDING PROPOSAL** for an innovation hub in Papua New Guinea. The proposal must be structured, professional, and ready for immediate submission to major international donors. It must be aligned with the following frameworks:

**1. PNG's National Development Frameworks:**
- **Medium Term Development Plan IV (MTDP IV) 2023-2027:** The proposal must explicitly contribute to the MTDP IV's core objectives: achieving a K200 billion economy by 2030, creating one million new jobs by 2027, and improving the quality of life for all citizens. It must also align with the 12 Strategic Priority Areas (SPAs), particularly:
    - **SPA 1: Strategic Economic Investment** – The hub will stimulate private sector growth and attract investment.
    - **SPA 3: Quality Education & Skilled Human Capital** – The hub will provide practical, entrepreneurial education and bridge the gap between academia and industry.
    - **SPA 4: Quality and Affordable Health Care** – The hub can support HealthTech innovations to improve service delivery.
    - **SPA 8: Digital Government, National Statistics & Public Service Governance** – The hub's focus on Fintech and Digital Innovation directly supports PNG's digital transformation.
    - **SPA 10: Climate Change and Protection of the Natural Environment** – The hub can incubate GreenTech and climate-resilient startups.
    - **SPA 11: Population, Youth and Woman Empowerment** – The hub will have targeted programs for youth and women entrepreneurs.

**2. Regional Pacific Frameworks:**
- **2050 Strategy for the Blue Pacific Continent:** The proposal must contribute to the vision of a resilient Pacific of peace, harmony, security, social inclusion, and prosperity. It must align with the six strategic goals (2025-2030), particularly:
    - **Enhanced, Sustainable and Inclusive Economic Growth** – The hub will foster entrepreneurship and create jobs.
    - **Strengthened Regional Trade and Investment** – The hub will support SMEs and startups that can engage in regional trade.
    - **Technology and Connectivity** – The hub will leverage digital technologies to drive innovation.
- **Pacific Aid for Trade Strategy (PAfTS) 2026-2030:** The hub can contribute to strengthening regional connectivity and expanding opportunities in services trade.
- **Pacific Islands Forum (PIF) Priorities:** The hub aligns with PIF's focus on economic resilience, climate action, and sustainable development.

**3. Global Frameworks:**
- **UN Sustainable Development Goals (SDGs):** The proposal must explicitly contribute to SDG 4 (Quality Education), SDG 8 (Decent Work and Economic Growth), SDG 9 (Industry, Innovation and Infrastructure), SDG 10 (Reduced Inequalities), SDG 17 (Partnerships for the Goals), and SDG 13 (Climate Action).
- **Paris Agreement:** The proposal must support PNG's Nationally Determined Contributions (NDCs) for climate action, particularly the 29% reduction in energy-sector emissions by 2035 and achieving 80% renewable energy share in on-grid electricity generation by 2035.
- **Sendai Framework for Disaster Risk Reduction 2015-2030:** The hub can support the development of disaster-resilient technologies and early warning systems.

**4. Donor Priorities (Align to increase chances of funding):**
- **ADB:** Align with ADB's country assistance pipeline ($1.85 billion for 2026-2028) focused on transport, public sector management, energy, and human and social development. ADB's new Pacific Approach (2026-2030) focuses on building long-term resilience in small island economies.
- **World Bank:** Center on job creation and align with the Country Partnership Framework's (CPF) four priorities: building skills and human capital, connecting communities to basic infrastructure, strengthening economic governance, and supporting private sector growth and economic diversification.
- **EU:** Align with the EU Global Gateway priorities and the Multiannual Indicative Programme (MIP) for PNG, focusing on sustainable infrastructure, renewable energy, digital transformation, and agriculture value chains.
- **DFAT (Australia):** Align with the PNG-Australia Comprehensive Strategic and Economic Partnership (CSEP) and the Incentive Fund's focus on improving social and economic development outcomes.
- **UNDP:** Align with UNDP's strategic plan (2026-2029) and its Pacific Office priorities under three outcome areas: Planet, Prosperity, and Peace.
- **Green Climate Fund (GCF):** Align with PNG's climate priorities, including supporting sustainable livelihoods and low-emission development.
- **Global Fund:** Align with health system strengthening priorities, particularly in the context of supporting health innovation.
- **Global Partnership for Education (GPE):** Align with education sector priorities, particularly in the context of skills development and human capital building.

{donor_instruction}

---

**User Inputs:**
- **Hub Name:** {data['name']}
- **Location:** {data['location']}
- **Focus Areas:** {data['focus']}
- **Problem Statement:** {data['problem']}
- **Proposed Solution:** {data['solution']}
- **Target Beneficiaries:** {data['beneficiaries']}
- **Funding Request:** {data['funding']}

---

**Proposal Requirements:**

1. **Length:** Exactly {desired_pages} pages (approx. {desired_pages * 280} words). 
   Be concise if shorter, detailed if longer. Cover all required sections but adjust depth accordingly.
2. **Formatting:** Use clear headings, subheadings, bullet points, and tables where relevant.
3. **Language:** Professional, persuasive, evidence-based, and compelling.
4. **Donor Appeal:** Explicitly highlight alignment with the frameworks and donor priorities listed above.
5. **Data-Driven:** Include specific numbers, statistics, and evidence from credible sources.
6. **Sustainability:** Demonstrate long-term sustainability beyond the initial funding period.

---

**STRUCTURE: You MUST include ALL of the following sections in this exact order, but adjust the depth to fit within {desired_pages} pages.**

# TABLE OF CONTENTS
(Provide a detailed list of all sections with page numbers.)

# LIST OF ACRONYMS AND ABBREVIATIONS
(Provide a comprehensive list of all acronyms used in the proposal.)

# EXECUTIVE SUMMARY
- Hook: Start with a compelling statement about PNG's potential and the urgent need for innovation.
- Project Overview: What is the innovation hub and what does it aim to achieve?
- Key Objectives: List 5-7 specific, measurable objectives.
- Alignment: Explicitly state alignment with PNG's MTDP IV, the 2050 Strategy for the Blue Pacific Continent, SDGs, and key donor priorities (ADB, World Bank, EU, DFAT, UNDP, GCF).
- Funding Request: Clearly state the total funding request ({data['funding']}).
- Expected Impact: Quantify the expected outcomes (e.g., number of jobs created, startups supported) and contribution to national and regional goals.
- Theory of Change: Briefly describe how the hub will achieve its objectives.

# INTRODUCTION AND BACKGROUND
- Context: Describe PNG's current innovation and entrepreneurship ecosystem.
- Gap Analysis: Identify the specific gaps (funding, mentorship, commercialisation) that the hub will address.
- National and Regional Alignment: Explain how the hub directly supports the MTDP IV's goal of creating one million jobs and the 2050 Strategy's vision for a prosperous Pacific.
- Urgency: Explain why this project is needed now, referencing current challenges and opportunities.
- Literature Review: Reference relevant studies and reports on innovation and entrepreneurship in PNG and the Pacific.

# PROBLEM STATEMENT
- Detailed Description: Elaborate on the problem, using the user's input.
- Statistical Evidence: Include relevant data (e.g., SME failure rates, youth unemployment in PNG, the "innovation gap" between academia and industry).
- Consequences: Describe the negative consequences of inaction (e.g., continued brain drain, economic stagnation, failure to achieve MTDP IV targets).
- Regional Context: Link the problem to similar challenges across the Pacific and the 2050 Strategy's goals.
- Global Context: Link the problem to global challenges (e.g., climate change, digital divide, inequality).

# PROJECT DESCRIPTION AND PROPOSED SOLUTION
- Introduction to the Hub: Describe the innovation hub in detail.
- Core Programs: Explain the key programs (mentorship, incubation, funding access, networking, training workshops).
- Unique Selling Points: What makes this hub different and more effective than existing initiatives?
- Innovation and Technology: How will the hub leverage technology (AI, fintech, digital platforms) to advance PNG's digital government agenda (SPA 8)?
- Implementation Approach: How will the hub be set up and operated?
- Contribution to SDGs: Explicitly link the project to SDG 4 (Quality Education), SDG 8 (Decent Work and Economic Growth), SDG 9 (Industry, Innovation and Infrastructure), SDG 10 (Reduced Inequalities), SDG 17 (Partnerships for the Goals), and SDG 13 (Climate Action).

# TARGET BENEFICIARIES
- Primary Beneficiaries: Students, entrepreneurs, startups, SMEs.
- Secondary Beneficiaries: Local communities, government agencies, industry partners.
- Quantification: Provide estimated numbers (e.g., 100 students mentored annually, 20 startups incubated per year).
- Impact on Beneficiaries: Describe how each group will benefit (skills, jobs, funding, growth), with a focus on youth and women empowerment (SPA 11).
- Inclusive Approach: Describe how the hub will ensure equal access for women, youth, and marginalised groups.

# MARKET AND IMPACT ANALYSIS
- Market Opportunity: Describe the market for innovation in PNG and the Pacific.
- Economic Impact: Quantify the potential economic benefits (job creation, increased GDP) and contribution to PNG's goal of a K200 billion economy by 2030.
- Social Impact: Describe the social benefits (empowerment, poverty reduction, gender equality).
- Regional Impact: Explain how the hub can be a model for other Pacific Island countries, contributing to the 2050 Strategy's goal of enhanced regional economic growth.
- Environmental Impact: Describe the potential environmental benefits (green entrepreneurship, climate resilience).

# BUSINESS MODEL AND SUSTAINABILITY
- Revenue Streams: Identify potential revenue sources (grants, sponsorships, service fees, alumni contributions, endowment fund).
- Cost Structure: Break down the costs (staff, infrastructure, programs, operations).
- Sustainability Plan: Explain how the hub will sustain itself after the initial funding period, aligning with donor expectations for long-term impact.
- Scalability: Describe how the hub's model can be replicated in other universities or regions across the Pacific.
- Risk Management: Describe how the hub will manage financial and operational risks.

# DETAILED BUDGET BREAKDOWN
(Create a detailed table with the following categories and justifications.)

| Category | Subcategory | Amount (K) | Justification |
|----------|-------------|------------|---------------|
| Personnel | Director, Programme Manager, Mentorship Coordinator, Admin Staff | 250,000 | Essential for experienced leadership and operations |
| Infrastructure | ICT, co-working space, hardware, software | 150,000 | Necessary for startup incubation |
| Programme Activities | Workshops, mentorship, hackathons, demo days, training | 100,000 | Core programme delivery |
| Operations | Utilities, supplies, travel, communication | 40,000 | Day-to-day operations |
| Monitoring & Evaluation | Data collection, reporting, impact assessment | 20,000 | Ensure accountability and learning |
| Contingency | Unforeseen expenses | 10,000 | Risk mitigation |
| **TOTAL** | | **570,000** | Aligns with funding request |

# IMPLEMENTATION TIMELINE
- Phase 1 (Months 1-3): Setup, recruitment, procurement.
- Phase 2 (Months 4-6): Launch programmes, first cohort.
- Phase 3 (Months 7-12): Scaling, partnerships, measurable outcomes.
- Phase 4 (Years 2-3): Sustainability, expansion, replication.
- Gantt Chart: (Provide a placeholder for a visual timeline)

# ORGANISATIONAL STRUCTURE AND TEAM
- Key Personnel: Roles and responsibilities (Director, Programme Manager, Mentorship Coordinator, Finance Officer, Admin Officer).
- Skills and Experience: Highlight the team's relevant expertise in innovation, entrepreneurship, and project management.
- Advisory Board: Mention the creation of an advisory board with industry leaders and academics.
- Capacity Building: Describe how the team will be trained and developed.

# MONITORING, EVALUATION, AND LEARNING (MEL)
- KPIs: Define Key Performance Indicators aligned with MTDP IV and donor priorities (e.g., number of startups incubated, jobs created, funds raised by alumni, contribution to GDP growth, percentage of female participants).
- Data Collection: How will data be collected (surveys, reports, tracking systems, interviews)?
- Reporting: How will progress be reported to donors (quarterly reports, annual reviews, impact reports)?
- Learning: How will the hub adapt and improve based on learnings?
- Evaluation: Describe how the hub will be evaluated (mid-term evaluation, end-of-project evaluation).

# RISK ASSESSMENT AND MITIGATION
- Financial Risk: Risk of funding shortfall. Mitigation: Diversify funding sources.
- Operational Risk: Risk of delays. Mitigation: Clear project plan and contingency measures.
- Sustainability Risk: Risk of the hub not becoming self-sustaining. Mitigation: Develop a robust sustainability plan.
- Market Risk: Risk of low demand. Mitigation: Conduct market research and engage stakeholders early.
- Political Risk: Risk of changes in government priorities. Mitigation: Engage with multiple government departments.
- Environmental Risk: Risk of natural disasters. Mitigation: Develop a business continuity plan.

# COMMUNICATION AND VISIBILITY PLAN
- Promotion: How will the hub promote its activities (social media, website, events, newsletters)?
- Stakeholder Engagement: How will the hub engage with partners and donors?
- Results Sharing: How will the hub share its successes and lessons learned?
- Branding: How will the hub build its brand identity?

# PARTNERSHIPS AND STAKEHOLDER ENGAGEMENT
- Key Partners: Identify potential partners (government, private sector, NGOs, universities, international organizations).
- Partnership Strategy: How will partnerships be formed and maintained?
- Donor Relations: How will the hub build and maintain relationships with donors?
- MoUs: Describe any existing or planned Memorandums of Understanding.

# GENDER AND SOCIAL INCLUSION
- Commitment: State the hub's commitment to gender equality and social inclusion.
- Strategies: Describe specific strategies to ensure equal access for women, youth, and marginalised groups (SPA 11).
- Targets: Set targets for female participation in programs (e.g., 50% female participation).
- Gender Analysis: Describe how the hub will address gender-specific barriers.

# ENVIRONMENTAL SUSTAINABILITY
- Commitment: State the hub's commitment to environmental sustainability.
- Practices: Describe sustainable practices (energy efficiency, waste reduction, green procurement).
- Green Entrepreneurship: How will the hub promote green entrepreneurship and contribute to climate resilience (SPA 10)?
- Environmental Impact Assessment: Describe any planned environmental impact assessments.

# CONCLUSION AND CALL TO ACTION
- Summary: Recap the strength and importance of the proposal.
- Reaffirm Request: Reiterate the funding request and its importance.
- Next Steps: Outline the next steps for donor engagement (meeting, site visit, further discussions).
- Closing Statement: End with a powerful, persuasive statement about the future impact of the hub on PNG and the Pacific.

---

**FINAL INSTRUCTIONS FOR THE AI:**

1. **Be Specific and Data-Driven:** Use specific numbers and evidence wherever possible. Reference credible sources (ADB, World Bank, UNDP reports).
2. **Align with Frameworks:** Explicitly reference the **MTDP IV**, **2050 Strategy**, **SDGs**, **Paris Agreement**, and **donor priorities** throughout the narrative.
3. **Highlight Donor Priorities:** Frame the project in terms that resonate with major international donors. Emphasize economic growth, job creation, sustainability, and alignment with their strategic goals.
4. **Be Persuasive but Concise:** Use compelling language, but keep it tight – you have only {desired_pages} pages to cover everything.
5. **Be Comprehensive:** Ensure every section is addressed, but avoid repetition and fluff.
6. **Tailor to the Selected Donor:** If a donor is specified above, explicitly highlight alignment with that donor's focus areas and funding calls throughout the proposal.

Now generate the complete proposal – exactly {desired_pages} pages, concise yet thorough.
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