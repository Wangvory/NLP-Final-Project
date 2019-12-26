# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperUpdateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    ticker = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    published_at = scrapy.Field()
    sentiment = scrapy.Field()
    timestamp = scrapy.Field()
    date = scrapy.Field()
    minute = scrapy.Field()
    tags = scrapy.Field()
    news_id = scrapy.Field()
    event_ticker = scrapy.Field()
    event_sector = scrapy.Field()
    event_genre = scrapy.Field()
    event_organization = scrapy.Field()
    event_location = scrapy.Field()
    event_person = scrapy.Field()
    relevance = scrapy.Field()


class IrrelevantNewsItem(scrapy.Item):
    title = scrapy.Field()
    ticker = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    published_at = scrapy.Field()
    timestamp = scrapy.Field()
    date = scrapy.Field()
    minute = scrapy.Field()
    news_id = scrapy.Field()
    event_ticker = scrapy.Field()
    event_sector = scrapy.Field()
    event_genre = scrapy.Field()
    event_organization = scrapy.Field()
    event_location = scrapy.Field()
    event_person = scrapy.Field()
    relevance = scrapy.Field()
    sentiment = scrapy.Field()


class AdsItem(scrapy.Item):
    title = scrapy.Field()
    ticker = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    published_at = scrapy.Field()
    timestamp = scrapy.Field()
    date = scrapy.Field()
    minute = scrapy.Field()
    event_ticker = scrapy.Field()
    event_sector = scrapy.Field()
    event_genre = scrapy.Field()
    event_organization = scrapy.Field()
    event_location = scrapy.Field()
    event_person = scrapy.Field()
    relevance = scrapy.Field()
    sentiment = scrapy.Field()

