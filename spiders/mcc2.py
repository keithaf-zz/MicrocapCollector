# -*- coding: utf-8 -*-
import pandas as pd
import scrapy
import datetime

from pandas.errors import EmptyDataError
from ..items import MicrocapcalculatorItem
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose


class MicrocapcalculatorItemLoader(ItemLoader):
    review_in = MapCompose(lambda x: x.replace("\n", " "))
    review_out = Join()


class MicrocapcalculatorSpider(scrapy.Spider):
    name = "mcc2"
    allowed_domains = ["https://coinmarketcap.com/"]

    try:
        df = pd.read_csv('MicrocapCollector/spiders/data/data1.csv')
        url_arr = list(df['link'])
        for i in range(0, len(url_arr)):
            url_arr[i] = "https://coinmarketcap.com" + url_arr[
                i] + 'historical-data/?start=20100429&end=' + datetime.datetime.now().strftime("%Y%m%d")
    except (FileNotFoundError, EmptyDataError):
        url_arr = []

    start_urls = url_arr

    def parse(self, response):
        loader = MicrocapcalculatorItemLoader(item=MicrocapcalculatorItem(), response=response)

        loader.add_xpath('symbol', '//small[@class="bold hidden-xs"]/text()')
        loader.add_xpath('supply', '//div[@class="coin-summary-item-detail details-text-medium"]/text()[1]')

        yield loader.load_item()
