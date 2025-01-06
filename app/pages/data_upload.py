import streamlit as st
import pandas as pd
from app.logging_config import LoggedSession


def upload_dataset(session: LoggedSession):
    st.header("📁 Загрузка данных")

    uploaded_file = st.file_uploader("Загрузите файл с температурными данными (CSV)", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        session.df = df
        st.success("Данные успешно загружены!")

        st.markdown(f"- Столбцы: **{df.columns.tolist()}**")
        st.markdown(f"- Всего строк: `{len(df)}`")
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