import pymongo

from pymongo import InsertOne
from decouple import config
from scrapy.exceptions import DropItem, NotConfigured

from stackflowCrawl.processors import HandleAPI


class DuplicatesJobPipeline(object):
    
    def __init__(self):
        self.jobs = set()

    def item_pipeline(self, item, spider):
        id_job = item.get('id')

        if not id_job:
            raise DropItem('Job not found. Item dropped')

        if id_job in self.jobs:
            self.inc_duplicated(spider)
            raise DropItem('Duplicated job')
        else:
            self.jobs.add(key)

        return item

    def inc_duplicated(self, spider):
        stat = spider.crawler.stats.get_value('stackflowCrawl/jobs') or {}
        stat['duplicated'] = stat.get('duplicated', 0) + 1
        spider.crawler.stats.set_value('stackflowCrawl/jobs', stat)


class BaseDBPipeline(object):
    bulk_size = 100

    collection_name = config(
        'COLLECTION_NAME', cast=str, default='jobs_crawled')

    def __init__(self, settings):
        self.bulk = []
        self.mongo_uri = settings.get('MONGODB_SERVER')
        self.mongo_db = settings.get('MONGO_DATABASE', 'items')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


class MongoDBPipeline(BaseDBPipeline):
    
    def __init__(self, settings, *args, **kwargs):
        if not settings.getbool('MONGODB_PIPELINE_ENABLE'):
            raise NotConfigured
        super(MongoDBPipeline, self).__init__(settings, *args, **kwargs)

    def call_api(self):
        api = HandleAPI(self.bulk)
        api.send()

    def process_bulk_item(self, items):
        operations = [InsertOne(dict(item)) for item in items]
        try:
            self.db[self.collection_name].bulk_write(operations)
        except pymongo.errors.BulkWriteError as bwe:
            raise bwe

    def process_item(self, item, spider):
        self.bulk.append(dict(item))
        if len(self.bulk) >= self.bulk_size:
            self.process_bulk_item(self.bulk)
            self.call_api()
            self.bulk = []
        return item
    
    def close_spider(self):
        if len(self.bulk) < self.bulk_size:
            for item in self.bulk:
                self.db[self.collection_name].insert_one(dict(item))
            self.call_api()
        self.client.close()
