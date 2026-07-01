import json
import pandas as pd

NUM_CANDIDATES = None 

DATA_PATH = "../data/candidates.jsonl"
OUTPUT_PATH = "../outputs/ekalvya.csv"

#loading the datset 

def load_candidates(path, limit=None):
    candidates = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            candidates.append(json.loads(line))

            if limit is not None and len(candidates) >= limit:
                break

    print(f"Loaded {len(candidates)} candidates.")

    return candidates

# -------------------------
# Feature Functions
# -------------------------
#these are the feature functions built in notebook 02_feature_engineering.ipynb

#experience score function
def experience_score(candidate):
    years = candidate["profile"]["years_of_experience"]

    if 5 <= years <= 9:
        return 1.0
    elif 4 <= years <= 12:
        return 0.7
    else:
        return 0.3
    
#open to work function
def open_to_work_score(candidate):
    return float(
        candidate["redrob_signals"]["open_to_work_flag"]
    )

#response rate function
def response_rate_score(candidate):
    return candidate["redrob_signals"][
        "recruiter_response_rate"
    ]

#notice period function
def notice_score(candidate):
    days = candidate["redrob_signals"][
        "notice_period_days"
    ]

    if days <= 30:
        return 1.0
    elif days <= 60:
        return 0.5
    else:
        return 0.0
    
#github score function
def github_score(candidate):
    score = candidate["redrob_signals"][
        "github_activity_score"
    ]
    if score == -1:
        return 0
    return score / 100

#relocation score function
def relocation_score(candidate):
    return float(
        candidate["redrob_signals"][
            "willing_to_relocate"
        ]
    )

EVIDENCE_WORDS = [
    "shipped",
    "production",
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "embedding",
    "evaluation",
    "a/b",
    "learning-to-rank",
    "offline metrics",
    "online metrics",
    "relevance"
]

def career_evidence_score(candidate):
    text = ""

    for job in candidate["career_history"]:
        text += (
            (job.get("title") or "")
            + " "
            + (job.get("description") or "")
            + " "
        )

    text = text.lower()

    score = 0

    for word in EVIDENCE_WORDS:
        if word in text:
            score += 1

    return score / len(EVIDENCE_WORDS)

KEYWORD_WEIGHTS = {
    "retrieval": 5,
    "ranking": 5,
    "recommendation": 5,
    "recommender": 5,
    "search": 4,
    "embedding": 4,
    "embeddings": 4,
    "vector": 3,
    "faiss": 5,
    "pinecone": 5,
    "milvus": 5,
    "qdrant": 5,
    "weaviate": 5,
    "elasticsearch": 4,
    "opensearch": 4,
    "semantic": 3
}

#Keyword score function
def keyword_relevance_score(candidate):
    text = ""

    profile = candidate["profile"]

    text += (profile.get("headline") or "") + " "
    text += (profile.get("summary") or "") + " "

    for job in candidate["career_history"]:
        text += (job.get("title") or "") + " "
        text += (job.get("description") or "") + " "

    for skill in candidate["skills"]:
        text += (skill.get("name") or "") + " "

    text = text.lower()

    score = 0

    for word, weight in KEYWORD_WEIGHTS.items():
        if word in text:
            score += weight

    return score

#career alignment score function
def career_alignment_score(candidate):
    title = candidate["profile"]["current_title"].lower()

    positive_keywords = [
        "ai",
        "machine learning",
        "ml",
        "recommendation",
        "search",
        "nlp",
        "data scientist",
        "applied",
        "retrieval",
        "backend"
    ]

    negative_keywords = [
        "accountant",
        "sales",
        "marketing",
        "graphic",
        "content",
        "hr",
        "operations",
        "project manager",
        "business analyst",
        "customer support",
        "mechanical",
        "civil"
    ]

    if any(word in title for word in negative_keywords):
        return 0.0

    if any(word in title for word in positive_keywords):
        return 1.0

    return 0.5
