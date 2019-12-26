import scrapy
import math
import json
import pandas as pd

from scrapy import Request
from datetime import datetime, timedelta

from news_scraper_update.utils.get_companies import get_companies
from news_scraper_update.utils.relevance_score import relevance_score, preprocess
from news_scraper_update.utils.get_sentiment import get_sentiment
from news_scraper_update.utils.get_genres import get_genres
from news_scraper_update.utils.get_tags import get_named_entities
from news_scraper_update.items import NewsScraperUpdateItem, IrrelevantNewsItem, AdsItem
from news_scraper_update.utils import constants
from sklearn.externals import joblib
from keras.models import model_from_json
import news_scraper_update.utils.loggerConfig as loggerConfig

logger = loggerConfig.set(__name__)


class NewsSpider(scrapy.Spider):
    name = 'nlp_news'
    custom_settings = {
        'ITEM_PIPELINES': {
            'news_scraper_update.pipelines.NewsPipeline': 300
        }
    }

    def __init__(self):
        logger.info("init news spider...\n")

        self.companies = get_companies()
        self.companies = self.companies
        logger.info("companies are {}".format(self.companies))

        self.hour_before = str((datetime.now() - timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%S"))
        self.hour_now = str((datetime.now()).strftime("%Y-%m-%dT%H:%M:%S"))


        # 自己做model
        logger.info('loading models...\n')
        self.filter_tfidf = joblib.load("./news_scraper_update/models/tfidf_model_fully_conn1")

        with open('./news_scraper_update/models/fully_conn1', 'r') as f:
            self.filter_model = model_from_json(f.read())
        self.filter_model.load_weights('./news_scraper_update/models/model.h5')

        self.tfidf = joblib.load("./news_scraper_update/models/tfidf_vec")
        self.tagger_model = joblib.load("./news_scraper_update/models/mnb_classifier")
        logger.info('models sucessfully loaded!\n')

        self.df_tags = pd.read_csv('./news_scraper_update/data/company_search.csv', index_col=False)
        self.ad_sources = constants.AD_BLOCK_SOURCES


    def start_requests(self):
        logger.info('starting requests..\n')
        start_url = "https://newsapi.org/v2/everything?q={clean_name}&from={hour_before}&to={hour_now}&language=en" + \
                    "&excludeDomains=9to5google.com,9to5toys.com,bleacherreport.com,boardgamegeek.com,boardingarea.com,boardingarea.com,checkpoint.com,collider.com,commingsoon.net,commonsensewithmoney.com,deadline.com,dealcatcher.com,dealnews.com,disneyfashionista.com,elitedaily.com,extratv.com,hotnewhiphop.com,hotukdeals.com,insideflyer.com,internetmarketinginc.com,ipadinsight.com,jeffsetter.com,justjared.com,kicksonfire.com,kinja.com,livingrichwithcoupons.com,loyaltylobby.com,millionmilesecrets.com,moneysavingmom.com,onemileatatime.com,ozbargain.com.au,qooah.com,queenbeecoupons.com,redflagdeals.com,road.cc,secretflying.com,slickdeals.net,smartcanucks.ca,smartinsights.com,socialmediaexaminer.com,sonyalpharumors.com,southernsavers.com,sweettoothsweetlife.com,thepointsguy.com,trustedreviews.com,yourmileagemayvary.net" + \
                    "&pageSize=100&page={page_num}&sortBy=publishedAt&apiKey=41a65dbf853849bf99fff3797a2baef2"

        for company in self.companies:
            ticker = company[0]
            clean_name = company[1]
            logger.info("start_requests() ticker is: {} \t company_clean_name is: {}".format(ticker, clean_name))
            url = start_url.format(clean_name=clean_name, hour_before=self.hour_before, hour_now=self.hour_now,
                                   page_num=1)
            yield Request(url=url, callback=self.parse, dont_filter=True,
                          meta={'ticker': ticker, 'company_name': clean_name, 'page_num': 1, 'start_url': start_url})


    def parse(self, response):
        ticker = response.meta['ticker']
        company_name = response.meta['company_name']
        start_url = response.meta['start_url']

        page_num = response.meta['page_num']
        logger.info("parse() Current Page is: {}".format(page_num))

        result = json.loads(response.text)

        total_results = result["totalResults"]
        total_page = math.ceil(total_results/100)
        logger.info("parse() Total Page is: {}".format(total_page))

        # parse article item and yield to pipeline
        for article in result['articles']:
            item = self.parse_article(article, ticker, company_name)

            if isinstance(item, NewsScraperUpdateItem) or isinstance(item, IrrelevantNewsItem):
                item['sentiment'] = get_sentiment(article)
                item['event_ticker'] = ticker

                logger.info("parse() get_genres...")

                tags_genres = get_genres(article, self.tfidf, self.tagger_model)
                event_genre = []
                for t in tags_genres:
                    event_genre.append(t)
                item['event_genre'] = event_genre
                logger.info("parse() tags_genres are: {}".format(tags_genres))

                try:
                    tags_sector = self.df_tags[self.df_tags['symbol'] == ticker]['sector'].values[0]
                    tags_sector = str(tags_sector).title()
                except Exception as e:
                    logger.error("parse() Error getting tags_sector: {}".format(e))
                    logger.error('parse() NO sector for {}\n'.format(ticker))
                    tags_sector = ''
                item['event_sector'] = tags_sector

                try:
                    people, locs, orgs = get_named_entities(article['description'])
                except Exception as e:
                    logger.error("parse() Error getting named entities: {}".format(e))
                    logger.error('parse() NO named entities for ' + ticker +'\n')
                    people, locs, orgs = [], [], []

                event_person = []
                event_location = []
                event_organization = []

                for ne in people:
                    event_person.append(ne)
                for ne in locs:
                    event_location.append(ne)
                for ne in orgs:
                    event_organization.append(ne)

                item['event_person'] = event_person
                item['event_location'] = event_location
                item['event_organization'] = event_organization


            yield item

        # Next Pages
        next_page = page_num + 1
        if next_page <= total_page:
            logger.info("parse() Next Page is: {}".format(next_page))
            url = start_url.format(clean_name=company_name, hour_before=self.hour_before, hour_now=self.hour_now, page_num=next_page)
            logger.info("parse() Next Page url is: {}".format(url))
            yield response.follow(url=url, callback=self.parse, dont_filter=True, meta={'ticker': ticker, 'company_name': company_name, 'page_num': next_page, 'start_url': start_url})

    def parse_article(self, article, ticker, company_name):
        if article['title'] is None:
            article['title'] = ''
        if article['description'] is None:
            article['description'] = ''
        doc = article['title'] + " " + article['description']
        score = relevance_score(doc, company_name, ticker)
        prediction = self.filter_model.predict(self.filter_tfidf.transform([preprocess(doc)]))[0][0]

        if article['source']['name'] in self.ad_sources:
            item = AdsItem()
            logger.info('parse_article() article is an ad!\n')
        elif score == 0 or (score == 1 and prediction < 0.4):
            item = IrrelevantNewsItem()
            logger.info('parse_article() article is an irrelevant news!\n')
        else:
            item = NewsScraperUpdateItem()
            logger.info('parse_article() article is a relevant news!\n')

        item['title'] = article['title']
        item['ticker'] = ticker
        item['author'] = article['author'] if article['author'] is not None else ''
        item['description'] = article['description']
        item['source'] = article['source']['name'] if article['source']['name'] is not None else ''
        item['url'] = article['url'] if article['url'] is not None else ''
        item['content'] = article['content']
        item['published_at'] = datetime.strptime(article['publishedAt'],
                                                 "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M:%SZ")
        item['date'] = datetime.strptime(item['published_at'],
                                                 "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d')
        item['minute'] = datetime.strptime(item['published_at'],
                                                 "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M:%S")
        item['timestamp'] = int(datetime.strptime(item['published_at'],
                                                  "%Y-%m-%dT%H:%M:%SZ").timestamp()) * 1000
        logger.info("parse_article() return item...")
        return item

