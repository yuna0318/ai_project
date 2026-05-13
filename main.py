import streamlit as st
st.title ('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름이 무엇인가요?')
b=st.selectbox('무엇을 좋아하시나요?',['오선','콜라','산책'])
if st.button('인사말 생성'):
  st.write(a+'님 안녕하세요!')
