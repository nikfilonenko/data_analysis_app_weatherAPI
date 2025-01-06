import streamlit as st
from app.logging_config import LoggedSession
from app.settings.api_client import OpenWeatherMapClient


owmc = OpenWeatherMapClient(api_key='...')


def monitor_temperature(session: LoggedSession):
    st.header("🌡️ Текущая температура")

    api_key = st.text_input("Введите API ключ OpenWeatherMap", type="password")

    if api_key:
        city = st.selectbox("Выберите город", [
            "New York",
            "London",
            "Paris",
            "Tokyo",
            "Moscow",
            "Sydney",
            "Berlin",
            "Beijing",
            "Rio de Janeiro",
            "Dubai",
            "Los Angeles",
            "Singapore",
            "Mumbai",
            "Cairo",
            "Mexico City"
        ])

        current_temp = owmc.get_current_temperature(city, api_key)

        if current_temp:
            st.write(f"Текущая температура в {city}: {current_temp}°C")
        else:
            st.error("Неверный ключ API. "
                     "Пожалуйста, смотрите раздел "
                     "https://openweathermap.org/faq#error401 "
                     "для получения дополнительной информации.")
    else:
        st.warning("Введите API ключ для отображения данных.")