<div align="center">

# 🎯 Ekalvya

### AI-Powered Candidate Discovery & Ranking Platform

**Built for the Redrob Intelligent Candidate Discovery & Ranking Challenge**

*Finding the right candidate through recruiter-inspired reasoning rather than simple keyword matching.*

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python">
<img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit">
<img src="https://img.shields.io/badge/Pandas-Data%20Analysis-blue?style=for-the-badge&logo=pandas">
<img src="https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikitlearn">

</div>

---

# 📖 Overview

Traditional Applicant Tracking Systems (ATS) rely heavily on keyword matching, often overlooking genuinely qualified candidates.

**Ekalvya** is a recruiter-inspired candidate ranking platform that evaluates candidates using multiple signals such as career evidence, career alignment, behavioral signals, technical relevance, and professional experience to identify the most suitable candidates.

---

# ✨ Features

- Intelligent candidate ranking
- Career evidence analysis
- Career alignment scoring
- Recruiter behavior signals
- Explainable recruiter reasoning
- Interactive Streamlit dashboard
- Top-100 candidate generation

---

# 🏗️ System Architecture

```mermaid
flowchart LR

A[Candidate Dataset]
-->B[Feature Engineering]

B-->C[Career Evidence]

B-->D[Keyword Relevance]

B-->E[Career Alignment]

B-->F[Behavior Signals]

B-->G[Experience]

C-->H[Ranking Engine]

D-->H

E-->H

F-->H

G-->H

H-->I[Top 100 Candidates]

I-->J[Recruiter Reasoning]

J-->K[Streamlit Dashboard]
```

---

# 🖥 Dashboard

### Home

<p align="center">
<img src="images/dashboard.png" width="900">
</p>

### Candidate Ranking

<p align="center">
<img src="images/ranking.png" width="900">
</p>

### Candidate Profile

<p align="center">
<img src="images/profile.png" width="900">
</p>

---

## Project Structure

```text
ekalvya/

├── data/
├── notebooks/
├── outputs/
├── src/
├── app.py
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Scikit-Learn
- Sentence Transformers
- Streamlit
- Matplotlib
- Git & GitHub

---

## Getting Started

```bash
git clone https://github.com/Keertana-N/Ekalvya.git

cd Ekalvya

pip install -r requirements.txt

python src/ranking.py

streamlit run app.py
```

---

## 📈 Results

- Processed **100,000 candidate profiles**
- Generated **Top 100 ranked candidates**
- Reduced keyword-stuffed false positives
- Explainable recruiter reasoning
- Interactive recruiter dashboard

---

## 🔮 Future Work

- Semantic reranking
- Resume PDF parsing
- Vector database integration
- Resume upload
- LLM-powered recruiter summaries

---

<div align="center">

⭐ Built for the **Redrob Intelligent Candidate Discovery & Ranking Challenge**

</div>