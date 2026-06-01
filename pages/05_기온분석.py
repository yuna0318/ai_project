import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------
# 페이지 설정
# --------------------------
st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 연도별 기온 분석")

# --------------------------
# 데이터 불러오기
# --------------------------
def load_data():

    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 오류 제거
    df = df.dropna(subset=["날짜"])

    # 연도, 월, 일 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# --------------------------
# 월 선택
# --------------------------
month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

# --------------------------
# 일 선택
# --------------------------
days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    days
)

# --------------------------
# 데이터 필터링
# --------------------------
filtered = df[
    (df["월"] == month)
    & (df["일"] == day)
].sort_values("연도")

# --------------------------
# 그래프
# --------------------------
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    filtered["연도"],
    filtered["최고기온(℃)"],
    color="green",
    linewidth=2,
    label="최고기온"
)

ax.plot(
    filtered["연도"],
    filtered["최저기온(℃)"],
    color="blue",
    linewidth=2,
    label="최저기온"
)

ax.set_title(
    f"{month}월 {day}일의 연도별 최고·최저기온"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")

ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)

# --------------------------
# 데이터 표
# --------------------------
st.subheader("데이터")

st.dataframe(
    filtered[
        ["연도", "최저기온(℃)", "최고기온(℃)"]
    ],
    use_container_width=True
)
