import csv
import collections


def preprocess(doc):
    doc = doc.lower()
    bad_symbols = ['.com', '.', ':', '!', '?', ',', "\'", '\"', '(', ')', 'nyse', 'nasdaq', 'business wire']
    for removable in bad_symbols:
        doc = doc.replace(removable, '')
    return doc


def get_tags():
    f = open('./news_scraper_update/data/tags.csv')
    cr = csv.reader(f)
    w2t = {}
    tag2id = {}
    count = 0
    for row in cr:
        tag = row[0]
        tag2id[tag] = count
        for idx in range(1, len(row)):
            if row[idx] != '' and row[idx] is not None:
                w2t[row[idx].strip().lower()] = tag
        count += 1
    return w2t, tag2id


def is_good_doc(doc):
    count = collections.Counter()
    word2tag, _ = get_tags()
    for keyword in word2tag:
        if (len(keyword) <= 3 and ' ' + keyword + ' ' in doc) or (len(keyword) >= 4 and ' ' + keyword in doc):
            count[keyword] += 1

    if sum(count.values()) > 1:
        return True
    else:
        return False


def relevance_score(doc, company_name, ticker):

    if (' ' + ticker + ' ' in doc) or ('(' + ticker + ')' in doc) or (':' + ticker + ')' in doc) or (
            ' ' + ticker + ')' in doc):
        return 2
    # Check if company name in doc in two ways.
    bad_endings = ['inc', 'ltd', 'corp', 'plc', 'cp', 'cpation', 'lp']
    score = 0
    company_name = company_name.split(' ')
    if company_name[0] == 'The':
        company_name = company_name[1:]

    if company_name[-1].lower() in bad_endings:
        company_name = company_name[:-1]

    company_name2 = ' '.join(company_name)

    name_in_doc = doc.count(company_name2)

    if name_in_doc >= 2:
        return 2

    if name_in_doc >= 1 and len(company_name) >= 3:
        return 2

    else:
        score += 1 if name_in_doc > 0 else 0

    if len(company_name) == 1 and score == 0:
        return 0

    # Check 2-grams if length > 2
    if len(company_name) >= 3:
        two_grams = [company_name[i:i + 2] for i in range(len(company_name) - 1)]
        gram_appearances = sum(list(map(lambda gram: doc.count(' '.join(gram)), two_grams)))
        if gram_appearances == 0:
            return 0

        score += 2 if gram_appearances >= 2 else 1

    if score == 0:
        return 0

    score += is_good_doc(preprocess(doc))

    return score
