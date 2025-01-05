import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from logging_config import LoggedSession


def analyze_data(session: LoggedSession):
    st.header("📊 Анализ данных")

    if not hasattr(session, "df"):
        st.warning("Загрузите данные на вкладке '📁 Загрузка данных'.")
        return

    df = session.df

    # Выбор города
    city = st.selectbox("Выберите город", df["city"].unique())

    # Фильтрация данных по городу
    city_data = df[df["city"] == city]

    # Описательная статистика
    st.subheader("Описательная статистика")
    st.write(city_data.describe())

    # Визуализация временного ряда
    st.subheader("Временной ряд температуры")

    # Используем st.line_chart для простого графика
    st.line_chart(city_data.set_index("timestamp")["temperature"])

    # Альтернативно, можно использовать matplotlib для более сложной визуализации
    st.subheader("Временной ряд температуры (Matplotlib)")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(city_data["timestamp"], city_data["temperature"], label="Температура", color="blue")
    ax.set_title(f"Температура в городе {city}")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Температура (°C)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)