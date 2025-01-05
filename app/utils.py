import pandas as pd
import numpy as np

def calculate_moving_average(df, window=30):
    df["moving_avg"] = df["temperature"].rolling(window=window).mean()
    return df

def detect_anomalies(df, std_dev_factor=2):
    df["mean"] = df.groupby("season")["temperature"].transform("mean")
    df["std"] = df.groupby("season")["temperature"].transform("std")
    df["anomaly"] = abs(df["temperature"] - df["mean"]) > std_dev_factor * df["std"]
    return df
