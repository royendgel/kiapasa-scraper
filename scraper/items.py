# -*- coding: utf-8 -*-

from scrapy import Item, Field


class Ad(Item):
    title = Field()
    text = Field()
    price = Field()
    clicks = Field()
    reference = Field()
    link = Field()
