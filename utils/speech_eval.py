import speech_recognition as sr
import jaconv
from difflib import SequenceMatcher


SIMILARITY_THRESHOLD = 0.8  # ⭐ 80% 기준


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def recognize_and_check(target_word: str) -> bool:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=3)
            result = r.recognize_google(audio, language="ja-JP")
        except:
            return False

    spoken = jaconv.kata2hira(result)
    target = jaconv.kata2hira(target_word)

    score = similarity(spoken, target)
    return score >= SIMILARITY_THRESHOLD
