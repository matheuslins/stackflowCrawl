# -*- coding: utf-8 -*-

from scrapy.http import Request
from urllib.parse import urljoin
from furl import furl

from .extracao import extract_job
from ..utils import clean_url
from ..constants.consulta import XPAHS_CONSULT


def consult_job(response):
    jobs_urls = response.xpath(XPAHS_CONSULT['jobs_urls'])
    for job_url in jobs_urls:
        final_url = clean_url(urljoin(response.url, job_url.extract()))
        yield Request(final_url, callback=extract_job)

    has_pagination = response.xpath(XPAHS_CONSULT['pagination'])
    if has_pagination:
        yield pagination(response)


def pagination(response):
    if '?pg=' not in response.url:
        # first page
        url_pagination = furl(response.url).add('pg=2').url
    else:
        splited_url = response.url.split('?pg=')
        url_pagination = furl(
            splited_url[0]).add(
                'pg={}'.format(str(int(splited_url[1]) + 1))).url

    return Request(url_pagination, callback=consult_job)
