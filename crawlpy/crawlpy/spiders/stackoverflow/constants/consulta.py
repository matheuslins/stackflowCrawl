# -*- coding: utf-8 -*-

XPAHS_CONSULT = {
    'jobs_urls': ('//div[contains(@class, "listResults")]'
                  '//div[contains(@class, "item")]//h2//a/@href'),
    'pagination': '//div[contains(@class, "pagination")]'
}

START_URL = 'https://stackoverflow.com/jobs/'
