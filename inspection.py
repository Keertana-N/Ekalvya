import pandas as pd
import json

top100 = pd.read_csv("outputs/top_100_candidates.csv")

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    candidates = [json.loads(line) for line in f]

candidate_lookup = {
    c["candidate_id"]: c
    for c in candidates
}

for i in range(20):

    cid = top100.iloc[i]["candidate_id"]

    c = candidate_lookup[cid]

    print("=" * 80)
    print("Rank:", i + 1)
    print("Title:", c["profile"]["current_title"])
    print("Company:", c["profile"]["current_company"])
    print("Experience:", c["profile"]["years_of_experience"])
    print()
    print(c["profile"]["summary"][:350])