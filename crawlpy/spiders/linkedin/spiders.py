# -*- coding: utf-8 -*-

from furl import furl
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from .constants.consulta import START_URL
from .steps.consulta import consult_jobs


class LinkedinSpider(CrawlSpider):
    name = 'linkedin'
    city = None
    allowed_domains = ['www.linkedin.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 0.8
    }

    def __init__(self, city=None, *args, **kwargs):
        self.city = city
        self.start_urls = [self.get_initial_url()]
        super(LinkedinSpider, self).__init__(self, *args, **kwargs)

    def get_city(self):
        return '' if self.city is None else self.city

    def get_initial_url(self):
        params = {
            'location': self.get_city(),
        }
        if not self.get_city():
            return START_URL
        return furl(START_URL).add(params).url

    def parse(self, response):
        for item in consult_jobs(response) or []:
            yield item
