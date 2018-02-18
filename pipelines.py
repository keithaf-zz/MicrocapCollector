# -*- coding: utf-8 -*-
import sys
from .processors import *
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


class MicrocapcollectorPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        if spider.name == 'mcc1':
            self.file = open('MicrocapCollector/spiders/data/data1.csv', 'w+b')
        if spider.name == 'mcc2':
            self.file = open('MicrocapCollector/spiders/data/data2.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file, delimiter=',')
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if spider.name == 'mcc1':
            raw_data = [item['symbol'], item['name'], item['market_cap'], item['volume'], item['price'], item['link']]

            for y in raw_data:
                for x in raw_data:
                    if len(x) != len(y):
                        sys.exit(1)

            raw_data = StringProcessor(raw_data, [2, 3, 4])
            raw_data = MCProcessor(raw_data)
            raw_data = MCVProcessor(raw_data)
            raw_data = Flattener(raw_data)
            for i in range(0, len(raw_data[0])):
                item['symbol'] = raw_data[0][i]
                item['name'] = raw_data[1][i]
                item['market_cap'] = raw_data[2][i]
                item['volume'] = raw_data[3][i]
                item['price'] = raw_data[4][i]
                item['link'] = raw_data[5][i]
                self.exporter.export_item(item)
            return item
        if spider.name == 'mcc2':
            raw_data = [item['symbol'], item['supply']]
            raw_data = StringProcessor(raw_data, [1])
            raw_data = CSTSProcessor(raw_data)

            item['symbol'] = raw_data[0][0].replace('(', '').replace(')', '')
            item['supply'] = raw_data[1]
            self.exporter.export_item(item)
            return item
