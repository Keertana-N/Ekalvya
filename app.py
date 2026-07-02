import streamlit as st
import pandas as pd
import json

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Ekalvya",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1200px;
}

section[data-testid="stSidebar"]{
    width:260px !important;
    background:#171923;
}

div[data-testid="metric-container"]{
    background:#1C1F2B;
    border-radius:16px;
    padding:18px;
    border:1px solid #2D3748;
    box-shadow:0 4px 15px rgba(0,0,0,0.20);
}

div[data-testid="stMetricLabel"]{
    font-size:15px !important;
    font-weight:600;
}

div[data-testid="stMetricValue"]{
    font-size:24px !important;
    font-weight:700 !important;
}

div[data-testid="stExpander"]{
    border-radius:14px;
    border:1px solid #2D3748;
}

div[data-testid="stDataFrame"]{
    border-radius:15px;
}

.skill{
    display:inline-block;
    background:#2563EB;
    color:white;
    padding:7px 14px;
    margin:4px;
    border-radius:18px;
    font-size:13px;
}

.footer{
    text-align:center;
    color:#9CA3AF;
    margin-top:40px;
    padding-bottom:20px;
}

</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = pd.read_csv("outputs/ekalvya.csv")

candidate_lookup = {}

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)
        candidate_lookup[candidate["candidate_id"]] = candidate

with open("data/job_description.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

titles = []
companies = []
experience = []

for cid in df["candidate_id"]:
    c = candidate_lookup[cid]
    titles.append(c["profile"]["current_title"])
    companies.append(c["profile"]["current_company"])
    experience.append(c["profile"]["years_of_experience"])

df["title"] = titles
df["company"] = companies
df["experience"] = experience

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("🎯 Ekalvya")

    st.caption("AI-Powered Candidate Discovery Platform")

    st.markdown("---")

    st.markdown("### 📌 Ranking Signals")

    st.markdown("""
✔ Career Evidence

✔ Career Alignment

✔ Keyword Relevance

✔ Recruiter Behaviour

✔ Experience

✔ GitHub Activity

✔ Relocation Preference
""")

    st.markdown("---")

    st.markdown("### 📊 Dataset")

    st.metric("Candidates", "100K")

    st.metric("Results Generated", "Top 100")

    st.markdown("---")

    st.caption(
        "Built for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**"
    )

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
# 🎯 Ekalvya

### Candidate Discovery & Ranking Platform

Identify the most suitable AI candidates using a hybrid ranking pipeline
that combines career evidence, recruiter behavior signals, and profile relevance.
""")

st.success(
    "The ranking system prioritizes recruiter reasoning instead of simple keyword matching."
)

st.divider()

# --------------------------------------------------
# Dashboard Metrics
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Candidates Ranked", "100K")

c2.metric("Candidates Shortlisted", "100")

c3.metric("Target Domain", "AI / ML")

c4.metric("Ranking Method","Hybrid")

st.divider()

# --------------------------------------------------
# Job Description
# --------------------------------------------------

with st.expander("📄 View Job Description"):

    st.write(job_description)

st.divider()

# --------------------------------------------------
# Candidate Table
# --------------------------------------------------

st.header("🏆 Top Ranked Candidates")

leaderboard = (
    df[
        [
            "rank",
            "title",
            "company",
            "experience",
            "score"
        ]
    ]
    .head(20)
    .copy()
)

leaderboard["score"] = leaderboard["score"].round(3)

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True
)

selected = st.selectbox(
    "Select Candidate",
    df["candidate_id"]
)

row = df[df["candidate_id"] == selected].iloc[0]

candidate = candidate_lookup[selected]

st.divider()

# --------------------------------------------------
# Candidate Metrics
# --------------------------------------------------

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "🏆 Rank",
    int(row["rank"])
)

m2.metric(
    "⭐ Score",
    round(row["score"], 3)
)

m3.metric(
    "💼 Experience",
    f'{candidate["profile"]["years_of_experience"]} yrs'
)

m4.metric(
    "🏢 Company",
    candidate["profile"]["current_company"]
)

# --------------------------------------------------
# Match Score
# --------------------------------------------------

score = float(row["score"])

st.subheader("📈 Candidate Match Score")

st.progress(score)

st.success(f"{score*100:.1f}% Match Score")

st.divider()

# --------------------------------------------------
# Profile
# --------------------------------------------------

st.header(candidate["profile"]["current_title"])

st.caption(candidate["profile"]["current_company"])

st.write(candidate["profile"]["summary"])

st.divider()

# --------------------------------------------------
# Reasoning
# --------------------------------------------------

st.subheader("⭐ Recruiter Reasoning")

st.success(row["reasoning"])

st.divider()

# --------------------------------------------------
# Career History
# --------------------------------------------------

st.subheader("💼 Career History")

for job in candidate["career_history"]:

    with st.expander(f"💼 {job['title']}"):

        st.markdown(
            f"**Company:** {job['company']}"
        )

        st.write(job["description"])

st.divider()

# --------------------------------------------------
# Skills
# --------------------------------------------------

st.subheader("🛠 Skills")

skills = [skill["name"] for skill in candidate["skills"]]

badge_html = ""

for skill in skills:
    badge_html += f"<span class='skill'>{skill}</span>"

st.markdown(
    badge_html,
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown("""
<hr>

<div class="footer">

<b>🎯 Ekalvya</b><br>

Built for the Redrob Intelligent Candidate Discovery & Ranking Challenge

Developed using Python • Pandas • Streamlit

</div>
""", unsafe_allow_html=True)