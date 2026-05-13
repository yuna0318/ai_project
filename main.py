import streamlit as st
st.title ('나의 첫 웹 서비스 만들기!')
st.text_input('이름이 무엇인가요?')
st.selectbox('무엇을 좋아하시나요?',['오선','콜라','산책'])
st.button('인사말 생성')
