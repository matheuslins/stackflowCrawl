import pytz
import hashlib
from datetime import datetime

from scrapy.exceptions import DropItem, NotConfigured
from elasticsearch.helpers import bulk

from stackflowCrawl.database import config_client
from stackflowCrawl.settings import BULK_SIZE


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
    client = None

    def __init__(self, settings):
        self.bulk = []
        self.es_index = settings.get('ES_INDEX')
        self.tz = pytz.timezone('America/Sao_Paulo')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)


class ElasticSearchPipeline(BaseDBPipeline):
    
    def __init__(self, settings, *args, **kwargs):
        if not settings.getbool('ES_PIPELINE_ENABLE'):
            raise NotConfigured
        super(ElasticSearchPipeline, self).__init__(settings, *args, **kwargs)

    def open_spider(self, spider):
        self.client = config_client()

    @staticmethod
    def generate_id(item):
        return hashlib.sha1(
            f"{item['url']}_{item['jobId']}".encode()
        ).hexdigest()[:40]

    def insert_items(self):
        date_timezone = datetime.now(tz=self.tz).date()
        for item in self.bulk:
            yield {
                "_index": f"{self.es_index}-{date_timezone}",
                "_type": "job",
                "_id": self.generate_id(item),
                '_op_type': 'create',
                '_source': item
            }

    def process_item(self, item, spider):
        dict_item = dict(item)
        dict_item.update({
            "dateTime": datetime.now(tz=self.tz).isoformat(),
            "location": dict_item['location'].replace('– ', "")
        })
        self.bulk.append(dict_item)
        if len(self.bulk) >= self.bulk_size:
            bulk(self.client, self.insert_items())
            self.bulk = []
        return item
    
    def close_spider(self, spider):
        if len(self.bulk) < self.bulk_size:
            bulk(self.client, self.insert_items())
            self.bulk = []
