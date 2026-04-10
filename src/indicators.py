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


def get_sma(symbol):
    params = {
        "function": "SMA",
        "symbol": symbol,
        "interval": "daily",
        "time_period": 14,
        "series_type": "close",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data["Technical Analysis: SMA"]).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df.columns = ["sma"]
    df = df.astype(float)

    return df


def get_ema(symbol):
    params = {
        "function": "EMA",
        "symbol": symbol,
        "interval": "daily",
        "time_period": 14,
        "series_type": "close",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data["Technical Analysis: EMA"]).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df.columns = ["ema"]
    df = df.astype(float)

    return df


def load_indicators(symbol):
    print(f"Индикаторы для {symbol}")

    rsi = get_rsi(symbol)
    time.sleep(12)

    sma = get_sma(symbol)
    time.sleep(12)

    ema = get_ema(symbol)
    time.sleep(12)

    if rsi is None or sma is None or ema is None:
        print("Ошибка загрузки индикаторов")
        return None

    df = rsi.join(sma)
    df = df.join(ema)

    return df