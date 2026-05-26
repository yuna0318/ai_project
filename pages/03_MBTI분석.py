# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 비율 분석")
st.markdown("국가를 선택하면 MBTI 유형 비율을 시각화합니다.")

# CSV 파일 읽기
df = pd.read_csv("countriesMBTI_16types.csv")

# 국가 컬럼 찾기
country_col = df.columns[0]

# MBTI 컬럼
mbti_cols = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 국가 선택
country = st.selectbox(
    "국가 선택",
    sorted(df[country_col].unique())
)

# 선택 국가 데이터
country_data = df[df[country_col] == country].iloc[0]

# MBTI 데이터 추출
values = country_data[mbti_cols].values.astype(float)

# 퍼센트 변환
if values.max() <= 1:
    values = values * 100

# 최고값 인덱스
max_idx = np.argmax(values)

# 색상 생성
base_colors = plt.cm.Blues(np.linspace(0.35, 0.85, len(values)))

# 최고값 보라색 지정
colors = base_colors.copy()
colors[max_idx] = mcolors.to_rgba("#8A2BE2")  # 보라색

# 그래프 생성
fig, ax = plt.subplots(figsize=(14, 7))

bars = ax.bar(
    mbti_cols,
    values,
    color=colors,
    edgecolor="white",
    linewidth=1.2
)

# 값 표시
for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.3,
        f"{height:.1f}%",
        ha='center',
        va='bottom',
        fontsize=10
    )

# 스타일
ax.set_title(f"{country} MBTI 비율", fontsize=20, weight="bold")
ax.set_ylabel("비율 (%)", fontsize=12)
ax.set_xlabel("MBTI 유형", fontsize=12)

plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.3)

# Streamlit 출력
st.pyplot(fig)

# 최고 유형 표시
top_mbti = mbti_cols[max_idx]
top_value = values[max_idx]

st.markdown("---")
st.subheader("🏆 가장 높은 MBTI")

st.markdown(
    f"""
    ### 💜 {top_mbti}
    비율: **{top_value:.2f}%**
    """
)
