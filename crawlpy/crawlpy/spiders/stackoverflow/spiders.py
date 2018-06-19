# -*- coding: utf-8 -*-
import re

from furl import furl
from scrapy.spiders import Spider

from .constants.consulta import START_URL
from .steps.consulta import consult_job


class StackOverflowSpider(Spider):
    name = 'stackoverflow'
    city = None
    distance = None
    initial_step = consult_job
    allowed_domains = ['stackoverflow.com']
    custom_settings = {
        'CONCURRENT_REQUESTS': 5
    }

    def __init__(self, city=None, distance=None, *a, **kw):
        self.city = city
        self.distance = distance

        if distance and (city is None):
            raise ValueError(
                "Was defined the distance, but not the city. Try again"
            )
        self.start_urls = [self.get_initial_url()]
        super(StackOverflowSpider, self).__init__(*a, **kw)

    def get_distance(self):
        return '20' if self.distance is None else self.distance

    def get_city(self):
        return '' if self.city is None else self.city

    def get_initial_url(self):
        params = {
            'sort': 'i',
            'u': 'Km',
            'd': self.get_distance(),
            'l': self.get_city()
        }
        if not self.get_city():
            return START_URL
        return furl(START_URL).add(params).url

    def parse(self, response):
        initial_step = self.initial_step(response)
        for item in initial_step or []:
            yield item
