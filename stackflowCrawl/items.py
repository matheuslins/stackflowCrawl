# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Identity


class JobItem(scrapy.Item):
    # General infos
    url = scrapy.Field()
    job_id = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    sponsor = scrapy.Field()
    salary = scrapy.Field()
    paid = scrapy.Field()

    # About the job
    _type = scrapy.Field()
    industry = scrapy.Field()
    experience_level = scrapy.Field()
    role = scrapy.Field()
    company_size = scrapy.Field()
    company_type = scrapy.Field()
    description = scrapy.Field()
    link_apply = scrapy.Field()
    joel_test = scrapy.Field(output_processor=Identity())  # list

    # Tecnologies
    tecnologies = scrapy.Field(output_processor=Identity())  # list

    # Benefits
    benefits = scrapy.Field(output_processor=Identity())  # list


class CompanyItem(scrapy.Item):
    # General infos
    name = scrapy.Field()
    company_type = scrapy.Field()
    company_home_page = scrapy.Field()
    open_jobs = scrapy.Field(output_processor=Identity())  # list
    benefits = scrapy.Field(output_processor=Identity())  # list
    technology_stack = scrapy.Field(output_processor=Identity())  # list
