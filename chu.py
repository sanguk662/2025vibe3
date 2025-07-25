import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="세계 GDP 시각화", layout="wide")

# ▶️ 1. 기본 데이터 (2010~2023 일부)
data = {
    "Country": [
        "USA", "USA", "USA",
        "China", "China",
        "Japan", "Germany", "UK", "France", "India",
        "Brazil", "Italy", "Canada", "South_Korea"
    ],
    "Year": [
        2010, 2011, 2023,
        2010, 2023,
        2010, 2010, 2010, 2010, 2010,
        2010, 2010, 2010, 2010
    ],
    "GDP_USD_trillions": [
        14.96, 15.52, 27.94,
        6.04, 17.50,
        5.70, 3.41, 2.21, 2.58, 1.70,
        2.20, 2.06, 1.60, 1.12
    ],
    "Population_millions": [
        309, 311, 334,
        1341, 1444,
        128, 82, 62, 63, 1230,
        195, 60, 34, 50
    ],
    "GDP_per_capita_USD": [
        48430, 49890, 83600,
        4500, 12120,
        44530, 41610, 35650, 40950, 1380,
        11280, 34350, 47100, 22400
    ]
}

# ▶️ 2. DataFrame 생성
df = pd.DataFrame(data)

# ▶️ 3. 누락 국가 2023년 데이터 추가
new_rows = [
    {"Country": "Japan", "Year": 2023, "GDP_USD_trillions": 4.2, "Population_millions": 125, "GDP_per_capita_USD": 33600},
    {"Country": "Germany", "Year": 2023, "GDP_USD_trillions": 4.5, "Population_millions": 83, "GDP_per_capita_USD": 54000},
    {"Country": "UK", "Year": 2023, "GDP_USD_trillions": 3.5, "Population_millions": 67, "GDP_per_capita_USD": 52200},
    {"Country": "France", "Year": 2023, "GDP_USD_trillions": 3.1, "Population_millions": 65, "GDP_per_capita_USD": 47600},
    {"Country": "India", "Year": 2023, "GDP_USD_trillions": 3.7, "Population_millions": 1400, "GDP_per_capita_USD": 2640},
    {"Country": "Brazil", "Year": 2023, "GDP_USD_trillions": 2.1, "Population_millions": 214, "GDP_per_capita_USD": 9800},
    {"Country": "Italy", "Year": 2023, "GDP_USD_trillions": 2.5, "Population_millions": 59, "GDP_per_capita_USD": 42600},
    {"Country": "Canada", "Year": 2023, "GDP_USD_trillions": 2.2, "Population_millions": 39, "GDP_per_capita_USD": 56000},
    {"Country": "South_Korea", "Year": 2023, "GDP_USD_trillions": 1.7, "Population_millions": 52, "GDP_per_capita_USD": 32800},
]

df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

# ▶️ 4. 2023년 데이터 추출
df_2023 = df[df["Year"] == 2023]

# ─────────────────────────────────────────────

# ▶️ 5. 제목 & 설명
st.title("🌍 세계 GDP 데이터 시각화 (2010–2023)")
st.markdown("주요 10개국 + 한국의 GDP, 인구, 1인당 GDP 데이터를 Plotly로 시각화합니다.")

# ▶️ 6. 명목 GDP 추이 (선 그래프)
st.subheader("📈 국가별 명목 GDP 추이 (조 달러)")
fig1 = px.line(df, x='Year', y='GDP_USD_trillions', color='Country',
               markers=True, title="명목 GDP 변화 추이")
fig1.update_layout(yaxis_title="GDP (US$ Trillion)", xaxis_title="연도")
st.plotly_chart(fig1, use_container_width=True)

# ▶️ 7. 2023년 1인당 GDP 비교 (막대 그래프)
st.subheader("💵 2023년 1인당 GDP 비교")
fig2 = px.bar(df_2023, x='Country', y='GDP_per_capita_USD',
              text='GDP_per_capita_USD', title="2023년 1인당 GDP (달러 기준)")
fig2.update_layout(yaxis_title="1인당 GDP (US$)", xaxis_title="국가")
st.plotly_chart(fig2, use_container_width=True)

# ▶️ 8. 인구 vs GDP 버블 차트 (2023년)
st.subheader("📊 인구 대비 GDP (버블 크기: 1인당 GDP)")
fig3 = px.scatter(df_2023, x="Population_millions", y="GDP_USD_trillions",
                  size="GDP_per_capita_USD", color="Country",
                  hover_name="Country", size_max=60,
                  title="인구 vs 명목 GDP (2023년 기준)")
fig3.update_layout(xaxis_title="인구 (백만 명)", yaxis_title="GDP (조 달러)")
st.plotly_chart(fig3, use_container_width=True)

# ▶️ 9. 데이터 테이블 보기
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df.sort_values(["Year", "Country"]))
