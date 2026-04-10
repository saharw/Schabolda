import pandas as pd
import numpy as np
from transformers import pipeline

df = pd.read_csv("enrich01.csv" )

#используем готовую библиотеку для получения окраски новости (негатив, позитив и тд) с уверенность (скором)
# брал как рефернс отсюдова https://github.com/hperer02/Portfolio-optimization-using-deep-learning/blob/main/FinBERT_newsapi.ipynb
# и отсюдова https://www.kaggle.com/code/zeeshanjamal97/2-financial-headline-sentiment-analysis-finbert

finbert = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert"
)

#функция, клторая по тексту новости выдает 2 значения - окраска и скор
def finbert_sentiment(text):
    #текст очень большой попадается, поэтому обезаю через truncation + иногда флоаты проскакивают, поэтому str текст
    result = finbert(str(text), truncation=True)[0]

    return pd.Series({
        "finbert_label": result["label"],
        "finbert_score": result["score"]
    })

mask = df["is_financial"] == 1
#создаем столбцы с результатами
result = df.loc[mask, "full_text"].apply(finbert_sentiment)

#джоиним
df.loc[mask, ["finbert_label", "finbert_score"]] = result

df.to_csv("enrich_finbert1.csv", index=False, encoding="utf-8-sig")