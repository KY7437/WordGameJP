import json
import re
from collections import defaultdict

# JMdict 간이 텍스트 버전 사용 (미리 다운받아야 함)
JM_DICT_PATH = "data/jmdict_sample.txt"
OUTPUT_PATH = "data/words.json"


def count_mora(word: str) -> int:
    """아주 단순한 모라 수 계산"""
    small = "ゃゅょぁぃぅぇぉャュョァィゥェォ"
    count = 0
    for c in word:
        if c not in small:
            count += 1
    return count


def classify_word(word: str) -> int | None:
    # 히라가나 1글자
    if re.fullmatch(r"[ぁ-ん]", word):
        return 1
    # 가타카나 1글자
    if re.fullmatch(r"[ァ-ン]", word):
        return 2

    mora = count_mora(word)
    if 2 <= mora <= 3:
        return 3
    if 4 <= mora <= 5:
        return 4
    if mora >= 6:
        return 5
    return None


def main():
    levels = defaultdict(list)

    with open(JM_DICT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()

            # 일본어만
            if not re.fullmatch(r"[ぁ-んァ-ンー]+", word):
                continue

            level = classify_word(word)
            if level:
                levels[str(level)].append(word)

    # 개수 제한 (너무 많으면 게임이 무거워짐)
    for k in levels:
        levels[k] = list(set(levels[k]))[:500]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(levels, f, ensure_ascii=False, indent=2)

    print("✅ words.json 자동 생성 완료")


if __name__ == "__main__":
    main()
