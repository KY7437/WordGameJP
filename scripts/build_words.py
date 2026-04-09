import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict

JM_DICT_PATH = "data/JMdict_e.xml"
OUTPUT_PATH = "data/words.json"


def count_mora(word: str) -> int:
    small = "ゃゅょぁぃぅぇぉャュョァィゥェォ"
    count = 0
    for c in word:
        if c not in small:
            count += 1
    return count


def classify_word(word: str) -> int | None:
    if re.fullmatch(r"[ぁ-ん]", word):
        return 1
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
    levels = defaultdict(set)

    tree = ET.parse(JM_DICT_PATH)
    root = tree.getroot()

    for entry in root.findall("entry"):
        for r_ele in entry.findall("r_ele"):
            reb = r_ele.find("reb")
            if reb is None:
                continue

            word = reb.text

            # 히라가나/가타카나만
            if not re.fullmatch(r"[ぁ-んァ-ンー]+", word):
                continue

            level = classify_word(word)
            if level:
                levels[str(level)].add(word)

    # 레벨별 개수 제한 (게임 성능용)
    result = {}
    for k, v in levels.items():
        result[k] = list(v)[:2000]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("✅ JMdict 기반 words.json 생성 완료")


if __name__ == "__main__":
    main()
