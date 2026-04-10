import requests
import pandas as pd
import time

API_KEY = "71D8X13H5HB9KM10"
BASE_URL = "https://www.alphavantage.co/query"


def get_rsi(symbol):
    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": "daily",
        "time_period": 14,
        "series_type": "close",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data["Technical Analysis: RSI"]).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df.columns = ["rsi"]
    df = df.astype(float)

    return df