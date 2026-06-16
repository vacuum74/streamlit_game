import streamlit as st
import random

MAX_TRIES = 10

st.title("🎯 숫자 맞추기 게임")

# 각 키를 개별적으로 초기화
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)
if "left" not in st.session_state:
    st.session_state.left = MAX_TRIES
if "done" not in st.session_state:
    st.session_state.done = False
if "win" not in st.session_state:
    st.session_state.win = False


def reset_game():
    """세션을 비워서 게임을 처음부터 다시 시작"""
    for key in ["secret", "left", "done", "win"]:
        if key in st.session_state:
            del st.session_state[key]


if not st.session_state.done:
    st.metric("남은 기회", f"{st.session_state.left}번")

    with st.form("guess_form"):
        guess = st.number_input(
            "1~100 사이 숫자를 입력하세요",
            min_value=1, max_value=100, step=1
        )

        # 버튼 두 개를 가로로 나란히 배치
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("추측하기", use_container_width=True)
        with col2:
            reset = st.form_submit_button("다시 하기", use_container_width=True)

    # 다시 하기를 먼저 검사 (눌렸으면 바로 리셋)
    if reset:
        reset_game()
        st.rerun()

    if submitted:
        st.session_state.left -= 1

        if guess == st.session_state.secret:
            st.session_state.win = True
            st.session_state.done = True
            st.rerun()
        elif st.session_state.left == 0:
            st.session_state.done = True
            st.rerun()
        elif guess < st.session_state.secret:
            st.info("📈 더 높아요!")
        else:
            st.warning("📉 더 낮아요!")

if st.session_state.done:
    used = MAX_TRIES - st.session_state.left
    if st.session_state.win:
        st.success(f"🎉 정답! {used}번 만에 맞혔어요! (남은 기회 {st.session_state.left}번)")
        st.balloons()
    else:
        st.error(f"💀 게임 오버! 기회를 모두 사용했어요. 정답은 {st.session_state.secret}였습니다.")

    if st.button("다시 하기"):
        reset_game()
        st.rerun()
