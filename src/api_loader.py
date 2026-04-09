import requests
import pandas as pd
import time

API_KEY = "71D8X13H5HB9KM10"
BASE_URL = "https://www.alphavantage.co/query"

def get_daily_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # проверка лимитов
    if "Note" in data or "Information" in data:
        print(f"Лимит API или ошибка для {symbol}: {data}")
        return None

    # проверка наличия данных
    if "Time Series (Daily)" not in data:
        print(f"Нет данных для {symbol}: {data}")
        return None

    return data