import firebase_admin
import pymongo

from pymongo import InsertOne
from decouple import config
from os import path, getcwd
from scrapy.exporters import BaseItemExporter
from scrapy.exceptions import DropItem, NotConfigured
from firebase_admin import credentials
from firebase_admin import db

from crawlpy.processors import HandleAPI


class DuplicatesJobPipeline(object):
    
    def __init__(self):
        self.jobs = set()

    def item_pipeline(self, item, spider):
        import ipdb; ipdb.set_trace()
        id_job = item.get('id')

        if not id_job:
            raise DropItem('Job not found. Item dropped')

        if id_job in self.jobs:
            self.inc_duplicados(spider)
            raise DropItem('Duplicated job')
        else:
            self.jobs.add(key)

        return item

    def inc_duplicados(self, spider):
        stat = spider.crawler.stats.get_value('crawlpy/jobs') or {}
        stat['duplicados'] = stat.get('duplicados', 0) + 1
        spider.crawler.stats.set_value('crawlpy/jobs', stat)


class FirebasePipeline(BaseItemExporter):
    
    def load_spider(self, spider):
        self.crawler = spider.crawler
        self.settings = spider.settings

    def open_spider(self, spider):
        self.load_spider(spider)
        filename = path.normpath(path.join(getcwd(), 'firebase_secrets.json'))
        configuration = {
            'credential': credentials.Certificate(filename),
            'options': {'databaseURL': self.settings['FIREBASE_DATABASE']}
        }

        firebase_admin.initialize_app(**configuration)
        self.ref = db.reference(self.settings['FIREBASE_REF'])

    def process_item(self, item):
        item = dict(self._get_serialized_fields(item))
        initial_path = item.pop('job_id')

        for key, value in item.items():
            self.ref.child(initial_path + '/' + key).set(value)
        return item

    def close_spider(self, spider):
        pass


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
