import news_scraper_update.settings as settings
import pymysql
from cleanco import cleanco
import re
import news_scraper_update.utils.loggerConfig as loggerConfig
import pandas as pd

logger = loggerConfig.set(__name__)


def create_search_words(cpy_name):
    redundant_key = ['Company', 'Group', 'Holdings', 'Corp', 'Holding', 'Corporation', 'plc', 'Inc', 'Class', 'com']
    cpy_name = str(cpy_name)
    if cpy_name == 'Snap Inc. Class A':
        return 'Snap Inc'
    cleanco_ob = cleanco(cpy_name)
    cleaned_name = cleanco_ob.clean_name()
    cleaned_name = re.sub('[^A-Za-z0-9\']', ' ', cleaned_name)
    cleaned_name = cleaned_name.split()
    cur = len(cleaned_name)
    for idx, name in enumerate(cleaned_name):
        if name in redundant_key:
            cur = idx
            break
    cleaned_name = ' '.join(cleaned_name[:cur])
    return cleaned_name


def get_companies():
    companies = pd.read_excel('companies.xlsx')
    name = companies['Name']
    tickers = companies['Ticker']
    results = [[company[0], create_search_words(company[1])] for company in list(zip(tickers, name))]
    return results
