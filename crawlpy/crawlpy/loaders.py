# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join
from crawlpy import processors
from crawlpy.items import JobItem


class BaseLoader(ItemLoader):
    default_input_processor = processors.DefaultInputProcessor()
    default_output_processor = processors.DefaultOutputProcessor()

    def add_xpaths(self, fields, raw=None, re={}):
        if raw:
            raw_fields = self.item.setdefault('raw', {})

        for field, args in fields.items():
            if not field or field.startswith('_'):
                continue

            args, kwargs = self._resolve_args(args)
            if field in re:
                kwargs.setdefault('re', re[field])

            self.add_xpath(field, *args, **kwargs)
            if raw is True or raw and field in raw:
                raw_value = self.get_xpath(args[0], Join())
                if raw_value:
                    raw_fields[field] = self.get_xpath(args[0], Join())

    def add_values(self, fields):
        for field, args in fields.iteritems():
            if not field or field.startswith('_'):
                continue

            args, kwargs = self._resolve_args(args)
            self.add_value(field, *args, **kwargs)

    def _resolve_args(self, args):
        kwargs = {}
        if not isinstance(args, tuple):
            args = (args,)
        elif isinstance(args[-1], dict):
            args, kwargs = args[:-1], args[-1]
        return args, kwargs


class JobLoader(BaseLoader):
    default_item_class = JobItem
