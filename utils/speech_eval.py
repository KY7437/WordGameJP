import speech_recognition as sr
import jaconv

def recognize_and_check(target_word: str) -> bool:
    r = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=3)
            result = r.recognize_google(audio, language="ja-JP")
        except:
            return False

    # 히라가나로 통일해서 비교
    spoken = jaconv.kata2hira(result)
    target = jaconv.kata2hira(target_word)

    return spoken == target
