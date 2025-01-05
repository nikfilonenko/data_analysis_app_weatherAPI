import streamlit as st
from logging_config import LoggedSession


def visualize_data(session: LoggedSession):
    st.header("📈 Визуализация")

    if not hasattr(session, "df"):
        st.warning("Загрузите данные на вкладке '📁 Загрузка данных'.")
        return

    df = session.df

    # Выбор города
    city = st.selectbox("Выберите город", df["city"].unique())

    # Фильтрация данных по городу
    city_data = df[df["city"] == city]

    # Визуализация сезонных профилей
    st.subheader("Сезонные профили температуры")
    seasonal_data = city_data.groupby("season")["temperature"].mean()
    st.bar_chart(seasonal_data)