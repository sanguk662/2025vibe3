import streamlit as st
import pandas as pd
import plotly.express as px

# ▒▒ Streamlit 설정 ▒▒
st.set_page_config(page_title="세계 GDP 시각화", layout="wide")
st.title("🌍 세계 GDP 데이터 시각화 (2010–2023)")
st.markdown("주요 10개국과 한국의 GDP, 인구, 1인당 GDP 데이터를 시각화한 프로젝트입니다.")

# ▒▒ 1. CSV 데이터 불러오기 ▒▒
df = pd.read_csv("world_gdp_extended.csv")  # Streamlit Cloud에서는 파일 경로 조정 필요할 수 있음
df_2023 = df[df["Year"] == 2023]

# ▒▒ 2. 국가 필터 (멀티 셀렉트) ▒▒
all_countries = df["Country"].unique().tolist()
selected_countries = st.multiselect("🔍 비교할 국가를 선택하세요", all_countries, default=all_countries)
filtered_df = df[df["Country"].isin(selected_countries)]
filtered_df_2023 = df_2023[df_2023["Country"].isin(selected_countries)]

# ▒▒ 3. 선 그래프 - 명목 GDP 추이 ▒▒
st.subheader("📈 명목 GDP 추이 (조 달러)")
fig1 = px.line(filtered_df, x='Year', y='GDP_USD_trillions', color='Country',
               markers=True, title="국가별 명목 GDP 변화")
fig1.update_layout(yaxis_title="GDP (US$ Trillion)", xaxis_title="연도")
st.plotly_chart(fig1, use_container_width=True)

# ▒▒ 4. 막대 그래프 - 1인당 GDP (2023년) ▒▒
st.subheader("💰 2023년 1인당 GDP 비교")
fig2 = px.bar(filtered_df_2023, x='Country', y='GDP_per_capita_USD',
              text='GDP_per_capita_USD', title="1인당 GDP (US$)")
fig2.update_layout(yaxis_title="1인당 GDP (US$)", xaxis_title="국가")
st.plotly_chart(fig2, use_container_width=True)

# ▒▒ 5. 버블 차트 - 인구 vs GDP (2023년) ▒▒
st.subheader("📊 인구 대비 GDP (버블 크기: 1인당 GDP)")
fig3 = px.scatter(filtered_df_2023, x="Population_millions", y="GDP_USD_trillions",
                  size="GDP_per_capita_USD", color="Country",
                  hover_name="Country", size_max=60,
                  title="인구 vs 명목 GDP (2023년 기준)")
fig3.update_layout(xaxis_title="인구 (백만 명)", yaxis_title="GDP (조 달러)")
st.plotly_chart(fig3, use_container_width=True)

# ▒▒ 6. 원본 데이터 테이블 ▒▒
with st.expander("📄 전체 원본 데이터 보기"):
    st.dataframe(df.sort_values(["Year", "Country"]))
