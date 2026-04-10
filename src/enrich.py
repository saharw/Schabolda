import pandas as pd
import numpy as np
from transformers import pipeline

financial_section = {}

df = pd.read_csv("parser_news.csv")

df["full_text"] = df["title"] + ". " + df["description"]
df["is_financial_news"] = df["section"].isin(financial_section)


df["finbert_label"] = np.nan
df["finbert_score"] = np.nan