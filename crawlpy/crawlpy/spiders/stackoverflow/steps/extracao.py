# -*- coding: utf-8 -*-

from crawlpy.loaders import JobLoader

from ..utils import extract_job_id
from ..constants.extracao import XPATHS_JOB


def extract_job(response):
    loader = JobLoader(response=response)
    loader.add_xpaths(XPATHS_JOB)
    loader.add_value('job_id', extract_job_id(response.url))
    loader.add_value('job_url', response.url)
    item = loader.load_item()
    return item


def extract_company(spider, response):
    pass
