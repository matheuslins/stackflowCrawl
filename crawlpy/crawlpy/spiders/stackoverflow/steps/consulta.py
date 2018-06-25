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
        yield pagination(response, has_pagination)


def pagination(response, h_pag):
    url_pag = h_pag.xpath('./@href')[0].extract()
    url_parse = furl(response.url)
    url_pagination = url_parse.origin + url_pag
    return Request(url_pagination, callback=consult_job)