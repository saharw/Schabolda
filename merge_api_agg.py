import pandas as pd

def merge_agg_api(df_agg, df_api):
    if df_agg.index.name =="archive_date": #проверка чтобы выровняться по индексам
        df_agg = df_agg.reset_index()

    merged = pd.merge(df_api, df_agg, on="archive_date", how="left")
    merged = merged.sort_values(by="archive_date")

    return merged

df_agg = pd.read_csv('df_agg.csv')
df_api = pd.read_csv('merged_data.csv')
df_api["archive_date"]=pd.to_datetime(df_api["archive_date"],format="mixed",dayfirst=True)
df_api["archive_date"]=df_api["archive_date"].dt.strftime("%d.%m.%Y")

df_fin =  merge_agg_api(df_agg, df_api)

df_fin.reset_index().to_csv("final_merge.csv", index=True)