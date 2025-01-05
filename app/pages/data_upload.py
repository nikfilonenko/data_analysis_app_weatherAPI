import streamlit as st
import pandas as pd
from app.logging_config import LoggedSession


def upload_dataset(session: LoggedSession):
    st.header("📁 Загрузка данных")

    # Загрузка файла
    uploaded_file = st.file_uploader("Загрузите файл с температурными данными (CSV)", type="csv")

    if uploaded_file is not None:
        # Чтение данных
        df = pd.read_csv(uploaded_file)
        session.df = df  # Сохраняем данные в сессии
        st.success("Данные успешно загружены!")
        st.write(f"Все данные `{uploaded_file.name}`:")

        st.markdown(
            """
            <style>
                .main .block-container {
                    max-width: 100%;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.dataframe(df, width=1000)