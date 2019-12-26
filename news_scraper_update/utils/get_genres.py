
import collections
import numpy as np
from sklearn.externals import joblib
from news_scraper_update.utils.relevance_score import get_tags, preprocess


def tag_documents(doc, bad_tags=[]):
    word2tag, _ = get_tags()
    tag = ''
    c = collections.Counter()
    for word in word2tag:
        if word2tag[word] in bad_tags:
            continue
        if (len(word) <= 3 and ' ' + word + ' ' in doc) or (len(word) >= 4 and ' ' + word in doc):
            c[word2tag[word]] += 1
    if len(c) > 0:
        tag = max(c, key=c.get)
    else:
        tag = 'undefined'
    return tag


def get_genres(key_event, tfidf, tagger_model):
    doc = key_event['title'] + ' ' + key_event['description']
    small_topics = ['Cloud Computing', 'Automotive', 'Machine Learning', 'Intellectual Property', 'Startup', 'Trade',
                    'Corruption', 'Taxation', 'Credit Market', 'Fraud', 'Blockchain', 'Recession', 'Economic data',
                    'Fixed Income', 'Emerging market', 'Technical Analysis', 'Antitrust', 'Tariff']
    best_tag = tag_documents(doc)
    vec = tfidf.transform([preprocess(doc)]).toarray()
    probs = tagger_model.predict_proba(vec).flatten()
    l1 = np.argsort(probs)
    l = [ i for i, prob in enumerate(probs) if prob >= 0.19 ]
    if len(l) == 0 and l1[-1] > 0.091:
        l = [l1[-1]]
        if probs[l1[-1]] <= .2 and probs[l1[-2]] > .1:
            l.append(l1[-2])
    if len(l) == 1 and probs[l1[-1]] >= .43 and probs[l1[-2]] >= .1:
        l.append(l1[-2])
        if probs[l1[-3]] >= .095:
            l.append(l1[-3])
    doctags = list(tagger_model.classes_[l])
    if best_tag in small_topics and best_tag not in doctags:
        doctags.append(best_tag)
    return doctags