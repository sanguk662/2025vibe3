import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도 만들기")
st.write("원하는 장소를 북마크로 지도에 추가해보세요!")

# 세션 상태에 장소 저장
if 'places' not in st.session_state:
    st.session_state['places'] = []

# 폼을 통해 장소 입력
with st.form("add_place_form"):
    st.subheader("➕ 장소 추가하기")
    name = st.text_input("장소 이름", placeholder="예: 집, 학교, 맛집")
    lat = st.number_input("위도", format="%.6f")
    lon = st.number_input("경도", format="%.6f")
    description = st.text_area("설명", placeholder="장소에 대한 설명을 적어보세요.")

    submitted = st.form_submit_button("장소 추가")
    if submitted:
        if name and lat and lon:
            st.session_state.places.append({
                "name": name,
                "lat": lat,
                "lon": lon,
                "description": description
            })
            st.success(f"✅ '{name}' 장소가 지도에 추가되었습니다!")
        else:
            st.warning("장소 이름과 위도/경도는 반드시 입력해야 합니다.")

# 지도 중심 위치 설정
if st.session_state.places:
    avg_lat = sum(p['lat'] for p in st.session_state.places) / len(st.session_state.places)
    avg_lon = sum(p['lon'] for p in st.session_state.places) / len(st.session_state.places)
else:
    # 기본 중심: 서울
    avg_lat, avg_lon = 37.5665, 126.9780

# folium 지도 생성
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# 마커 추가
for p in st.session_state.places:
    folium.Marker(
        [p["lat"], p["lon"]],
        popup=f"<b>{p['name']}</b><br>{p['description']}",
        tooltip=p["name"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st.subheader("🗺️ 내 북마크 지도")
st_data = st_folium(m, width=1000, height=600)

# 북마크 목록 출력
if st.session_state.places:
    st.subheader("📋 북마크 목록")
    df = pd.DataFrame(st.session_state.places)
    st.dataframe(df, use_container_width=True)

# 초기화 버튼
if st.button("🗑️ 모든 북마크 삭제"):
    st.session_state.places = []
    st.success("모든 북마크가 삭제되었습니다.")
