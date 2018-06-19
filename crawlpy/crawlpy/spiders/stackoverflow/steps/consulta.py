# -*- coding: utf-8 -*-
from scrapy.http import Request
from urllib.parse import urljoin

from .extracao import extract_job
from ..constants.consulta import XPAHS_CONSULT
from ..utils import clean_url


def consult_job(spider, response):
    jobs_urls = response.xpath(XPAHS_CONSULT['jobs_urls'])
    for job_url in jobs_urls:
        final_url = clean_url(urljoin(response.url, job_url.extract()))
        yield Request(final_url, callback=extract_job)
