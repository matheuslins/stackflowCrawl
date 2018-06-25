# -*- coding: utf-8 -*-

START_URL = 'https://www.linkedin.com/jobs/search/?f_I=4%2C96'

XPAHS_CONSULT = {
    'jobs_urls': ('//div[contains(@class, "content-wrapper")]//'
                  'a[contains(@data-control-name, "job_result_click")]'),
    'pagination': '//div[contains(@class, "next-text")]'
}
