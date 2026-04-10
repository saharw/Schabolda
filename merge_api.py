import pandas as pd

market = pd.read_csv("market_data.csv")
macro = pd.read_csv("macro_usd.csv")
indicators = pd.read_csv("indicators_xom.csv")

#приводим к единому формату столб даты
market = market.rename(columns={market.columns[0]: "archive_date"})
macro = macro.rename(columns={macro.columns[0]: "archive_date"})
indicators = indicators.rename(columns={indicators.columns[0]: "archive_date"})


market["archive_date"] = pd.to_datetime(market["archive_date"])
macro["archive_date"] = pd.to_datetime(macro["archive_date"])
indicators["archive_date"] = pd.to_datetime(indicators["archive_date"])

market = market.rename(columns={col: f"market_{col}" for col in market.columns if col != "archive_date"})
macro = macro.rename(columns={col: f"macro_{col}" for col in macro.columns if col != "archive_date"})
indicators = indicators.rename(columns={col: f"indicators_{col}" for col in indicators.columns if col != "archive_date"})

df = market.merge(macro, on="archive_date", how="left")
df = df.merge(indicators, on="archive_date", how="left")

df = df.sort_values("archive_date")

df.to_csv("merged_data.csv", index=False, encoding="utf-8-sig")