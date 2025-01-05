import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from logging_config import LoggedSession
from scipy.stats import skew, kurtosis


def display_descriptive_statistics(city_data):
    st.subheader("Описательная статистика")

    desc_stats = city_data.describe()

    skewness = skew(city_data["temperature"])
    kurt = kurtosis(city_data["temperature"])

    st.write(desc_stats)

    # Динамические выводы на основе describe()
    mean_temp = desc_stats.loc["mean", "temperature"]
    median_temp = desc_stats.loc["50%", "temperature"]
    std_temp = desc_stats.loc["std", "temperature"]
    min_temp = desc_stats.loc["min", "temperature"]
    max_temp = desc_stats.loc["max", "temperature"]
    q1_temp = desc_stats.loc["25%", "temperature"]
    q3_temp = desc_stats.loc["75%", "temperature"]

    st.markdown(f"""
    ### Анализ описательной статистики:
    
    - **Средняя температура**: `{mean_temp:.2f}°C`.
    - **Медианная температура**: `{median_temp:.2f}°C`.
        - {"Средняя температура близка к медиане, что указывает на симметричное распределение." if abs(mean_temp - median_temp) < 1 else "Средняя температура значительно отличается от медианы, что указывает на асимметричное распределение."}
    -----
    - **Разброс температуры**:
        - Стандартное отклонение: `{std_temp:.2f}°C`.
        - {"`Разброс данных небольшой, температура относительно стабильна.`" if std_temp < 5 else "`Разброс данных значительный, температура сильно варьируется.`"}
    -----
    - **Диапазон температур**:
        - Минимальная температура: `{min_temp:.2f}°C`.
        - Максимальная температура: `{max_temp:.2f}°C`.
        - Общий диапазон: `{max_temp - min_temp:.2f}°C`.
        
    -----
    """)

    # Скошенность (skewness)
    st.markdown(f"""
    ### Анализ формы распределения
    
    #### Скошенность (skewness):
    - **Значение**: `{skewness:.2f}`
    - **Интерпретация**:
        - {"`Распределение имеет правый скос (длинный хвост справа).`" if skewness > 0 else "`Распределение имеет левый скос (длинный хвост слева)." if skewness < 0 else "Распределение симметрично.`"}
    -----
    """)

    # Эксцесс (kurtosis)
    st.markdown(f"""
    #### Эксцесс (kurtosis):
    - **Значение**: `{kurt:.2f}`
    - **Интерпретация**:
        - {"`Распределение имеет острый пик и тяжелые хвосты (больше выбросов).`" if kurt > 0 else "`Распределение имеет плоский пик и легкие хвосты (меньше выбросов).`" if kurt < 0 else "Распределение близко к нормальному."}
    -----
    """)

    st.subheader("Распределение температуры")
    fig = px.histogram(city_data, x="temperature", nbins=30, title="Распределение температуры")

    # Добавляем линии для среднего, медианы и квартилей
    fig.add_vline(x=mean_temp, line_dash="dash", line_color="red", annotation_text=f"Среднее: {mean_temp:.2f}°C",
                  annotation_position="top")
    fig.add_vline(x=median_temp, line_dash="dash", line_color="green", annotation_text=f"Медиана: {median_temp:.2f}°C",
                  annotation_position="bottom")
    fig.add_vline(x=q1_temp, line_dash="dot", line_color="blue", annotation_text=f"25%: {q1_temp:.2f}°C",
                  annotation_position="top")
    fig.add_vline(x=q3_temp, line_dash="dot", line_color="blue", annotation_text=f"75%: {q3_temp:.2f}°C",
                  annotation_position="top")

    # Добавляем информацию о стандартном отклонении
    fig.add_vrect(
        x0=mean_temp - std_temp, x1=mean_temp + std_temp,
        fillcolor="lightgray", opacity=0.5,
        annotation_text=f"±1σ: {std_temp:.2f}°C", annotation_position="top"
    )

    st.plotly_chart(fig, use_container_width=True)


