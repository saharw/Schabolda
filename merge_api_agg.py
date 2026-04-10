import pandas as pd

def merge_agg_api(df_agg, df_api):
    if df_agg.index.name =="archive_date": #проверка чтобы выровняться по индексам
        df_agg = df_agg.reset_index()

    #Перестраховка по приведению в один формат
    df_agg["archive_date"]= pd.to_datetime(df_agg["archive_date"])
    df_api["archive_date"]= pd.to_datetime(df_api["archive_date"])

    merged = pd.merge(df_api, df_agg, on="archive_date", how="left")
    merged = merged.sort_values(by="archive_date")

    return merged
