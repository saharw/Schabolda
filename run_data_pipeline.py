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