def display_temperature_time_series(city_data, city):
    """Отображает временной ряд температуры с аномалиями."""
    st.subheader("Временной ряд температуры с аномалиями")

    # Определение аномалий (например, температуры выше 90-го процентиля)
    threshold = np.percentile(city_data["temperature"], 90)
    city_data["is_anomaly"] = city_data["temperature"] > threshold

    # Визуализация с использованием Plotly
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=city_data["timestamp"],
            y=city_data["temperature"],
            mode="lines",
            name="Температура",
            line=dict(color="blue", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=city_data[city_data["is_anomaly"]]["timestamp"],
            y=city_data[city_data["is_anomaly"]]["temperature"],
            mode="markers",
            name="Аномалии",
            marker=dict(color="red", size=8),
        )
    )
    fig.update_layout(
        title=f"Температура в городе {city} с выделением аномалий",
        xaxis_title="Дата",
        yaxis_title="Температура (°C)",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)


def display_correlation_analysis(city_data):
    """Отображает корреляцию температуры с другими параметрами."""
    if "humidity" in city_data.columns and "pressure" in city_data.columns:
        st.subheader("Корреляция температуры с другими параметрами")
        corr_matrix = city_data[["temperature", "humidity", "pressure"]].corr()
        fig = px.imshow(corr_matrix, text_auto=True, title="Матрица корреляции")
        st.plotly_chart(fig, use_container_width=True)


def display_seasonal_profiles(city_data, city):
    """Отображает сезонные профили температуры с подробным анализом."""
    st.subheader("Сезонные профили температуры")

    # Группировка по сезонам
    seasonal_data = city_data.groupby("season")["temperature"].agg(
        [("mean", "mean"), ("median", "median"), ("q1", lambda x: x.quantile(0.25)), ("q3", lambda x: x.quantile(0.75)), ("count", "size")]
    ).reset_index()

    # Визуализация с использованием Plotly
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=seasonal_data["season"],
            y=seasonal_data["mean"],
            error_y=dict(type="data", array=seasonal_data["mean"] - seasonal_data["q1"], visible=True),
            name="Средняя температура",
        )
    )
    fig.update_layout(
        title=f"Сезонные профили температуры в городе {city}",
        xaxis_title="Сезон",
        yaxis_title="Средняя температура (°C)",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Динамические выводы
    st.markdown("### Анализ сезонных профилей температуры:")
    for index, row in seasonal_data.iterrows():
        season = row["season"]
        mean_temp = row["mean"]
        median_temp = row["median"]
        q1_temp = row["q1"]
        q3_temp = row["q3"]
        count = row["count"]

        st.markdown(f"""
        #### Сезон: **{season}**
        - **Средняя температура**: `{mean_temp:.2f}°C`
        - **Медианная температура**: `{median_temp:.2f}°C`
        - **25-й процентиль (Q1)**: `{q1_temp:.2f}°C`
        - **75-й процентиль (Q3)**: `{q3_temp:.2f}°C`
        - **Количество данных**: `{count}`
        """)

        # Интерпретация
        if mean_temp > median_temp:
            st.markdown(f"В сезоне **{season}** средняя температура выше медианы, что указывает на наличие выбросов с высокой температурой.")
        elif mean_temp < median_temp:
            st.markdown(f"В сезоне **{season}** средняя температура ниже медианы, что указывает на наличие выбросов с низкой температурой.")
        else:
            st.markdown(f"В сезоне **{season}** средняя температура близка к медиане, что указывает на симметричное распределение.")

        # Анализ разброса
        iqr = q3_temp - q1_temp  # Межквартильный размах
        st.markdown(f"Межквартильный размах (IQR): {iqr:.2f}°C.")
        if iqr < 5:
            st.markdown(f"Разброс температуры в сезоне **{season}** небольшой, что указывает на стабильные условия.")
        else:
            st.markdown(f"Разброс температуры в сезоне **{season}** значительный, что указывает на изменчивые условия.")


def analyze_data(session: LoggedSession):
    """Основная функция для анализа данных."""
    st.header("📊 Анализ данных")

    if not hasattr(session, "df"):
        st.warning("Загрузите данные на вкладке '📁 Загрузка данных'.")
        return

    df = session.df

    # Выбор города
    city = st.selectbox("Выберите город", df["city"].unique(), key="city_selectbox")

    # Фильтрация данных по городу
    city_data = df[df["city"] == city]

    # Отображение описательной статистики и анализа распределения
    display_descriptive_statistics(city_data)

    # Отображение временного ряда температуры с аномалиями
    display_temperature_time_series(city_data, city)

    # Отображение корреляции температуры с другими параметрами
    display_correlation_analysis(city_data)

    # Отображение сезонных профилей температуры
    display_seasonal_profiles(city_data, city)