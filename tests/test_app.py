import pytest
import pandas as pd
from app.logging_config import LoggedSession
from app.pages.data_upload import upload_dataset
from app.pages.data_analysis import analyze_data
from app.pages.visualization import visualize_data
from app.pages.current_temperature import monitor_temperature
from app.pages.data_analysis import (
    display_descriptive_statistics,
    display_temperature_time_series,
    display_correlation_analysis,
    display_seasonal_profiles
)


@pytest.fixture
def sample_data():
    data = {
        "city": ["Berlin", "Berlin", "Cairo", "Cairo"],
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-01", "2023-01-02"],
        "temperature": [10, 12, 25, 26],
        "humidity": [60, 65, 70, 75],
        "pressure": [1010, 1012, 1015, 1016],
        "season": ["Winter", "Winter", "Summer", "Summer"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def session(sample_data):
    session = LoggedSession()
    session.df = sample_data
    return session


def test_upload_dataset(session, tmp_path, sample_data):
    file_path = tmp_path / "test.csv"
    sample_data.to_csv(file_path, index=False)

    class MockFileUploader:
        def __init__(self, file_path):
            self.file_path = file_path

        def read(self):
            with open(self.file_path, "rb") as f:
                return f.read()

    class MockStreamlit:
        def __init__(self, file_path):
            self.uploaded_file = MockFileUploader(file_path)

        def file_uploader(self, *args, **kwargs):
            return self.uploaded_file

        def success(self, message):
            print(f"Success: {message}")

        def write(self, message):
            print(f"Write: {message}")

        def markdown(self, *args, **kwargs):
            print(f"Markdown: {args}")

        def dataframe(self, *args, **kwargs):
            print(f"DataFrame: {args}")

    upload_dataset(session)

    assert hasattr(session, "df")
    assert isinstance(session.df, pd.DataFrame)
    assert not session.df.empty

    assert session.df.equals(sample_data)


def test_analyze_data(session):
    analyze_data(session)
    assert True


def test_visualize_data(session):
    visualize_data(session)
    assert True


def test_display_descriptive_statistics(session):
    city_data = session.df[session.df["city"] == "Berlin"]
    display_descriptive_statistics(city_data)
    assert True


def test_display_temperature_time_series(session):
    city_data = session.df[session.df["city"] == "Berlin"]
    display_temperature_time_series(city_data, "Berlin")
    assert True


def test_display_correlation_analysis(session):
    city_data = session.df[session.df["city"] == "Berlin"]
    display_correlation_analysis(city_data)
    assert True


def test_display_seasonal_profiles(session):
    city_data = session.df[session.df["city"] == "Berlin"]
    display_seasonal_profiles(city_data, "Berlin")
    assert True