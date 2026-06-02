import streamlit as st

st.title("바이브 코딩 수업")
st.write("왼쪽 메뉴를 선택하세요!")

st.page_link("pages/1_number_pick.py", label="🎯 숫자 맞추기")
st.page_link("pages/2_rsp.py", label="✂️ 가위바위보")
