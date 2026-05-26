# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="국가별 MBTI 분석",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 국가별 MBTI 분석 대시보드")

# -----------------------------
# 데이터 불러오기
# -----------------------------
df = pd.read_csv("countriesMBTI_16types.csv")

# 국가 컬럼
country_col = df.columns[0]

# MBTI 컬럼
mbti_cols = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# -----------------------------
# 퍼센트 변환 함수
# -----------------------------
def convert_percent(values):
    values = values.astype(float)

    if values.max() <= 1:
        values = values * 100

    return values

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.title("메뉴")

menu = st.sidebar.radio(
    "분석 선택",
    [
        "국가별 MBTI 분석",
        "MBTI별 국가 순위"
    ]
)

# =========================================================
# 1. 국가별 MBTI 분석
# =========================================================
if menu == "국가별 MBTI 분석":

    st.header("🌎 국가별 MBTI 비율")

    country = st.selectbox(
        "국가 선택",
        sorted(df[country_col].unique())
    )

    # 선택 국가 데이터
    country_data = df[df[country_col] == country].iloc[0]

    # MBTI 데이터
    values = convert_percent(country_data[mbti_cols].values)

    mbti_df = pd.DataFrame({
        "MBTI": mbti_cols,
        "비율": values
    })

    # 높은 순 정렬
    mbti_df = mbti_df.sort_values(
        by="비율",
        ascending=False
    ).reset_index(drop=True)

    # 최고값 index
    max_idx = 0

    # 초록색 그라데이션
    colors = plt.cm.Greens(
        np.linspace(0.35, 0.9, len(mbti_df))
    )

    # 1등 진한 초록
    colors[max_idx] = [0.0, 0.45, 0.0, 1]

    # 그래프
    fig, ax = plt.subplots(figsize=(14, 7))

    bars = ax.bar(
        mbti_df["MBTI"],
        mbti_df["비율"],
        color=colors,
        edgecolor="white",
        linewidth=1.5
    )

    # 값 표시
    for bar in bars:
        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.3,
            f"{height:.1f}%",
            ha='center',
            fontsize=10
        )

    # 스타일
    ax.set_title(
        f"{country} MBTI 비율 순위",
        fontsize=20,
        weight="bold"
    )

    ax.set_ylabel("비율 (%)")
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    st.pyplot(fig)

    # TOP MBTI
    top_mbti = mbti_df.iloc[0]["MBTI"]
    top_value = mbti_df.iloc[0]["비율"]

    st.success(
        f"🏆 {country}의 가장 높은 MBTI는 "
        f"{top_mbti} ({top_value:.2f}%) 입니다."
    )

# =========================================================
# 2. MBTI별 국가 순위
# =========================================================
elif menu == "MBTI별 국가 순위":

    st.header("🏆 MBTI별 국가 TOP 10")

    selected_mbti = st.selectbox(
        "MBTI 선택",
        mbti_cols
    )

    # 데이터 준비
    rank_df = df[[country_col, selected_mbti]].copy()

    # 퍼센트 변환
    rank_df[selected_mbti] = convert_percent(
        rank_df[selected_mbti].values
    )

    # 정렬
    rank_df = rank_df.sort_values(
        by=selected_mbti,
        ascending=False
    ).head(10)

    # 색상
    colors = plt.cm.Greens(
        np.linspace(0.35, 0.9, len(rank_df))
    )

    # 1등 강조
    colors[0] = [0.0, 0.45, 0.0, 1]

    # 그래프
    fig, ax = plt.subplots(figsize=(14, 7))

    bars = ax.bar(
        rank_df[country_col],
        rank_df[selected_mbti],
        color=colors,
        edgecolor="white",
        linewidth=1.5
    )

    # 값 표시
    for bar in bars:
        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.3,
            f"{height:.1f}%",
            ha='center',
            fontsize=10
        )

    # 스타일
    ax.set_title(
        f"{selected_mbti} 비율이 높은 국가 TOP 10",
        fontsize=20,
        weight="bold"
    )

    ax.set_ylabel("비율 (%)")
    plt.xticks(rotation=20)

    ax.grid(axis='y', linestyle='--', alpha=0.3)

    st.pyplot(fig)

    # 표 출력
    st.subheader("📋 국가 순위")

    rank_df.columns = ["국가", "비율 (%)"]

    rank_df.index = rank_df.index + 1

    st.dataframe(
        rank_df,
        use_container_width=True
    )
