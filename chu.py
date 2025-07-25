import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("서울특별시 연령별 인구 시각화 (2025년 6월 기준)")
st.markdown("전체 인구와 남녀 성별 인구를 연령별로 시각화합니다.")

@st.cache_data
def load_data():
    df_all = pd.read_csv("202506_202506_연령별인구현황_월간.csv", encoding="cp949")
    df_gender = pd.read_csv("202506_202506_연령별인구현황_월간지형이수학2등급.csv", encoding="cp949")

    df_all_seoul = df_all[df_all["행정구역"].str.contains("서울특별시  \(1100000000\)")]
    df_gender_seoul = df_gender[df_gender["행정구역"].str.contains("서울특별시  \(1100000000\)")]

    df_all_seoul = df_all_seoul.drop(columns=["행정구역", "2025년06월_계_총인구수", "2025년06월_계_연령구간인구수"])
    df_gender_seoul = df_gender_seoul.drop(columns=["행정구역", "2025년06월_남_총인구수", "2025년06월_남_연령구간인구수"])

    df_all_seoul = df_all_seoul.applymap(lambda x: int(str(x).replace(",", "")))
    df_gender_seoul = df_gender_seoul.applymap(lambda x: int(str(x).replace(",", "")))

    df_all_seoul.columns = [col.split("_")[-1].replace("세", "").replace("이상", "100+") for col in df_all_seoul.columns]
    df_all_seoul = df_all_seoul.T.reset_index()
    df_all_seoul.columns = ["연령", "전체인구"]
    df_all_seoul["연령"] = df_all_seoul["연령"].replace("100 100+", "100").astype(int)
    df_all_seoul = df_all_seoul.sort_values("연령")

    male_cols = [col for col in df_gender_seoul.columns if "_남_" in col]
    female_cols = [col for col in df_gender_seoul.columns if "_여_" in col]

    df_male = df_gender_seoul[male_cols].T.reset_index()
    df_female = df_gender_seoul[female_cols].T.reset_index()

    df_male.columns = ["연령", "남자"]
    df_female.columns = ["연령", "여자"]

    df_male["연령"] = df_male["연령"].apply(lambda x: x.split("_")[-1].replace("세", "").replace("이상", "100+"))
    df_female["연령"] = df_female["연령"].apply(lambda x: x.split("_")[-1].replace("세", "").replace("이상", "100+"))

    df_gender_combined = pd.merge(df_male, df_female, on="연령")
    df_gender_combined["연령"] = df_gender_combined["연령"].replace("100 100+", "100").astype(int)
    df_gender_combined = df_gender_combined.sort_values("연령")

    return df_all_seoul, df_gender_combined

df_all, df_gender = load_data()

# 전체 인구 바 차트
fig1 = px.bar(df_all, x="연령", y="전체인구",
              title="서울특별시 연령별 전체 인구",
              labels={"연령": "나이", "전체인구": "인구 수"},
              height=500)
fig1.update_layout(xaxis=dict(dtick=5))
st.plotly_chart(fig1, use_container_width=True)

# 남녀 인구 라인 차트
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_gender["연령"], y=df_gender["남자"], mode='lines+markers', name="남자"))
fig2.add_trace(go.Scatter(x=df_gender["연령"], y=df_gender["여자"], mode='lines+markers', name="여자"))
fig2.update_layout(title="서울특별시 연령별 남녀 인구 분포",
                   xaxis_title="나이", yaxis_title="인구 수")
st.plotly_chart(fig2, use_container_width=True)

# 데이터 보기
with st.expander("📊 전체 원본 데이터 보기"):
    st.subheader("전체 인구 데이터")
    st.dataframe(df_all)
    st.subheader("남녀 인구 데이터")
    st.dataframe(df_gender)
