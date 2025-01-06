import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app.logging_config import LoggedSession


def display_seasonal_profiles(city_data, city):
    st.subheader("Сезонные профили температуры")
    seasonal_data = city_data.groupby("season")["temperature"].agg(["mean", "std"]).reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=seasonal_data["season"],
            y=seasonal_data["mean"],
            error_y=dict(type="data", array=seasonal_data["std"], visible=True),
            name="Средняя температура",
        )
    )
    fig.update_layout(
        title=f"Сезонные профили температуры в городе {city}",
        xaxis_title="Сезон",
        yaxis_title="Средняя температура (°C)",
    )
    st.plotly_chart(fig, use_container_width=True, key="seasonal_profiles")


def display_temperature_trends(city_data):
    st.subheader("Тренды температуры")
    city_data["year"] = pd.to_datetime(city_data["timestamp"]).dt.year
    yearly_trend = city_data.groupby("year")["temperature"].mean().reset_index()
    fig = px.line(yearly_trend, x="year", y="temperature", title="Средняя температура по годам")
    st.plotly_chart(fig, use_container_width=True, key="temperature_trends")


def display_temperature_distribution(city_data):
    st.subheader("Распределение температуры")
    fig = px.histogram(city_data, x="temperature", nbins=30, title="Распределение температуры")
    st.plotly_chart(fig, use_container_width=True, key="temperature_distribution")


def display_correlation_analysis(city_data):
    if "humidity" in city_data.columns and "pressure" in city_data.columns:
        st.subheader("Корреляция температуры с другими параметрами")
        corr_matrix = city_data[["temperature", "humidity", "pressure"]].corr()
        fig = px.imshow(corr_matrix, text_auto=True, title="Матрица корреляции")
        st.plotly_chart(fig, use_container_width=True, key="correlation_analysis")


def display_extreme_temperatures(city_data):
    st.subheader("Экстремальные температуры")
    min_temp = city_data["temperature"].min()
    max_temp = city_data["temperature"].max()
    st.markdown(f"""
    - **Минимальная температура**: {min_temp:.2f}°C
    - **Максимальная температура**: {max_temp:.2f}°C
    """)

    extreme_data = city_data[(city_data["temperature"] == min_temp) | (city_data["temperature"] == max_temp)]
    st.write(extreme_data)


def display_heatmap_by_day_month(city_data, city):
    st.subheader("Тепловая карта температуры по дням и месяцам")
    city_data["month"] = pd.to_datetime(city_data["timestamp"]).dt.month
    city_data["day"] = pd.to_datetime(city_data["timestamp"]).dt.day
    heatmap_data = city_data.groupby(["month", "day"])["temperature"].mean().unstack()
    fig = px.imshow(heatmap_data, labels=dict(x="День", y="Месяц", color="Температура (°C)"),
                    title=f"Температура в городе {city} по дням и месяцам")
    st.plotly_chart(fig, use_container_width=True, key="heatmap_day_month")


def display_boxplot_by_season(city_data, city):
    st.subheader("Распределение температуры по сезонам (Boxplot)")
    fig = px.box(city_data, x="season", y="temperature", title=f"Распределение температуры по сезонам в городе {city}")
    st.plotly_chart(fig, use_container_width=True, key="boxplot_by_season")


def display_comparison_between_cities(df):
    st.subheader("Сравнение температуры между городами")
    cities = st.multiselect("Выберите города для сравнения", df["city"].unique(), default=df["city"].unique()[:2])
    if len(cities) >= 2:
        comparison_data = df[df["city"].isin(cities)]
        fig = px.line(comparison_data, x="timestamp", y="temperature", color="city",
                      title="Сравнение температуры между городами")
        st.plotly_chart(fig, use_container_width=True, key="comparison_between_cities")
    else:
        st.warning("Выберите как минимум два города для сравнения.")


def visualize_data(session: LoggedSession):
    st.header("📈 Визуализация")
    st.info("Здесь представлен расширенный анализ загруженного набора данных.")

    if not hasattr(session, "df"):
        st.warning("Загрузите данные на вкладке '📁 Загрузка данных'.")
        return

    df = session.df

    city = st.selectbox("Выберите город", df["city"].unique(), key="city_selectbox_visualization")
    city_data = df[df["city"] == city].copy()

    threshold = city_data["temperature"].quantile(0.9)
    city_data.loc[:, "is_anomaly"] = city_data["temperature"] > threshold

    display_comparison_between_cities(df)
    display_seasonal_profiles(city_data, city)
    display_temperature_trends(city_data)
    display_temperature_distribution(city_data)
    display_correlation_analysis(city_data)
    display_extreme_temperatures(city_data)
    display_heatmap_by_day_month(city_data, city)
    display_boxplot_by_season(city_data, city)