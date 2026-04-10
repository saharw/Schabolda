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


def process_data(data, symbol):
    ts = data["Time Series (Daily)"]

    df = pd.DataFrame(ts).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df.columns = ["open", "high", "low", "close", "volume"]
    df = df.astype(float)

    df["ticker"] = symbol

    return df


def load_market_data(tickers):
    all_data = []

    for ticker in tickers:
        print(f"Загружаю {ticker}")

        data = get_daily_data(ticker)
        if data is None:
            continue

        df = process_data(data, ticker)
        all_data.append(df)

        time.sleep(12)

    if len(all_data) == 0:
        print("Нет данных")
        return None

    return pd.concat(all_data)


def save_data(df, path):
    df.to_csv(path)
    print("Сохранили в файл")