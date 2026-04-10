import pandas as pd
import numpy as np
#df = pd.read_csv('enrich_finbert1.csv')
def day_metrics(df):
    #подготовка df: создание тоталов по кол-ву позитивных, нейтральных и негативных новостей в разрезе:
    #все новости и финансовые новости (В, Ф)
    #по числу (сколько таких новостей) и по уверенности (какая сумма "уверенности модели")

    #уверенность, В
    df["pos_score"]=np.where(df["finbert_label"]=="positive",df["finbert_score"],0)
    df["neg_score"]=np.where(df["finbert_label"]=="negative",df["finbert_score"],0)
    df["neu_score"]=np.where(df["finbert_label"]=="neutral",df["finbert_score"],0)
    # уверенность, Ф
    df["fin_pos_score"]=np.where((df["is_financial"]==1)&(df["finbert_label"]=="positive"),df["finbert_score"],0)
    df["fin_neg_score"]=np.where((df["is_financial"]==1)&(df["finbert_label"]=="negative"),df["finbert_score"],0)
    df["fin_neu_score"]=np.where((df["is_financial"]==1)&(df["finbert_label"]=="neutral"),df["finbert_score"],0)
    # кол-во, В
    df["pos_flag"]=(df["finbert_label"]=="positive").astype(int)
    df["neg_flag"]=(df["finbert_label"]=="negative").astype(int)
    df["neu_flag"]=(df["finbert_label"]=="neutral").astype(int)
    # кол-во, Ф
    df["fin_pos_flag"]=np.where((df["is_financial"]==1)&(df["finbert_label"]=="positive"),1,0)
    df["fin_neg_flag"]=np.where((df["is_financial"]==1)&(df["finbert_label"]=="negative"),1,0)
    df["fin_neu_flag"]=np.where((df["is_financial"]==1)&(df["finbert_label"]=="neutral"),1,0)

    # Агрегация, колонки для расчета:
    # Все новости за день (число)
    # Сумма оценок уверенности по финансовым новостям
    # Сумма оценок уверенности в разрезе позитив, негатив, нейтрально
    # Сумма оценок уверенности по финансовым новосотям в разрезе позитив, негатив, нейтрально
    # Сумма новостей в разрезе позитив, негатив, нейтрально
    # Сумма новостей по финансам в разрезе позитив, негатив, нейтрально
    # доп для удобства: принцип неймингаsum - score, count - flag

    df_gr_day=df.groupby("archive_date").agg(total_news=("title", "count"), financial_share=("is_financial", "mean"), pos_sum=("pos_score", "sum"), neg_sum=("neg_score", "sum"), neu_sum=("neu_score", "sum"), fin_pos_sum=("fin_pos_score", "sum"), fin_neg_sum=("fin_neg_score", "sum"), fin_neu_sum=("fin_neu_score", "sum"), pos_count=("pos_flag", "sum"), neg_count=("neg_flag", "sum"), neu_count=("neu_flag", "sum"), fin_pos_count=("fin_pos_flag", "sum"), fin_neg_count=("fin_neg_flag", "sum"), fin_neu_count=("fin_neu_flag", "sum"))

    df_gr_day["total_score"]= df_gr_day["pos_sum"] + df_gr_day["neg_sum"] + df_gr_day["neu_sum"]
    df_gr_day["fin_total_score"]= df_gr_day["fin_pos_sum"] + df_gr_day["fin_neg_sum"] + df_gr_day["fin_neu_sum"]

    df_gr_day["pos_share"]= df_gr_day["pos_sum"] / df_gr_day["total_score"]
    df_gr_day["neg_share"]= df_gr_day["neg_sum"] / df_gr_day["total_score"]
    df_gr_day["neu_share"]= df_gr_day["neu_sum"] / df_gr_day["total_score"]

    df_gr_day["fin_pos_share"]= df_gr_day["fin_pos_sum"] / df_gr_day["fin_total_score"]
    df_gr_day["fin_neg_share"]= df_gr_day["fin_neg_sum"] / df_gr_day["fin_total_score"]
    df_gr_day["fin_neu_share"]= df_gr_day["fin_neu_sum"] / df_gr_day["fin_total_score"]

    df_gr_day["pos_share_count"]= df_gr_day["pos_count"] / df_gr_day["total_news"]
    df_gr_day["neg_share_count"]= df_gr_day["neg_count"] / df_gr_day["total_news"]
    df_gr_day["neu_share_count"]= df_gr_day["neu_count"] / df_gr_day["total_news"]

    df_gr_day["fin_total_count"]= df_gr_day["fin_pos_count"] + df_gr_day["fin_neg_count"] + df_gr_day["fin_neu_count"]
    df_gr_day["fin_pos_share_count"]= df_gr_day["fin_pos_count"] / df_gr_day["fin_total_count"]
    df_gr_day["fin_neg_share_count"]= df_gr_day["fin_neg_count"] / df_gr_day["fin_total_count"]
    df_gr_day["fin_neu_share_count"]= df_gr_day["fin_neu_count"] / df_gr_day["fin_total_count"]

    #ATTENTION: шаг ниже позволяет выбрать наиболее релевантные колонки в файл. Регулируется при необходимости
    df_gr_day=df_gr_day[["financial_share","fin_pos_share_count","fin_neg_share_count","fin_neu_share_count","fin_pos_share","fin_neg_share","fin_neu_share"]]
    return(df_gr_day)

df_pr = pd.read_csv('df_process.csv')
df_pr = day_metrics(df_pr)
df_pr.reset_index().to_csv("df_agg.csv", index=True)