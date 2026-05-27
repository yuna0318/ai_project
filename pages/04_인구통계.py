# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import re

# -----------------------------
# 한글 폰트 설정
# -----------------------------
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding='euc-kr')
    
    # 숫자형 변환
    for col in df.columns[1:]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .astype(int)
        )

    return df

df = load_data()

# -----------------------------
# 자치구 이름 추출
# -----------------------------
districts = []

for value in df['행정구역']:
    match = re.search(r'서울특별시\s(.+?)\s\(', value)
    
    if match:
        districts.append(match.group(1))

district_df = df.iloc[1:].copy()
district_df['자치구'] = districts

# -----------------------------
# 나이 컬럼 추출
# -----------------------------
age_columns = []
ages = []

for col in district_df.columns:
    match = re.search(r'_(\d+)세', col)

    if match:
        age = int(match.group(1))
        age_columns.append(col)
        ages.append(age)

# -----------------------------
# 스트림릿 UI
# -----------------------------
st.title("서울특별시 자치구 연령별 인구 분석")

selected_district = st.selectbox(
    "행정구를 선택하세요",
    district_df['자치구'].tolist()
)

# -----------------------------
# 선택된 구 데이터
# -----------------------------
selected_row = district_df[
    district_df['자치구'] == selected_district
].iloc[0]

population_values = [
    selected_row[col] for col in age_columns
]

# -----------------------------
# 그래프 생성
# -----------------------------
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    ages,
    population_values,
    color='purple',
    linewidth=2.5
)

# 제목 및 축
ax.set_title(
    f"{selected_district} 연령별 인구 분포",
    fontsize=18
)

ax.set_xlabel("나이", fontsize=13)
ax.set_ylabel("인구수", fontsize=13)

# x축 10살 단위
ax.set_xticks(range(0, 101, 10))

# 세로 구분선
ax.grid(
    axis='x',
    linestyle='--',
    alpha=0.5
)

# 그래프 표시
st.pyplot(fig)

# -----------------------------
# 데이터 표
# -----------------------------
chart_df = pd.DataFrame({
    "나이": ages,
    "인구수": population_values
})

st.dataframe(chart_df, use_container_width=True)
