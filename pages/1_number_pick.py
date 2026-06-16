import streamlit as st
import random

MAX_TRIES = 10

st.title("🎯 숫자 맞추기 게임")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)
if "left" not in st.session_state:
    st.session_state.left = MAX_TRIES
if "done" not in st.session_state:
    st.session_state.done = False
if "win" not in st.session_state:
    st.session_state.win = False
if "msg" not in st.session_state:
    st.session_state.msg = None   # 이전 추측 힌트를 저장할 칸


def reset_game():
    # 입력칸(guess), 힌트(msg)까지 모두 삭제
    for key in ["secret", "left", "done", "win", "msg", "guess"]:
        if key in st.session_state:
            del st.session_state[key]


if not st.session_state.done:
    st.metric("남은 기회", f"{st.session_state.left}번")

    # 직전 추측에 대한 힌트 표시 (rerun 후에도 유지되도록 session_state에서 꺼냄)
    if st.session_state.msg:
        kind, text = st.session_state.msg
        if kind == "info":
            st.info(text)
        else:
            st.warning(text)

    with st.form("guess_form"):
        guess = st.number_input(
            "1~100 사이 숫자를 입력하세요",
            min_value=1, max_value=100, step=1,
            key="guess",   # ← 입력칸에 이름표 부여
        )
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("추측하기", use_container_width=True)
        with col2:
            reset = st.form_submit_button("다시 하기", use_container_width=True)

    if reset:
        reset_game()
        st.rerun()

    if submitted:
        st.session_state.left -= 1

        if guess == st.session_state.secret:
            st.session_state.win = True
            st.session_state.done = True
        elif st.session_state.left == 0:
            st.session_state.done = True
        elif guess < st.session_state.secret:
            st.session_state.msg = ("info", "📈 더 높아요!")
        else:
            st.session_state.msg = ("warning", "📉 더 낮아요!")

        st.rerun()   # ← 추측 처리 후 즉시 재실행 → metric이 깎인 값으로 갱신

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
