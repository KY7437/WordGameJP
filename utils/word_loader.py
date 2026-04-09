import json
import random

def get_random_word(level: int) -> str:
    with open("data/words.json", "r", encoding="utf-8") as f:
        words = json.load(f)

    level_words = words.get(str(level), [])
    if not level_words:
        return "データなし"

    return random.choice(level_words)
