import streamlit as st
import pandas as pd
from app.pages.analysis import calculate_moving_average, calculate_anomalies
from app.settings.api_client import get_current_temperature


def main():
    st.title("Анализ температурных данных")

    # Загрузка данных
    uploaded_file = st.file_uploader("Загрузите файл с историческими данными", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Данные успешно загружены!")

        # Выбор города
        city = st.selectbox("Выберите город", data['city'].unique())

        # Ввод API-ключа
        api_key = st.text_input("Введите API-ключ OpenWeatherMap")
        if api_key:
            try:
                current_temp = get_current_temperature(api_key, city)
                st.write(f"Текущая температура в {city}: {current_temp}°C")
            except Exception as e:
                st.error(f"Ошибка: {e}")

        # Отображение графиков и статистик
        if st.button("Показать анализ"):
            moving_avg = calculate_moving_average(data[data['city'] == city])
            anomalies = calculate_anomalies(data[data['city'] == city])

            st.line_chart(moving_avg)
            st.write("Аномалии:", anomalies)

if __name__ == "__main__":
    main()