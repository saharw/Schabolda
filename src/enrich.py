import pandas as pd
import numpy as np
from transformers import pipeline



df = pd.read_csv("parser_news.csv")

df["full_text"] = df["title"] + ". " + df["description"]


# https://huggingface.co/facebook/bart-large-mnli
# берем готовую библиотеку для того, чтобы оценить насколько новость финансовая
financial_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

labels = ["financial news", "non-financial news"]

#функция, которая будет на основе текста новости будет относить ее к нужному классу
def classify_financial(text):
    result = financial_classifier(text, labels)

    # формат ответа{
    #   'sequence': 'text',
    #    'labels': ['financial news', 'non-financial news'],
    #    'scores': [0.98, 0.02]
    #}

    best_label = result["labels"][0]


    if best_label == "financial news":
        is_financial = 1
    else:
        is_financial = 0

    return is_financial

df["is_financial"] = df["full_text"].apply(classify_financial)

df.to_csv("enrich01.csv", index=False, encoding="utf-8-sig")