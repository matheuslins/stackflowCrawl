import re

from scrapy.http import Request
from urllib.parse import urljoin
from furl import furl

from stackflowCrawl.parsers import convert_items_to_int
from .extraction import extract_job
from ..utils import clean_url
from ..constants.consult import XPAHS_CONSULT


def consult_job(response):

    results = convert_items_to_int(
        re.findall(
            r'(\d+)',
            response.xpath(XPAHS_CONSULT['results']).extract_first()
        )
    )

    if not results or (0 in results):
        return []

    jobs_urls = response.xpath(XPAHS_CONSULT['jobs_urls'])
    for job_url in jobs_urls:
        final_url = clean_url(urljoin(response.url, job_url.extract()))
        yield Request(final_url, callback=extract_job)

    has_pagination = response.xpath(XPAHS_CONSULT['pagination_indicator'])
    if has_pagination:
        yield pagination(response)


def pagination(response):
    url_pag = response.xpath(XPAHS_CONSULT['pagination_url']).extract_first()
    url_parse = furl(response.url)
    url_pagination = url_parse.origin + url_pag
    return Request(url_pagination, callback=consult_job)
