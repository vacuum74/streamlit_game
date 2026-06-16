import streamlit as st
import random

MAX_TRIES = 10  # 최대 시도 횟수

st.title("🎯 숫자 맞추기 게임")

# 게임 상태 저장 (새로고침해도 유지)
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)
    st.session_state.left = MAX_TRIES   # 남은 기회 (10부터 시작)
    st.session_state.done = False       # 게임 종료 여부
    st.session_state.win = False        # 승리 여부

if not st.session_state.done:
    # 남은 기회를 눈에 띄게 표시
    st.metric("남은 기회", f"{st.session_state.left}번")

    with st.form("guess_form"):
        guess = st.number_input(
            "1~100 사이 숫자를 입력하세요",
            min_value=1, max_value=100, step=1
        )
        submitted = st.form_submit_button("추측하기")

    if submitted:
        st.session_state.left -= 1   # 기회 1 깎기

        if guess == st.session_state.secret:
            st.session_state.win = True
            st.session_state.done = True
            st.rerun()
        elif st.session_state.left == 0:
            # 마지막 기회까지 못 맞힘 → 게임 오버
            st.session_state.done = True
            st.rerun()
        elif guess < st.session_state.secret:
            st.info("📈 더 높아요!")
        else:
            st.warning("📉 더 낮아요!")

if st.session_state.done:
    used = MAX_TRIES - st.session_state.left  # 사용한 횟수 계산
    if st.session_state.win:
        st.success(f"🎉 정답! {used}번 만에 맞혔어요! (남은 기회 {st.session_state.left}번)")
        st.balloons()
    else:
        st.error(f"💀 게임 오버! 기회를 모두 사용했어요. 정답은 {st.session_state.secret}였습니다.")

    if st.button("다시 하기"):
        del st.session_state.secret
        del st.session_state.left
        del st.session_state.done
        del st.session_state.win
        st.rerun()
