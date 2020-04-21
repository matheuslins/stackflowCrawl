import scrapy
from scrapy.loader.processors import Identity


class JobItem(scrapy.Item):
    # General infos
    url = scrapy.Field()
    jobId = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    sponsor = scrapy.Field()
    salary = scrapy.Field()
    paid = scrapy.Field()

    # About the job
    jobType = scrapy.Field()
    industry = scrapy.Field(output_processor=Identity())
    experienceLevel = scrapy.Field(output_processor=Identity())
    role = scrapy.Field()
    companySize = scrapy.Field()
    companyType = scrapy.Field()
    companyLogo = scrapy.Field()
    description = scrapy.Field()
    aboutCompany = scrapy.Field()
    jobLike = scrapy.Field()
    jobDislike = scrapy.Field()
    jobLove = scrapy.Field()
    linkApply = scrapy.Field()
    joelTest = scrapy.Field(output_processor=Identity())  # list
    technologies = scrapy.Field(output_processor=Identity())  # list
    benefits = scrapy.Field(output_processor=Identity())  # list


class CompanyItem(scrapy.Item):
    # General infos
    name = scrapy.Field()
    companyType = scrapy.Field()
    companyHomePage = scrapy.Field()
    openJobs = scrapy.Field(output_processor=Identity())  # list
    benefits = scrapy.Field(output_processor=Identity())  # list
    technologyStack = scrapy.Field(output_processor=Identity())  # list
