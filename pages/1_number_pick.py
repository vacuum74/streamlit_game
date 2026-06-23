import streamlit as st
import random

MAX_TRIES = 10

st.title("🎯 숫자 맞추기 게임")
st.write(session_state.secret)
st.write(session_state.guess)
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)
if "left" not in st.session_state:
    st.session_state.left = MAX_TRIES
if "done" not in st.session_state:
    st.session_state.done = False
if "win" not in st.session_state:
    st.session_state.win = False
if "msg" not in st.session_state:
    st.session_state.msg = None


def handle_guess():
    """버튼 클릭 시 호출 — 이 안에서는 guess가 항상 최신 입력값"""
    g = st.session_state.guess
    st.session_state.left -= 1
    if g == st.session_state.secret:
        st.session_state.win = True
        st.session_state.done = True
    elif st.session_state.left == 0:
        st.session_state.done = True
    elif g < st.session_state.secret:
        st.session_state.msg = ("info", "📈 더 높아요!")
    else:
        st.session_state.msg = ("warning", "📉 더 낮아요!")


def reset_game():
    for key in ["secret", "left", "done", "win", "msg", "guess"]:
        if key in st.session_state:
            del st.session_state[key]


if not st.session_state.done:
    st.metric("남은 기회", f"{st.session_state.left}번")
    if st.session_state.msg:
        kind, text = st.session_state.msg
        if kind == "info":
            st.info(text)
        else:
            st.warning(text)

    with st.form("guess_form"):
        st.number_input(
            "1~100 사이 숫자를 입력하세요",
            min_value=1, max_value=100, step=1,
            key="guess",
        )
        col1, col2 = st.columns(2)
        with col1:
            st.form_submit_button("추측하기", use_container_width=True,
                                  on_click=handle_guess)
        with col2:
            st.form_submit_button("다시 하기", use_container_width=True,
                                  on_click=reset_game)

if st.session_state.done:
    used = MAX_TRIES - st.session_state.left
    if st.session_state.win:
        st.success(f"🎉 정답! {used}번 만에 맞혔어요! (남은 기회 {st.session_state.left}번)")
        st.balloons()
    else:
        st.error(f"💀 게임 오버! 기회를 모두 사용했어요. 정답은 {st.session_state.secret}였습니다.")
    st.button("다시 하기", on_click=reset_game)
