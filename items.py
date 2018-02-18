# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class MicrocapcollectorItem(scrapy.Item):
    symbol = scrapy.Field()
    name = scrapy.Field()
    market_cap = scrapy.Field()
    volume = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()


class MicrocapcalculatorItem(scrapy.Item):
    symbol = scrapy.Field()
    supply = scrapy.Field()
