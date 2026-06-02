import streamlit as st
import random

st.title("🎯 숫자 맞추기 게임")

# 게임 상태 저장 (새로고침해도 유지)
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)
    st.session_state.tries = 0
    st.session_state.done = False

if not st.session_state.done:
    guess = st.number_input("1~100 사이 숫자를 입력하세요", min_value=1, max_value=100, step=1)
    if st.button("추측하기"):
        st.session_state.tries += 1
        if guess < st.session_state.secret:
            st.info("📈 더 높아요!")
        elif guess > st.session_state.secret:
            st.info("📉 더 낮아요!")
        else:
            st.success(f"🎉 정답! {st.session_state.tries}번 만에 맞혔어요!")
            st.session_state.done = True

if st.session_state.done:
    if st.button("다시 하기"):
        del st.session_state.secret
        del st.session_state.tries
        del st.session_state.done
        st.rerun()
