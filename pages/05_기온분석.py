import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# --------------------------
# 페이지 설정
# --------------------------
st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 기온 분석 및 미래 기온 예측")

# --------------------------
# 데이터 불러오기
# --------------------------
def load_data():

    try:
        df = pd.read_csv("seoul.csv", encoding="cp949")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8")

    df.columns = df.columns.str.strip()

    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    df = df.dropna(subset=["날짜"])

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
].copy()

filtered = filtered.sort_values("연도")

# --------------------------
# 미래 연도 선택
# --------------------------
future_year = st.number_input(
    "예측할 미래 연도",
    min_value=int(filtered["연도"].max()) + 1,
    max_value=2100,
    value=2030
)

# --------------------------
# 최고기온 모델
# --------------------------
X = filtered[["연도"]]

high_model = LinearRegression()
high_model.fit(X, filtered["최고기온(℃)"])

pred_high = high_model.predict(
    np.array([[future_year]])
)[0]

# --------------------------
# 최저기온 모델
# --------------------------
low_model = LinearRegression()
low_model.fit(X, filtered["최저기온(℃)"])

pred_low = low_model.predict(
    np.array([[future_year]])
)[0]

# --------------------------
# 그래프
# --------------------------
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    filtered["연도"],
    filtered["최고기온(℃)"],
    color="green",
    linewidth=2,
    label="실제 최고기온"
)

ax.plot(
    filtered["연도"],
    filtered["최저기온(℃)"],
    color="blue",
    linewidth=2,
    label="실제 최저기온"
)

# 예측점 표시
ax.scatter(
    future_year,
    pred_high,
    s=120,
    marker="*",
    label=f"{future_year} 최고기온 예측"
)

ax.scatter(
    future_year,
    pred_low,
    s=120,
    marker="*",
    label=f"{future_year} 최저기온 예측"
)

ax.set_title(
    f"{month}월 {day}일의 연도별 최고·최저기온 및 미래 예측"
)

ax.set_xlabel("연도")
ax.set_ylabel("기온(℃)")
ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)

# --------------------------
# 예측 결과
# --------------------------
st.subheader(f"🔮 {future_year}년 예측 결과")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "예상 최고기온",
        f"{pred_high:.1f}℃"
    )

with col2:
    st.metric(
        "예상 최저기온",
        f"{pred_low:.1f}℃"
    )

# --------------------------
# 데이터 표
# --------------------------
st.subheader("과거 관측 데이터")

st.dataframe(
    filtered[
        ["연도", "최저기온(℃)", "최고기온(℃)"]
    ],
    use_container_width=True
)
