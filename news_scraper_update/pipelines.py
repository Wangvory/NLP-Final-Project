# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from news_scraper_update.items import NewsScraperUpdateItem, IrrelevantNewsItem
import news_scraper_update.utils.loggerConfig as loggerConfig
import pandas as pd


logger = loggerConfig.set(__name__)


class NewsPipeline(object):
    def __init__(self):
        self.writer = pd.ExcelWriter('company_news.xlsx')

        with open('whitelist.txt','r') as f:
            self.white_list = []
            a_list = f.readlines()

        for i in range(len(a_list)):
            self.white_list.append(a_list[i].split(',')[2].strip('\n'))

        self.white_list = ','.join(self.white_list)
        self.news_list = []


    def process_item(self, item, spider):
        # if item['source'].lower() in self.white_list and isinstance(item, NewsScraperUpdateItem):
        if isinstance(item, NewsScraperUpdateItem):
            item['relevance'] = 'relevant'
        elif isinstance(item, IrrelevantNewsItem):
            item['relevance'] = 'irrelevant'
        else:
            item['relevance'] = 'advertisement'
        self.news_list.append(item)


    def close_spider(self, spider):
        df = pd.DataFrame(self.news_list)
        df.to_excel(self.writer)
        self.writer.save()

