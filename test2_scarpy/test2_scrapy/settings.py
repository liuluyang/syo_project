# -*- coding: utf-8 -*-

# Scrapy settings for test2_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

BOT_NAME = 'test2_scrapy'

SPIDER_MODULES = ['test2_scrapy.spiders']
NEWSPIDER_MODULE = 'test2_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test2_scrapy (+http://www.yourdomain.com)'

#此方法只能获取相同的User-Agent 如果随机需要另写中间件
# USER_AGENT_ = [
#     'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14',
#     'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2',
#     'Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre',
#     #'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)',
#     #'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5',
#     #'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527 (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )',
#     #'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1 '
# ]
#USER_AGENT = random.choice(USER_AGENT_)

# Obey robots.txt rules
#对于请求微博mblog列表来说 True False 没影响
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#电脑配置不变的情况下 16跟32 速度上没区别
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

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
   'test2_scrapy.middlewares.Test2ScrapySpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'test2_scrapy.middlewares.Test2ScrapyDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'test2_scrapy.middlewares.UserAgentMiddleware':401,#521在useragent之后加载
}
#downloader middlewares加载顺序401时
# ['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
#  'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
#  'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
#  'test2_scarpy.middlewares.UserAgentMiddleware',
#  'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
#  'scrapy.downloadermiddlewares.retry.RetryMiddleware',
#  'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
#  'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
#  'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
#  'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
#  'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
#  'scrapy.downloadermiddlewares.stats.DownloaderStats']


# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'test2_scrapy.pipelines.Test2ScrapyPipeline': 300,
#}

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

#DOWNLOAD_TIMEOUT = 30
DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
    #'test2_scrapy.pipelines_btc.PolicyPipeline':100
    #'test2_scrapy.pipelines_bsj.NewsletterPipeline':101
    'test2_scrapy.pipelines_token.EthTokenPipeline':107,
}

#接收到此状态码 会触发异常
HTTPERROR_ALLOWED_CODES = [403, 302]

#禁止重定向
REDIRECT_ENABLED = False


#mysql配置
MYSQL = {'host':'localhost', 'port':3306, 'db':'lvjian', 'user':'root',
         'passwd':'123456', 'charset':'utf8', 'use_unicode':True}

#友盟推送
production_mode = "false"
appkey = '5b441123b27b0a6e5f00009d'
app_master_secret = 'c5col1l3jijfl16titxvbf8iloc3gkdt'
method = 'POST'
url = 'http://msg.umeng.com/api/send'

