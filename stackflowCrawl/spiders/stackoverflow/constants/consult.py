
XPAHS_CONSULT = {
    'jobs_urls': '//div[contains(@class, "listResults")]//div[contains(@data-jobid, "")]//h2//a/@href',
    'results': '//span[@class="description fc-light fs-body1"]//text()',
    'pagination_indicator': '//a[contains(@class, "s-pagination--item")][last()]//span[contains(text(), "next")]',
    'pagination_url': '//a[contains(@class, "s-pagination--item")][last()]/@href',
}

START_URL = 'https://stackoverflow.com/jobs/'
