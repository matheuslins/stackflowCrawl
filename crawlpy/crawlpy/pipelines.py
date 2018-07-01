# -*- coding: utf-8 -*-

import firebase_admin
import logging
import pymongo

from base64 import b64decode
from decouple import config
from os import path, getcwd
from scrapy.exporters import BaseItemExporter
from scrapy.exceptions import DropItem, NotConfigured
from scrapy import signals
from firebase_admin import credentials
from firebase_admin import db

from crawlpy.processors import HandleAPI


class DuplicatesJobPipeline(object):
    
    def __init__(self):
        self.jobs = set()

    def item_pipeline(self, item, spider):
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

    def process_item(self, item, spider):
        item = dict(self._get_serialized_fields(item))
        initial_path = item.pop('job_id')

        for key, value in item.items():
            self.ref.child(initial_path + '/' + key).set(value)
        return item

    def close_spider(self, spider):
        pass


class BaseDBPipeline(object):

    collection_name = config(
        'COLLECTION_NAME', cast=str, default='jobs_crawled')

    def __init__(self, settings):
        self.mongo_uri = settings.get('MONGODB_SERVER')
        self.mongo_db = settings.get('MONGO_DATABASE', 'items')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()


class MongoDBPipeline(BaseDBPipeline):
    
    def __init__(self, settings, *args, **kwargs):
        super(MongoDBPipeline, self).__init__(settings, *args, **kwargs)

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


class APIPipeline(BaseDBPipeline):
    
    def __init__(self, settings, *args, **kwargs):
        if not settings.getbool('API_PIPILINE_ENABLE'):
            raise NotConfigured
        super(APIPipeline, self).__init__(settings, *args, **kwargs)

    def close_spider(self, spider):
        cursor = self.db[self.collection_name].find({})
        api = HandleAPI(cursor)
        api.send()
        self.client.close()

# class MongoBulkInsert(object):

#     logger = logging.getLogger(__name__)
#     collection_name = 'crawlpy_jobs'
#     bulk_size = 100

#     def __init__(self, crawler):
#         self.mongo_uri = crawler.settings.get('MONGODB_SERVER')
#         self.mongo_db = crawler.settings.get('MONGO_DATABASE', 'items')
#         self.crawler = crawler
#         self.bulk = []

#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls(crawler)
#         crawler.signals.connect(
#             pipeline.spider_closed,
#             signal=signals.spider_closed)
#         return pipeline

#     def open_spider(self, spider):
#         import ipdb; ipdb.set_trace()
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]

#     def process_bulk_item(self, items):
#         operations = []
#         for item in items:
#             data = dict(item)
#             operations.append(self.make_write_recipe(data))
#         try:
#             database_collection = getattr(self, 'collection_name')
#             self.check_index(self.db, database_collection)
#             self.db[database_collection].bulk_write(operations)
#         except pymongo.errors.BulkWriteError as bwe:
#             raise bwe

#     def make_write_recipe(self, item):
#         import ipdb; ipdb.set_trace()
#         return pymongo.UpdateOne(item['id'], {'$set': item}, upsert=True)

#     def item_pipeline(self, item, spider):
#         import ipdb; ipdb.set_trace()
#         item = super(MongoBulkInsert, self).item_pipeline(item, spider)
#         spider.logger.info('Scraped one item.')
#         self.bulk.append(item)
#         if len(self.bulk) >= self.bulk_size:
#             spider.logger.info('Sending items to database.')
#             self.process_bulk_item(self.bulk)
#             self.bulk = []
#         return item

#     def spider_closed(self, spider, *args, **kwargs):
#         import ipdb; ipdb.set_trace()
#         if self.bulk:
#             self.logger.info('Sending items to database.')
#             if not hasattr(self, 'database_collection'):
#                 self.collection_name = spider.collection_name
#             self.process_bulk_item(self.bulk)
#             self.bulk = []
