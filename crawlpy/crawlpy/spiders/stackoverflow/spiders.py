# -*- coding: utf-8 -*-
import scrapy


class StackOverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    allowed_domains = ['https://stackoverflow.com']
    start_urls = ['http://https://stackoverflow.com/']

    def parse(self, response):
        pass
