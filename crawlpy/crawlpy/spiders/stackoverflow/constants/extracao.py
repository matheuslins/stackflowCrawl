# -*- coding: utf-8 -*-

from scrapy.loader.processors import Join, TakeFirst


_base_xpath_job = ('//div[contains(@class, "job-details--about")]/'
                   '/div[@class="mb8"]//span[preceding-sibling::span['
                   'contains(., "{}")]]/text()').format

XPATHS_JOB = {

    # Jobs infos
    'job_title': '//h1[contains(@class, "headline1")]//a/text()',
    'job_type': _base_xpath_job('Job type'),
    'experience_level': _base_xpath_job('Experience level'),
    'role': _base_xpath_job('Role'),
    'industry': _base_xpath_job('Industry'),
    'company_size': _base_xpath_job('Company size'),
    'company_type': _base_xpath_job('Company type'),
    'tecnologies': '//section[contains(., "Technologies")]//div//a/text()',

    'job_description': ('//section[contains(., "Job description")]//p', Join()),  # noqa
    'joel_test': ('//section[contains(., "Joel Test")]'
                  '//div[@class="mb4" and //span[conta'
                  'ins(@class, "green")]]'),
    'link_apply': ('//a[contains(@class, "_apply")]/@href', TakeFirst()),
    'benefits': '//section[contains(@class, "benefits")]//ul//li/@title',

    # Company infos
    'company': ('//h1[contains(@class, "headline1")]/'
                'following-sibling::div[1]//a//text()'),
    'location': ('//h1[contains(@class, "headline1")]/'
                 'following-sibling::div[1]//span/text()'),
    'salary_year': ('//span[contains(@class, "-salary")]/text()', TakeFirst()),
    'sponsor': ('//span[contains(@class, "-visa")]/text()', TakeFirst()),
    'paid': ('//span[contains(@class, "-relocation")]/text()', TakeFirst())
}
