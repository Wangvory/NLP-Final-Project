# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:52:55 2019

@author: Li Xiang
"""
from joblib import load
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def get_sentiment(key_events):
    text = key_events["title"] + key_events["description"]
    doc = load('news_scraper_update/models/documents.jbl')
    vectorizer = CountVectorizer(max_features=2500, stop_words="english")
    vectorizer.fit(doc)
    model = load('news_scraper_update/models/bayes-all-words-raw-counts.jbl')
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', '' , text)
    text = re.sub(r'\s+', ' ', text)
    text_matrix = vectorizer.transform([text]).toarray()
    text_matrix = pd.DataFrame(text_matrix)
    return model.predict(text_matrix)[0]