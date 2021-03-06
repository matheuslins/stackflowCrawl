from furl import furl
from scrapy import Spider

from stackflowCrawl.tools.wrappers import property_collection
from .constants.consult import START_URL
from .steps.consult import consult_job


class StackOverflowSpider(Spider):
    name = 'stkflow'
    city = None
    distance = None
    job = None
    allowed_domains = ['stackoverflow.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'ES_PIPELINE_ENABLE': True
    }

    def __init__(self, city=None, distance=None, job=None, *a, **kw):
        self.city = city
        self.distance = distance
        self.job = job

        if distance and (city is None):
            raise ValueError(
                "Was defined the distance, but not the city. Try again"
            )
        self.start_urls = [self.get_initial_url()]
        super(StackOverflowSpider, self).__init__(*a, **kw)

    def get_distance(self):
        return self.distance or '20'
    
    @property_collection
    def get_job(self):
        return self.job

    @property_collection
    def get_city(self):
        return self.city

    def get_initial_url(self):
        params = {
            'u': 'Km',
            'd': self.get_distance(),
            'l': self.get_city(),
            'q': self.get_job()
        }
        if not self.get_city():
            return START_URL
        return furl(START_URL).add(params).url

    def parse(self, response):
        for item in consult_job(response) or []:
            yield item
