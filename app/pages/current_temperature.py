import time
import asyncio
import aiohttp
import requests
import streamlit as st
from datetime import datetime
from app.logging_config import LoggedSession
from app.settings.api_client import OpenWeatherMapClient


owmc = OpenWeatherMapClient(api_key='...')


async def fetch_async(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_current_temperature_async(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    async with aiohttp.ClientSession() as session:
        data = await fetch_async(session, url)
        return data['main']['temp']


def get_current_temperature_sync(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data['main']['temp']


def is_temperature_normal(current_temp, season_data):
    q1 = season_data['q1']
    q3 = season_data['q3']
    return q1 <= current_temp <= q3


def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"


def check_api_key(api_key):
    test_city = "London"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={test_city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.status_code == 200


def check_temperature_normal(df, city, api_key):
    city_data = df[df['city'] == city]
    if not city_data.empty:
        current_date = datetime.now()
        season = get_season(current_date)
        season_data = city_data.groupby('season')['temperature'].agg(
            mean='mean', q1=lambda x: x.quantile(0.25), q3=lambda x: x.quantile(0.75)
        ).loc[season]

        current_temp = get_current_temperature_sync(city, api_key)
        if current_temp:
            if is_temperature_normal(current_temp, season_data):
                st.success(f"Текущая температура {current_temp}°C нормальна для сезона {season}.")
            else:
                st.warning(f"Текущая температура {current_temp}°C выходит за пределы нормы для сезона {season}.")


def monitor_temperature(session: LoggedSession):
    st.header("🌡️ Текущая температура")

    if not hasattr(session, "df"):
        st.warning("Загрузите данные на вкладке '📁 Загрузка данных'.")
        return

    df = session.df

    api_key = st.text_input("Введите API ключ OpenWeatherMap", type="password")

    if api_key:
        if check_api_key(api_key):
            st.success("API ключ корректный.")
            cities = df["city"].unique().tolist()
            city = st.selectbox("Выберите город", cities)

            if st.button("Получить температуру (синхронно)"):
                start_time = time.time()
                current_temp = get_current_temperature_sync(city, api_key)
                end_time = time.time()
                if current_temp:
                    st.write(f"Текущая температура в {city}: {current_temp}°C")
                    st.write(f"Время выполнения: {end_time - start_time:.2f} секунд")
                    check_temperature_normal(df, city, api_key)
                else:
                    st.error("Ошибка при получении температуры.")

            if st.button("Получить температуру (асинхронно)"):
                start_time = time.time()
                current_temp = asyncio.run(get_current_temperature_async(city, api_key))
                end_time = time.time()
                if current_temp:
                    st.write(f"Текущая температура в {city}: {current_temp}°C")
                    st.write(f"Время выполнения: {end_time - start_time:.2f} секунд")
                    check_temperature_normal(df, city, api_key)
                else:
                    st.error("Ошибка при получении температуры.")
        else:
            st.error("Неверный ключ API. "
                     "Пожалуйста, смотрите раздел "
                     "https://openweathermap.org/faq#error401 "
                     "для получения дополнительной информации.")
    else:
        st.warning("Введите API ключ для отображения данных.")