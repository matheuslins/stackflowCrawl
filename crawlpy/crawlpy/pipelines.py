# -*- coding: utf-8 -*-
import pymongo

from os import path, getcwd
from base64 import b64decode

from scrapy.exporters import BaseItemExporter

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


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


class MongoDBPipeline(object):

    collection_name = 'crawlpy_jobs'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_SERVER'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
