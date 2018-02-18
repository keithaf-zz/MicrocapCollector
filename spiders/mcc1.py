# -*- coding: utf-8 -*-
import scrapy

from ..items import MicrocapcollectorItem
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose


class MicrocapcollectorItemLoader(ItemLoader):
    review_in = MapCompose(lambda x: x.replace("\n", " "))
    review_out = Join()


class MicrocapcollectorSpider(scrapy.Spider):
    name = "mcc1"
    allowed_domains = ["https://coinmarketcap.com/"]

    start_urls = ["https://coinmarketcap.com/all/views/all/"]

    def parse(self, response):
        loader = MicrocapcollectorItemLoader(item=MicrocapcollectorItem(), response=response)

        loader.add_xpath('symbol', '//td[@class="text-left col-symbol"]/text()')
        loader.add_xpath('name', '//a[@class="currency-name-container"]/text()')
        loader.add_xpath('market_cap', '//td[@class="no-wrap market-cap text-right"]/text()')
        loader.add_xpath('volume', '//a[@class="volume"]/text()')
        loader.add_xpath('price', '//a[@class="price"]/text()')
        loader.add_xpath('link', '//a[@class="currency-name-container"]/@href')

        yield loader.load_item()

