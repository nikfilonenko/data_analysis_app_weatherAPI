import pandas as pd

def calculate_moving_average(data, window=30):
    return data['temperature'].rolling(window=window).mean()

def calculate_anomalies(data, window=30):
    moving_avg = calculate_moving_average(data, window)
    std_dev = data['temperature'].rolling(window=window).std()
    anomalies = data[(data['temperature'] > moving_avg + 2 * std_dev) |
                     (data['temperature'] < moving_avg - 2 * std_dev)]
    return anomalies