import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("서울시 연령별 인구 분포 (2025년 6월 기준)")
st.markdown("서울특별시의 나이별 인구 수를 바 차트로 시각화합니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("202506_202506_연령별인구현황_월간.csv", encoding="cp949")
    df_seoul = df[df["행정구역"].str.contains("서울특별시  \(1100000000\)")]
    df_seoul = df_seoul.drop(columns=["행정구역", "2025년06월_계_총인구수", "2025년06월_계_연령구간인구수"])
    df_seoul = df_seoul.applymap(lambda x: int(str(x).replace(",", "")))
    df_seoul.columns = [col.split("_")[-1].replace("세", "").replace("이상", "100+") for col in df_seoul.columns]
    df_seoul = df_seoul.T.reset_index()
    df_seoul.columns = ["연령", "인구수"]
    df_seoul["연령"] = df_seoul["연령"].replace("100 100+", "100")
    df_seoul["연령"] = df_seoul["연령"].astype(int)
    df_seoul = df_seoul.sort_values("연령")
    return df_seoul

df_seoul = load_data()

# 시각화
fig = px.bar(df_seoul, x="연령", y="인구수",
             title="서울특별시 연령별 인구 분포",
             labels={"연령": "나이", "인구수": "인구 수"},
             height=600)

fig.update_layout(xaxis=dict(dtick=5))

# 차트 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블도 보기
with st.expander("📊 원본 데이터 보기"):
    st.dataframe(df_seoul, use_container_width=True)
