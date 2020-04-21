import re

from scrapy.loader.processors import Join, TakeFirst
from stackflowCrawl.parsers import convert_to_int


_base_xpath_job = ('//div[contains(@class, "job-details--about")]/'
                   '/div[@class="mb8"]//span[preceding-sibling::span['
                   'contains(., "{}")]]/text()').format

_react_job_base_xpath = ("//span[contains(text(), 'React to this job')]"
                         "/following-sibling::span[@title='{}']//span//text()").format


def _clean_skills(skills):
    pattern = re.compile(r'(iphone|http|https|http:\/\/.*|https:\/\/.*|www|\.com|\.com\..*|@)')
    skills = [element for element in skills if not re.findall(pattern, element)]
    return list(set(skills))


def split_by_comma(item):
    if item:
        return item[0].split(',')
    return item


XPATHS_JOB = {

    # Jobs infos
    'title': '//h1[contains(@class, "headline1")]//a/text()',
    'jobType': _base_xpath_job('Job type'),
    'experienceLevel': (_base_xpath_job('Experience level'), split_by_comma),
    'role': (_base_xpath_job('Role'), split_by_comma),
    'industry': (_base_xpath_job('Industry'), split_by_comma),
    'companySize': _base_xpath_job('Company size'),
    'companyType': _base_xpath_job('Company type'),
    'technologies': ('//section[contains(., "Technologies")]//div//a/text()', _clean_skills),

    'description': ('//section[@class="mb32 fs-body2 fc-medium pr48"]', Join()),
    'jobLike': (_react_job_base_xpath('Like'), convert_to_int),
    'jobDislike': (_react_job_base_xpath('Dislike'), convert_to_int),
    'jobLove': (_react_job_base_xpath('Love'), convert_to_int),
    'aboutCompany': ("//section[@class='-about-company mb32']/div[@class='description']/p/text()", Join()),
    'joelTest': ('//section[contains(., "Joel Test")]'
                  '//div[@class="mb4" and //span[conta'
                  'ins(@class, "green")]]//span/following::text()[1]'),
    'linkApply': '//div[contains(@class, "job-details--display-contents")]/a/@href',
    'benefits': '//section[contains(@class, "benefits")]//ul//li/@title',

    # Company infos
    'company': ('//h1[contains(@class, "headline1")]/'
                'following-sibling::div[1]//a//text()'),

    'companyLogo': '//img[contains(@class, "s-avatar__lg")]/@src',
    'location': (
        'normalize-space(.//span[contains(@class, "fc-black-500")]/text())', TakeFirst()),
    'salary': '//header//span[contains(@class, "-salary")]/text()',
    'sponsor': ('//span[contains(@class, "-visa")]/text()', TakeFirst()),
    'paid': ('//span[contains(@class, "-relocation")]/text()', TakeFirst())
}
