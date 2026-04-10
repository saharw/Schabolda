from src.api_loader import load_market_data, save_data
from src.indicators import load_indicators
from src.macro_data import get_usd_eur_daily

# Выгрузка тикеров
tickers = ["USO", "XLE", "XOM", "CVX", "BP", "SHEL"]
print("Начинаем загрузку данных...")
market_df = load_market_data(tickers)

if market_df is not None:
    save_data(market_df, "data/raw/market_data.csv")
    print("Рыночные данные сохранены")
else:
    print("Ошибка рынка")


# Выгрузка индикаторов для тикера XOM
print("\nЗагружаем индикаторы...")

ind_df = load_indicators("XOM")

if ind_df is not None:
    save_data(ind_df, "data/raw/indicators_xom.csv")
    print("Индикаторы сохранены")
else:
    print("Ошибка индикаторов")


# Выгрузка валютных изменений
print("\nЗагружаем макро данные...")

macro_df = get_usd_eur_daily()

if macro_df is not None:
    save_data(macro_df, "data/raw/macro_usd.csv")
    print("Макро данные сохранены")
else:
    print("Ошибка макро данных")