def build_reasoning(candidate, row):

    profile = candidate["profile"]
    signals = candidate["redrob_signals"]

    title = profile["current_title"]
    years = profile["years_of_experience"]

    reasons = []

    # Experience
    reasons.append(
        f"{years:.1f} years of experience as a {title}"
    )

    # Career evidence
    if row["career_evidence_score"] >= 0.4:
        reasons.append(
            "strong production and retrieval experience"
        )
    elif row["career_evidence_score"] >= 0.2:
        reasons.append(
            "relevant production experience"
        )

    # Career alignment
    if row["career_alignment_score"] == 1.0:
        reasons.append(
            f"current role '{title}' closely matches the target AI/ML position"
        )

    # Behaviour
    if signals["open_to_work_flag"]:
        reasons.append(
            "currently open to work"
        )

    if signals["recruiter_response_rate"] >= 0.7:
        reasons.append(
            "high recruiter response rate"
        )

    if signals["notice_period_days"] <= 30:
        reasons.append(
            "short notice period"
        )
    elif signals["notice_period_days"] >= 90:
        reasons.append(
            "long notice period"
        )

    if signals["github_activity_score"] >= 70:
        reasons.append(
            "strong GitHub activity"
        )

    # Keep it concise
    reasoning = ", ".join(reasons[:4])

    return reasoning + "."
# -------------------------
# Feature Extraction
# -------------------------

def build_feature_dataframe(candidates):

    features = []

    for c in candidates:

        features.append({

            "candidate_id": c["candidate_id"],

            "experience_score":
                experience_score(c),

            "keyword_relevance_score":
                keyword_relevance_score(c),

            "career_evidence_score":
                career_evidence_score(c),

            "career_alignment_score":
                career_alignment_score(c),

            "open_to_work_score":
                open_to_work_score(c),

            "response_rate_score":
                response_rate_score(c),

            "notice_score":
                notice_score(c),

            "github_score":
                github_score(c),

            "relocation_score":
                relocation_score(c)

        })

    features_df = pd.DataFrame(features)

    return features_df

# -------------------------
# Main Function
# -------------------------
if __name__ == "__main__":

    # Load candidates
    candidates = load_candidates(
        DATA_PATH,
        NUM_CANDIDATES
    )

    # Build feature dataframe
    features_df = build_feature_dataframe(candidates)

    # Normalize keyword score
    features_df["keyword_relevance_score_norm"] = (
        features_df["keyword_relevance_score"]
        / features_df["keyword_relevance_score"].max()
    )

    # Behavioral score
    features_df["behavior_score"] = (
        0.4 * features_df["open_to_work_score"]
        + 0.4 * features_df["response_rate_score"]
        + 0.2 * features_df["notice_score"]
    )

    # Final ranking score
    features_df["final_score"] = (
        0.25 * features_df["career_evidence_score"]
        + 0.20 * features_df["keyword_relevance_score_norm"]
        + 0.20 * features_df["career_alignment_score"]
        + 0.15 * features_df["behavior_score"]
        + 0.10 * features_df["experience_score"]
        + 0.05 * features_df["github_score"]
        + 0.05 * features_df["relocation_score"]
    )

    # Rank candidates
    ranked = (
        features_df
        .sort_values("final_score", ascending=False)
        .reset_index(drop=True)
    )

    # Build lookup dictionary
    candidate_lookup = {
        c["candidate_id"]: c
        for c in candidates
    }

    
    # Create submission dataframe
    rows = []

    for _, row in ranked.head(100).iterrows():

        candidate = candidate_lookup[row["candidate_id"]]

        rows.append({

    "candidate_id": candidate["candidate_id"],
    "rank": len(rows) + 1,
    "score": round(row["final_score"], 6),
    "reasoning": build_reasoning(candidate, row)

})

    submission = pd.DataFrame(rows)

    submission.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(submission.head(10))

    print("\nTop 100 candidates saved successfully.")