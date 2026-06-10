import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# 페이지 설정
# ======================

st.set_page_config(
    page_title="Spotify Music Analytics",
    page_icon="🎵",
    layout="wide"
)

# ======================
# CSS
# ======================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1,h2,h3 {
    color: white;
}

.stMetric {
    background-color: #1DB95420;
    padding: 10px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# 데이터 불러오기
# ======================

@st.cache_data
def load_data():
    return pd.read_csv("songs_normalize.csv")

df = load_data()

# ======================
# 사이드바
# ======================

st.sidebar.title("🎵 Spotify Dashboard")

menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "🏠 홈",
        "📈 데이터 개요",
        "🎤 아티스트 분석",
        "🎼 장르 분석",
        "🔥 인기곡 분석",
        "📅 연도별 트렌드",
        "🎧 오디오 특성",
        "📊 상관관계 분석",
        "🌳 트리맵 분석"
    ]
)

# ======================
# 홈
# ======================

if menu == "🏠 홈":

    st.title("🎵 Spotify Music Analytics Dashboard")

    st.markdown("""
    ### 🎧 음악 데이터로 보는 트렌드 분석

    Spotify 인기곡 데이터를 활용하여

    - 🎤 인기 아티스트
    - 🎼 장르 분포
    - 🔥 인기곡 TOP 25
    - 📅 연도별 트렌드
    - 🎧 오디오 특성
    - 📊 상관관계 분석

    을 시각화한 프로젝트입니다.
    """)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🎵 총 곡 수", f"{len(df):,}")
    c2.metric("🎤 아티스트 수", f"{df['artist'].nunique():,}")
    c3.metric("🎼 장르 수", f"{df['genre'].nunique():,}")
    c4.metric("📅 기간", f"{df['year'].min()}~{df['year'].max()}")

# ======================
# 데이터 개요
# ======================

elif menu == "📈 데이터 개요":

    st.title("📈 데이터 개요")

    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("결측치 확인")

    missing = pd.DataFrame(
        df.isnull().sum(),
        columns=["결측치"]
    )

    st.dataframe(missing)

# ======================
# 아티스트 분석
# ======================

elif menu == "🎤 아티스트 분석":

    st.title("🎤 TOP 20 아티스트")

    artist_df = (
        df.groupby("artist")
        .size()
        .reset_index(name="곡 수")
        .sort_values("곡 수", ascending=False)
        .head(20)
    )

    fig = px.bar(
        artist_df,
        x="곡 수",
        y="artist",
        orientation="h",
        color="곡 수"
    )

    fig.update_layout(height=700)

    st.plotly_chart(fig, use_container_width=True)

# ======================
# 장르 분석
# ======================

elif menu == "🎼 장르 분석":

    st.title("🎼 TOP 15 장르")

    genre_df = (
        df.groupby("genre")
        .size()
        .reset_index(name="곡 수")
        .sort_values("곡 수", ascending=False)
        .head(15)
    )

    fig = px.bar(
        genre_df,
        x="genre",
        y="곡 수",
        color="곡 수"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# 인기곡 분석
# ======================

elif menu == "🔥 인기곡 분석":

    st.title("🔥 인기곡 TOP 25")

    top_song = (
        df.sort_values("popularity", ascending=False)
        .head(25)
    )

    fig = px.bar(
        top_song,
        x="popularity",
        y="song",
        color="popularity",
        hover_data=["artist"]
    )

    fig.update_layout(height=800)

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        top_song[
            ["song", "artist", "popularity", "year"]
        ],
        use_container_width=True
    )

# ======================
# 연도별 트렌드
# ======================

elif menu == "📅 연도별 트렌드":

    st.title("📅 연도별 음악 수")

    year_df = (
        df.groupby("year")
        .size()
        .reset_index(name="곡 수")
    )

    fig = px.area(
        year_df,
        x="year",
        y="곡 수",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# 오디오 특성
# ======================

elif menu == "🎧 오디오 특성":

    st.title("🎧 오디오 특성 분석")

    feature = st.selectbox(
        "특성 선택",
        [
            "danceability",
            "energy",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo"
        ]
    )

    fig = px.histogram(
        df,
        x=feature,
        nbins=30
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# 상관관계
# ======================

elif menu == "📊 상관관계 분석":

    st.title("📊 상관관계 분석")

    numeric_df = df.select_dtypes(include="number")

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================
# 트리맵
# ======================

elif menu == "🌳 트리맵 분석":

    st.title("🌳 장르별 인기 트리맵")

    tree_df = (
        df.groupby("genre")["popularity"]
        .mean()
        .reset_index()
        .sort_values("popularity", ascending=False)
        .head(25)
    )

    fig = px.treemap(
        tree_df,
        path=["genre"],
        values="popularity",
        color="popularity"
    )

    st.plotly_chart(fig, use_container_width=True)
