# -*- coding: utf-8 -*-
import scrapy


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    allowed_domains = ['www.linkedin.com']
    start_urls = ['http://www.linkedin.com/']

    def parse(self, response):
        pass
