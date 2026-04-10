import requests
import pandas as pd

API_KEY = "71D8X13H5HB9KM10"
BASE_URL = "https://www.alphavantage.co/query"


def get_usd_eur_daily():
    print("Загружаю курс USD/EUR")

    params = {
        "function": "FX_DAILY",
        "from_symbol": "USD",
        "to_symbol": "EUR",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data["Time Series FX (Daily)"]).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df.columns = ["open", "high", "low", "close"]
    df = df.astype(float)

    return df