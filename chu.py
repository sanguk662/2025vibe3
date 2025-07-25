import pandas as pd
import plotly.express as px
import plotly.io as pio

# ▶️ 1. 데이터 정의
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

# ▶️ 3. 현재 디렉토리에 CSV 저장
csv_path = "world_gdp_2010_2023_sample.csv"
df.to_csv(csv_path, index=False)
print(f"✅ CSV 저장 완료: {csv_path}")

# ▶️ 4. Plotly 시각화

# ① 명목 GDP 추이 (선 그래프)
fig1 = px.line(df, x='Year', y='GDP_USD_trillions', color='Country',
               title='🌍 국가별 명목 GDP 추이 (조 달러)', markers=True)
fig1.update_layout(yaxis_title="GDP (US$ Trillion)", xaxis_title="연도")
pio.write_html(fig1, file="plot_gdp_line.html", auto_open=False)

# ② 2023년 1인당 GDP (막대 그래프)
df_2023 = df[df["Year"] == 2023]
fig2 = px.bar(df_2023, x='Country', y='GDP_per_capita_USD',
              title='💰 2023년 1인당 GDP 비교 (USD)', text='GDP_per_capita_USD')
fig2.update_layout(yaxis_title="1인당 GDP (US$)", xaxis_title="국가")
pio.write_html(fig2, file="plot_gdp_per_capita_bar.html", auto_open=False)

# ③ 2023년 인구 vs GDP 버블 차트
fig3 = px.scatter(df_2023, x="Population_millions", y="GDP_USD_trillions",
                  size="GDP_per_capita_USD", color="Country",
                  hover_name="Country", size_max=60,
                  title="📊 GDP vs 인구 (버블 크기: 1인당 GDP)")
fig3.update_layout(xaxis_title="인구 (백만)", yaxis_title="GDP (조 달러)")
pio.write_html(fig3, file="plot_gdp_population_bubble.html", auto_open=False)

print("✅ Plotly 시각화 3개 HTML 저장 완료")
