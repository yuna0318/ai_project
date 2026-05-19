import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 외국인 인기 관광지 TOP10",
    layout="wide"
)

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.markdown("Folium 지도를 사용해 서울의 인기 관광지를 표시했습니다.")

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]

# Folium 지도 생성
m = folium.Map(
    location=seoul_center,
    zoom_start=11,
    tiles="CartoDB positron"
)

# 관광지 데이터
places = [
    {
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 왕조의 대표 궁궐"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "전통 한옥이 모여 있는 관광 명소"
    },
    {
        "name": "명동",
        "lat": 37.5636,
        "lon": 126.9827,
        "desc": "쇼핑과 길거리 음식의 중심지"
    },
    {
        "name": "N서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울 야경 명소"
    },
    {
        "name": "홍대거리",
        "lat": 37.5563,
        "lon": 126.9236,
        "desc": "젊은 문화와 버스킹의 거리"
    },
    {
        "name": "인사동",
        "lat": 37.5740,
        "lon": 126.9850,
        "desc": "전통 문화와 공예품 거리"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.5131,
        "lon": 127.1025,
        "desc": "서울 대표 초고층 랜드마크"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.5665,
        "lon": 127.0092,
        "desc": "현대적인 건축과 패션 중심지"
    },
    {
        "name": "한강공원",
        "lat": 37.5283,
        "lon": 126.9327,
        "desc": "서울 시민과 관광객의 휴식 공간"
    },
    {
        "name": "광장시장",
        "lat": 37.5704,
        "lon": 126.9997,
        "desc": "한국 전통 먹거리 시장"
    }
]

# 마커 추가
for place in places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"""
        <b>{place['name']}</b><br>
        {place['desc']}
        """,
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# Streamlit에 지도 출력
st_folium(m, width=1200, height=700)

st.markdown("---")
st.caption("Built with Streamlit + Folium")
