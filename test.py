import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="나만의 북마크 지도", layout="wide")
st.title("📍 나만의 북마크 지도 만들기")

if "places" not in st.session_state:
    st.session_state["places"] = []

# 입력 폼
with st.form("add_place"):
    name = st.text_input("장소 이름")
    lat = st.number_input("위도", format="%.6f")
    lon = st.number_input("경도", format="%.6f")
    description = st.text_area("설명")
    submitted = st.form_submit_button("추가")
    if submitted and name:
        st.session_state.places.append({
            "name": name,
            "lat": lat,
            "lon": lon,
            "description": description
        })
        st.success(f"{name} 추가됨!")

# 지도 중심 설정
if st.session_state.places:
    avg_lat = sum(p["lat"] for p in st.session_state.places) / len(st.session_state.places)
    avg_lon = sum(p["lon"] for p in st.session_state.places) / len(st.session_state.places)
    center = [avg_lat, avg_lon]
else:
    center = [37.5665, 126.9780]  # 서울

m = folium.Map(location=center, zoom_start=12)

# 기존 마커들
for p in st.session_state.places:
    folium.Marker(
        location=[p["lat"], p["lon"]],
        popup=f"<b>{p['name']}</b><br>{p['description']}",
        tooltip=p["name"]
    ).add_to(m)

# 지도 출력 및 클릭 이벤트 감지
st.subheader("🗺️ 내 북마크 지도")
map_data = st_folium(m, width=900, height=600, returned_objects=["last_clicked"])

# 사용자가 지도 클릭 시 위치 출력
if map_data and map_data["last_clicked"]:
    clicked = map_data["last_clicked"]
    st.info(f"🧭 클릭한 위치의 좌표: 위도={clicked['lat']:.6f}, 경도={clicked['lng']:.6f}")

# 장소 목록 출력
if st.session_state.places:
    st.subheader("📋 북마크 목록")
    df = pd.DataFrame(st.session_state.places)
    st.dataframe(df)

# 초기화 버튼
if st.button("🗑️ 모든 장소 삭제"):
    st.session_state.places = []
    st.success("모든 장소가 삭제되었습니다.")
