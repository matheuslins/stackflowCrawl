# -*- coding: utf-8 -*-

XPAHS_CONSULT = {
    'jobs_urls': ('//div[contains(@class, "listResults")]'
                  '//div[contains(@class, "item")]//h2//a/@href'),
    'results': '//div[@id="index-hed"]//span//text()',
    'pagination': ('//div[contains(@class, "pagination")]'
                   '//a[contains(@class, "pagination-next")]')
}

START_URL = 'https://stackoverflow.com/jobs/'
