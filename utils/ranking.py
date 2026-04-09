import json
import os

RANK_FILE = "data/ranking.json"

def save_score(name: str, score: int):
    if not os.path.exists(RANK_FILE):
        ranking = []
    else:
        with open(RANK_FILE, "r", encoding="utf-8") as f:
            ranking = json.load(f)

    ranking.append({"name": name, "score": score})
    ranking = sorted(ranking, key=lambda x: x["score"], reverse=True)[:10]

    with open(RANK_FILE, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)

def load_ranking():
    if not os.path.exists(RANK_FILE):
        return []
    with open(RANK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
