# -*- coding: utf-8 -*-

from scrapy.http import Request

from ..constants.consulta import XPAHS_CONSULT
from ..steps.extracao import extract_job


def consult_jobs(response):
    jobs_urls = response.xpath(XPAHS_CONSULT['jobs_urls'])
    for job_url in jobs_urls:
        final_url = ''
        yield Request(final_url, callback=extract_job)

    has_pagination = response.xpath(XPAHS_CONSULT['pagination'])
    if has_pagination:
        yield pagination(response, has_pagination)


def pagination(response, has_pag):
    pass
