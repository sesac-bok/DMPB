

BOT_NAME = 'bok'
RETRY_TIMES = 10
SPIDER_MODULES = ['bok.spiders']
NEWSPIDER_MODULE = 'bok.spiders'
HTTPERROR_ALLOWED_CODES = [404]
LOG_FILE = 'naver_news.log3'
FEED_EXPORT_ENCODING = 'utf-8-sig'
FEED_EXPORT_FIELDS = ['media', 'date', 'url', 'content']
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
}
FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
    # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FakerProvider',
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Fall back to USER_AGENT value
]

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32


REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
