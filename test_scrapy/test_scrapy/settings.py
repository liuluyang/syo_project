# -*- coding: utf-8 -*-

# Scrapy settings for test_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'test_scrapy'

SPIDER_MODULES = ['test_scrapy.spiders']
NEWSPIDER_MODULE = 'test_scrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

#下载超时
DOWNLOAD_TIMEOUT = 20
#禁止重定向
REDIRECT_ENABLED = False

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
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
   'test_scrapy.middlewares.TestScrapySpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'test_scrapy.middlewares.TestScrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'test_scrapy.pipelines.TestScrapyPipeline': 300,
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

ITEM_PIPELINES = {
    'test_scrapy.pipelines_common.DropTag_a':100,          #过滤a标签
    'test_scrapy.pipelines_attention.AttentionPipeline':101,    #关注(微博 推特)
    'test_scrapy.pipelines_news.NewsPipeline':102, #新闻(政策、测评、活动、教程)
    'test_scrapy.pipelines_newsletter.NewsletterPipeline':103,#快讯(币世界 公告 火球财经)
    'test_scrapy.pipelines_tradingview.TradingViewPipeline':104, #TradingView

    'test_scrapy.pipelines_currency.CurrencyPipeline': 105,  # 币种
    'test_scrapy.pipelines_media.MediaPipeline':106,         #更新微博视频链接

    'test_scrapy.pipelines_token.EthTokenPipeline':107,      #代币
    'test_scrapy.pipelines_address.TokenAddressPipeline':108,      #代币 账户地址

    # 'test_scrapy.pipelines_common.CloseDB':200,              #关闭连接
    'test_scrapy.pipelines_common.PushMessage':201,          #消息推送

}

COMMANDS_MODULE = 'test_scrapy.commands'

#设置日志级别跟日志文件目录
LOG_LEVEL= 'INFO'
LOG_FILE ='test_scrapy.log'

DOWNLOADER_MIDDLEWARES = {
    'test_scrapy.middlewares.UserAgentMiddleware':401,
}

#设置需要捕获的状态码 抛出异常
HTTPERROR_ALLOWED_CODES = [403]

#mysql配置
MYSQL = {'host':'localhost', 'port':3306, 'db':'lvjian', 'user':'root',
         'passwd':'123456', 'use_unicode':True}

#测试数据库
MYSQL_TEST = {'host':'localhost', 'port':3306, 'db':'lvjian_test', 'user':'root',
         'passwd':'123456', 'use_unicode':True}

#是否推送
IS_PUSH = True
#需要消息推送的爬虫
PUST_SPIDER_SET = {'bsj_kuaixun'
                    }
#推送时间段
PUSH_TIME = ((9,10), (12,14), (17,18), (21,22))
#推送关键词
KEY_WORDS = ('上涨','下跌','主网','熊市','牛市','新币','回调',
             'Coindesk','突破','跌破','Coinbase')

#爬虫全抓取列表
SPIDER_NAME_LIST = ['bsj_kuaixun', 'fxh_notice', 'huoqiu_foreign','huoqiu_project',
                    'wlcj_eval', 'll_activity', 'hc_policy', 'btc_policy_new',
                    'weibo_mblog'
                    ]

TIME_PERIOD_CHECK = True

#持币地址变化阈值
address_change = 10000000

#大额充币提币阈值
transaction_value = 10000

#友盟推送
production_mode = "true"
appkey = '5b441123b27b0a6e5f00009d'
app_master_secret = 'c5col1l3jijfl16titxvbf8iloc3gkdt'
method = 'POST'
url = 'http://msg.umeng.com/api/send'