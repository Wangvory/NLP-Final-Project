from polyglot.text import Text
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import spacy
import re
import os


def preprocess(doc):
    # doc = doc.lower()
    bad_symbols = ["\'s", '.com', ':', "\'", '\"', '(', ')', '-']
    for removable in bad_symbols:
        doc = doc.replace(removable, '')
    return doc


def filter_numbers(text):
    return re.sub(r'\d+', '', text)


def stanford_parse(text):
    parent_dir = '/'.join(( os.path.dirname(os.path.abspath(__file__))).split('/')[:-1])
    st = StanfordNERTagger(parent_dir + '/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                           parent_dir + '/stanford-ner/stanford-ner-3.9.2.jar', encoding='utf-8')
    tokenized_text = word_tokenize(text)
    classified_text = st.tag(tokenized_text)

    obj = ''
    prev_tag = 'O'

    ner_dict = {'PERSON': set(), 'LOCATION': set(), 'ORGANIZATION': set()}
    for idx, (ne, net) in enumerate(classified_text):
        # print(f"ne is: {ne}")
        # print(f"net is: {net}")
        if net != prev_tag and prev_tag != 'O':
            if obj != '':
                ner_dict[prev_tag].add(filter_numbers(obj.lower()))

            obj = ''
        elif net == prev_tag and net != 'O':
            obj = obj + ' ' + ne

        elif net != 'O' and prev_tag == 'O':
            obj = ne

            if idx == len(classified_text) - 1:
                ner_dict[net].add(filter_numbers(obj.lower()))
                break

        prev_tag = net

    # print(f"ner_dict is: {ner_dict}")
    return ner_dict


def polyglot_parse(text):
    ents = Text(text).entities
    # print(f"Entities are: {ents}")
    m = {'I-PER': 'PERSON', 'I-LOC': 'LOCATION', 'I-ORG': 'ORGANIZATION'}
    ner_dict = {'PERSON': set(), 'LOCATION': set(), 'ORGANIZATION': set()}

    # print(f"raw ner_dict is: {ner_dict}")

    for e in ents:
        entity = ' '.join(e)
        ner_dict[m[e.tag]].add(filter_numbers(entity.lower()))

    # print(f"result ner_dict is: {ner_dict}")
    return ner_dict


def spacy_parse(text):
    nlp = spacy.load('en')
    sp = nlp(text)
    spacy_entities = []
    m = {'PERSON': 'PERSON', 'ORG': 'ORGANIZATION', 'GPE': 'LOCATION'}
    ner_dict = {'PERSON': set(), 'ORGANIZATION': set(), 'LOCATION': set()}
    for ent in sp.ents:
        if ent.label_ in m:
            ner_dict[m[ent.label_]].add(filter_numbers(ent.text.lower()))

    # print(f"result ner_dict is: {ner_dict}")
    return ner_dict


def symm_agree(w1, w2):
    return w1 in w2 or w2 in w1


def get_smallest(w1, w2, w3):
    if w1 in w2 and w1 in w3:
        return w1
    elif w2 in w1 and w2 in w3:
        return w2
    else:
        return w3


# Never selects the third ranked
def get_biased_smallest(w1, w2, w3):
    if w1 in w2 and w1 in w3:
        return w1

    elif w2 in w1 and w1 in w3:
        return w1

    elif w2 in w1 and w2 in w3:
        return w2
    else:
        if w1 in w2:
            return w1
        else:
            return w2


def vote(poly, stanf, spac, ner_type):
    ner = set()

    # If poly is a subset of the others, use that

    for poly_p in poly[ner_type]:
        for stanf_p in stanf[ner_type]:
            for spac_p in spac[ner_type]:
                pst = symm_agree(poly_p, stanf_p)
                ss = symm_agree(stanf_p, spac_p)
                psp = symm_agree(poly_p, spac_p)

                if pst and ss and psp:
                    ner.add(get_biased_smallest(poly_p, stanf_p, spac_p))
                elif pst or ss or psp:
                    # Select what the actual named entity is.

                    if psp:
                        ner.add(poly_p)

                    elif pst:
                        if poly_p in stanf_p:
                            ner.add(poly_p)
                        else:
                            ner.add(stanf_p)
                    """    
                    else:
                        if stanf_p in spac_p:
                            ner.add(stanf_p)
                        else:
                            ner.add(spac_p)
                    """
    # At the end, take away all entities that are substrings of other entities

    new_set = set()
    blacklist = ['foundation', 'company', 'inc', 'corp', 'business', 'l.l.c', 'corporation', 'incorporated']
    for ne1 in ner:
        good = True
        for ne2 in ner:
            if ne1 != ne2 and ne1 in ne2:
                good = False
                break

        if good and ne1 not in blacklist:
            new_set.add(ne1)

    return new_set


def get_named_entities(Doc):
    doc = preprocess(Doc)
    try:
        a = polyglot_parse(doc)
        b = stanford_parse(doc)
        c = spacy_parse(doc)
    except:
        return []

    persons = vote(a, b, c, 'PERSON')
    new_person = set()
    bad_person = set()
    for p in persons:
        if len(p.split(' ')) == 4:
            new_person.update([' '.join(p.split(' ')[:2]), ' '.join(p.split(' ')[2:])])
            bad_person.add(p)
        if len(p.split(' ')) == 1:
            bad_person.add(p)

    for p in bad_person:
        persons.remove(p)
    for p in new_person:
        persons.add(p)

    locations = vote(a, b, c, 'LOCATION')
    orgs = vote(a, b, c, 'ORGANIZATION')

    orgs = set([n for n in orgs if len(n.split(' ')) < 5])

    return list(map(lambda p: p.title(), persons)), list(map(lambda l: l.title(), locations)), list(
        map(lambda o: o.title(), orgs))