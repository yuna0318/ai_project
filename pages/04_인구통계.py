# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import re

# -----------------------------------
# 한글 폰트 완벽 설정
# -----------------------------------
system_name = platform.system()

if system_name == 'Windows':
    plt.rc('font', family='Malgun Gothic')

elif system_name == 'Darwin':
    plt.rc('font', family='AppleGothic')

else:
    # Streamlit Cloud (Linux)
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="서울 인구 분석",
    layout="wide"
)

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv(
        "population.csv",
        encoding="euc-kr"
    )

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

# -----------------------------------
# 자치구 이름 추출
# -----------------------------------
district_df = df.iloc[1:].copy()

districts = []

for value in district_df['행정구역']:

    match = re.search(
        r'서울특별시\s(.+?)\s\(',
        value
    )

    if match:
        districts.append(match.group(1))

district_df['자치구'] = districts

# -----------------------------------
# 나이 컬럼 추출
# -----------------------------------
age_columns = []
ages = []

for col in district_df.columns:

    # 0세 ~ 99세
    match = re.search(r'_(\d+)세', col)

    if match:

        age = int(match.group(1))

        age_columns.append(col)
        ages.append(age)

# -----------------------------------
# 제목
# -----------------------------------
st.title("서울특별시 자치구 연령별 인구 분석")

st.markdown("---")

# -----------------------------------
# 자치구 선택
# -----------------------------------
selected_district = st.selectbox(
    "행정구를 선택하세요",
    district_df['자치구'].tolist()
)

# -----------------------------------
# 선택된 자치구 데이터
# -----------------------------------
selected_row = district_df[
    district_df['자치구'] == selected_district
].iloc[0]

population_values = []

for col in age_columns:
    population_values.append(selected_row[col])

# -----------------------------------
# 그래프 생성
# -----------------------------------
fig, ax = plt.subplots(figsize=(16, 7))

# 보라색 꺾은선 그래프
ax.plot(
    ages,
    population_values,
    color="#7B2CBF",
    linewidth=3
)

# 그래프 제목
ax.set_title(
    f"{selected_district} 연령별 인구 분포",
    fontsize=20,
    pad=20
)

# 축 이름
ax.set_xlabel(
    "나이",
    fontsize=14
)

ax.set_ylabel(
    "인구수",
    fontsize=14
)

# -----------------------------------
# x축 설정 (10살 단위)
# -----------------------------------
ax.set_xticks(range(0, 101, 10))

# 세로 구분선
ax.grid(
    axis='x',
    linestyle='--',
    alpha=0.5
)

# 전체 그리드
ax.grid(
    True,
    linestyle=':',
    alpha=0.3
)

# 여백 자동 조절
plt.tight_layout()

# -----------------------------------
# 그래프 출력
# -----------------------------------
st.pyplot(fig)

# -----------------------------------
# 데이터 표 출력
# -----------------------------------
st.markdown("### 연령별 데이터")

chart_df = pd.DataFrame({
    "나이": ages,
    "인구수": population_values
})

st.dataframe(
    chart_df,
    use_container_width=True
)


