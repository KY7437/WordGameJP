import streamlit as st
import time
from utils.word_loader import get_random_word
from utils.speech_eval import recognize_and_check
from utils.ranking import save_score, load_ranking

st.set_page_config(page_title="日本語 発音ゲーム", layout="centered")

st.title("🎤 日本語 発音スピードゲーム")

# ---------------- 상태 초기화 ----------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "current_word" not in st.session_state:
    st.session_state.current_word = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# ---------------- 설정 ----------------
level = st.selectbox(
    "레벨 선택",
    [
        "1단계: 히라가나",
        "2단계: 가타카나",
        "3단계: 2~3음절",
        "4단계: 4~5음절",
        "5단계: 5음절 이상",
    ],
)

time_limit = st.slider("제한 시간 (초)", 30, 60, 45)

level_map = {
    "1단계: 히라가나": 1,
    "2단계: 가타카나": 2,
    "3단계: 2~3음절": 3,
    "4단계: 4~5음절": 4,
    "5단계: 5음절 이상": 5,
}

# ---------------- 게임 시작 ----------------
if st.button("게임 시작"):
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_over = False
    st.session_state.current_word = get_random_word(level_map[level])

# ---------------- 게임 진행 ----------------
if st.session_state.start_time and not st.session_state.game_over:
    elapsed = time.time() - st.session_state.start_time
    remaining = int(time_limit - elapsed)

    st.subheader(f"⏱ 남은 시간: {remaining}초")

    if remaining <= 0:
        st.session_state.game_over = True
    else:
        if st.session_state.current_word is None:
            st.session_state.current_word = get_random_word(level_map[level])

        st.markdown(
            f"<h1 style='text-align:center'>{st.session_state.current_word}</h1>",
            unsafe_allow_html=True,
        )

        if st.button("🎙 발음하기"):
            correct = recognize_and_check(st.session_state.current_word)
            if correct:
                st.session_state.score += 1
            st.session_state.current_word = None

# ---------------- 종료 & 랭킹 ----------------
if st.session_state.game_over:
    st.subheader(f"🎉 게임 종료! 점수: {st.session_state.score}")

    name = st.text_input("이름 입력 (랭킹 저장)")
    if st.button("랭킹 저장"):
        save_score(name, st.session_state.score)
        st.success("저장 완료!")

    st.subheader("🏆 랭킹")
    ranking = load_ranking()
    for i, r in enumerate(ranking, 1):
        st.write(f"{i}. {r['name']} - {r['score']}")
