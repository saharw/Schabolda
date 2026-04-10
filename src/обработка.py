import pandas as pd
df = pd.read_csv('enrich_finbert1.csv')

def duplicate_function (df):
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset = 'article_url')
    df = df.drop_duplicates(subset = 'title')
    df = df.drop_duplicates(subset = 'description')
    return df

def data_upd (df):
    df['archive_date'] = df['archive_date'].str.replace('\ufeff', '')
    df['archive_date'] = pd.to_datetime(df['archive_date'])
    df['archive_date'] = df['archive_date'].dt.strftime('%d.%m.%Y')
    return df

def na (df):
    df = df[df['description'].notna()]
    df = df[df['title'].notna()]
    return df

def stip_simbols(df):
    df['title']= df['title'].str.strip()
    df['description'] = df['description'].str.strip()
    return df

df = duplicate_function(df)
df = data_upd(df)
df = na(df)
df = stip_simbols(df)

df.reset_index().to_csv("df_process.csv", index=True)