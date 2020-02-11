import pytz
import hashlib
from datetime import datetime
from geopy import geocoders

from scrapy.exceptions import DropItem, NotConfigured
from elasticsearch.helpers import bulk

from stackflowCrawl.database import config_client
from stackflowCrawl.settings import GEOCODE_USERNAME, BULK_SIZE


class DuplicatesJobPipeline(object):
    
    def __init__(self):
        self.jobs = set()

    def process_item(self, item, spider):
        url_job = item.get('url')

        if not url_job:
            raise DropItem('Job not found. Item dropped')

        if url_job in self.jobs:
            self.inc_duplicated(spider)
            raise DropItem('Duplicated job')
        else:
            self.jobs.add(url_job)
            return item

    def inc_duplicated(self, spider):
        stat = spider.crawler.stats.get_value('stackflowCrawl/jobs') or {}
        stat['duplicated'] = stat.get('duplicated', 0) + 1
        spider.crawler.stats.set_value('stackflowCrawl/jobs', stat)


class BaseDBPipeline(object):
    bulk_size = BULK_SIZE

    def __init__(self, settings):
        self.bulk = []
        self.es_index = settings.get('ES_INDEX')
        self.tz = pytz.timezone('America/Sao_Paulo')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.client = config_client()
        self.gn = geocoders.GeoNames(username=GEOCODE_USERNAME)


class ElasticSearchPipeline(BaseDBPipeline):
    
    def __init__(self, settings, *args, **kwargs):
        if not settings.getbool('ES_PIPELINE_ENABLE'):
            raise NotConfigured
        super(ElasticSearchPipeline, self).__init__(settings, *args, **kwargs)

    @staticmethod
    def generate_id(item):
        return hashlib.sha1(
            f"{item['url']}_{item['job_id']}".encode()
        ).hexdigest()[:20]

    def process_bulk_item(self, items):
        def insert_items():
            for item in items:
                yield {
                    "_index": self.es_index,
                    "_type": "job",
                    "_id": self.generate_id(item),
                    '_op_type': 'create',
                    '_source': item
                }

        bulk(self.client, insert_items())

    def process_item(self, item, spider):
        dict_item = dict(item)
        dict_item.update({
            "dateTime": datetime.now(tz=self.tz).isoformat(),
            "location": dict_item['location'].replace('– ', "")
        })
        self.bulk.append(dict_item)
        if len(self.bulk) >= self.bulk_size:
            self.process_bulk_item(self.bulk)
            self.bulk = []
        return item
    
    def close_spider(self, spider):
        if len(self.bulk) < self.bulk_size:
            self.process_bulk_item(self.bulk)
            self.bulk = []
