from fastapi import FastAPI
from utils.word_loader import get_random_word
from utils.speech_eval import similarity
import jaconv

app = FastAPI()

@app.get("/word/{level}")
def get_word(level: int):
    word = get_random_word(level)
    return {"word": word}

@app.post("/check")
def check_pronunciation(target: str, spoken: str):
    target = jaconv.kata2hira(target)
    spoken = jaconv.kata2hira(spoken)

    score = similarity(target, spoken)
    return {
        "score": score,
        "correct": score >= 0.8
    }
