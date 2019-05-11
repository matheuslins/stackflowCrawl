# -*- coding: utf-8 -*-

from stackflowCrawl.loaders import JobLoader

from stackflowCrawl.tools.text import extract_job_id
from ..constants.extraction import XPATHS_JOB


def extract_job(response):
    loader = JobLoader(response=response)
    loader.add_xpaths(XPATHS_JOB)
    loader.add_value('job_id', extract_job_id(response.url))
    loader.add_value('url', response.url)
    item = loader.load_item()
    yield item


def extract_company(spider, response):
    pass
