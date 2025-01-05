import sys
from pathlib import Path
import streamlit as st
from logging_config import LoggedSession
from pages.data_upload import upload_dataset
from pages.data_analysis import analyze_data
from pages.current_temperature import monitor_temperature
from pages.visualization import visualize_data


sys.path.append(str(Path(__file__).resolve().parent))
session = LoggedSession()


def main():
    st.title("🌍 Анализ температурных данных")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📁 Загрузка данных", "📊 Анализ данных", "📈 Визуализация", "🌡️ Текущая температура OpenWeatherAPI"]
    )

    with tab1:
        upload_dataset(session)
    with tab2:
        analyze_data(session)
    with tab3:
        visualize_data(session)
    with tab4:
        monitor_temperature(session)


    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"][aria-expanded="true"],
            div[data-testid="stSidebarCollapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()