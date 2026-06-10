import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------
# 페이지 설정
# --------------------

st.set_page_config(
    page_title="Spotify Music Trend Analysis",
    page_icon="🎵",
    layout="wide"
)

# --------------------
# 스타일
# --------------------

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
}

h1,h2,h3 {
    color:white;
}

.metric-box{
    background:linear-gradient(135deg,#1DB954,#7B2CBF);
    padding:15px;
    border-radius:15px;
    text-align:center;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# --------------------
# 데이터 로드
# --------------------

@st.cache_data
def load_data():

    possible_paths = [
        Path("songs_normalize.csv"),
        Path("data/songs_normalize.csv"),
        Path(__file__).resolve().parent.parent / "songs_normalize.csv",
        Path(__file__).resolve().parent.parent / "data" / "songs_normalize.csv",
    ]

    for path in possible_paths:
        if path.exists():
            return pd.read_csv(path)

    st.error("❌ songs_normalize.csv 파일을 찾을 수 없습니다.")
    st.stop()

df = load_data()

# --------------------
# 제목
# --------------------

st.title("🎵 Spotify 음악 트렌드 분석")
st.caption("2000 ~ 2019 Spotify 인기 음악 데이터 분석")

# --------------------
# 연도 선택
# --------------------

selected_year = st.selectbox(
    "📅 분석할 연도를 선택하세요",
    sorted(df["year"].unique())
)

year_df = df[df["year"] == selected_year]

# --------------------
# KPI
# --------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "🎵 총 곡 수",
    len(year_df)
)

c2.metric(
    "🎤 아티스트 수",
    year_df["artist"].nunique()
)

c3.metric(
    "🎼 장르 수",
    year_df["genre"].nunique()
)

c4.metric(
    "🔥 평균 인기",
    round(year_df["popularity"].mean(),1)
)

st.divider()

# --------------------
# 인기 장르
# --------------------

st.subheader(f"🎼 {selected_year} 인기 장르 TOP 10")

genre_top = (
    year_df.groupby("genre")
    .size()
    .reset_index(name="곡 수")
    .sort_values("곡 수", ascending=False)
    .head(10)
)

fig = px.bar(
    genre_top,
    x="genre",
    y="곡 수",
    color="곡 수",
    color_continuous_scale=["#7B2CBF","#1DB954"]
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 인기 아티스트
# --------------------

st.subheader(f"🎤 {selected_year} 인기 아티스트 TOP 10")

artist_top = (
    year_df.groupby("artist")
    .size()
    .reset_index(name="곡 수")
    .sort_values("곡 수", ascending=False)
    .head(10)
)

fig = px.bar(
    artist_top,
    y="artist",
    x="곡 수",
    orientation="h",
    color="곡 수",
    color_continuous_scale=["#7B2CBF","#1DB954"]
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 인기곡
# --------------------

st.subheader(f"🔥 {selected_year} 인기곡 TOP 10")

top_song = (
    year_df
    .sort_values("popularity", ascending=False)
    .head(10)
)

st.dataframe(
    top_song[
        ["song","artist","genre","popularity"]
    ],
    use_container_width=True
)

# --------------------
# 음악 특징
# --------------------

st.subheader("🎧 음악 특징 분석")

feature_df = pd.DataFrame({
    "특성":[
        "danceability",
        "energy",
        "acousticness",
        "valence"
    ],
    "값":[
        year_df["danceability"].mean(),
        year_df["energy"].mean(),
        year_df["acousticness"].mean(),
        year_df["valence"].mean()
    ]
})

fig = px.bar(
    feature_df,
    x="특성",
    y="값",
    color="값",
    color_continuous_scale=["#7B2CBF","#1DB954"]
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 장르 변화
# --------------------

st.subheader("📈 2000~2019 인기 장르 변화")

genre_year = (
    df.groupby(["year","genre"])
    .size()
    .reset_index(name="count")
)

top_genres = (
    df["genre"]
    .value_counts()
    .head(5)
    .index
)

genre_year = genre_year[
    genre_year["genre"].isin(top_genres)
]

fig = px.line(
    genre_year,
    x="year",
    y="count",
    color="genre",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 자동 트렌드 해설
# --------------------

top_genre = genre_top.iloc[0]["genre"]

top_artist = artist_top.iloc[0]["artist"]

st.success(
f"""
🎵 {selected_year}년 음악 트렌드 분석

🎼 가장 인기 있었던 장르 : {top_genre}

🎤 가장 활발했던 아티스트 : {top_artist}

📊 총 {len(year_df)}곡이 데이터에 포함되어 있습니다.

이 시기 음악의 특징은 Danceability와 Energy를 기반으로
분석할 수 있으며 당시의 음악 시장 흐름을 확인할 수 있습니다.
"""
)
