from decouple import config
from scrapy.utils.project import get_project_settings


settings = get_project_settings()


DEBUG = config('DEBUG', cast=bool, default=False)
ENVIRONMENT = config('ENVIRONMENT', cast=str, default='hml')

BOT_NAME = 'stackflowCrawl'

SPIDER_MODULES = [
    'stackflowCrawl.spiders.stackoverflow'
]

NEWSPIDER_MODULE = 'stackflowCrawl.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stackflowCrawl (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
#    'stackflowCrawl.middlewares.CrawlpySpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'stackflowCrawl.middlewares.TooManyRequestsRetryMiddleware': 543,
}
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

ITEM_PIPELINES = {
    'stackflowCrawl.pipelines.DuplicatesJobPipeline': 0,
    'stackflowCrawl.pipelines.BaseDBPipeline': 100
}

ITEM_PIPELINES['stackflowCrawl.pipelines.ElasticSearchPipeline'] = 300


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Elastic Search
ES_HOST = config('ES_HOST', cast=str, default='https://8a7b0b59fcde4d50ae94d5027ffbaba0.us-east-1.aws.found.io:9243')
ES_INDEX = config('ES_INDEX', cast=str, default='stkflow-jobs')

ES_CLUSTER_USER = config('ES_CLUSTER_USER', cast=str, default='elastic')
ES_CLUSTER_PASS = config('ES_CLUSTER_PASS', cast=str, default='wL7S8rUNIRh2bXKQ5lvy53Pr')

RETRY_HTTP_CODES = [429]

BULK_SIZE = config('BULK_SIZE', cast=int, default=100)
