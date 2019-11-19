

import scrapy
#from test2_scrapy.items import NewsItem, NewsletterItem, AttentionItem

class T(scrapy.Spider):
    name = 't'
    allowed_domains = ['baidu.com']

    start_urls = ['https://www.baidu.com']

    def parse(self, response):
        print (response.css('title'))

        #测试一 该爬虫不推送 测试二 爬虫加入推送列表
        #测试三 关闭推送 测试四 关键字
        #测试五 时间段 关键字冲突测试
        # new_item = NewsItem()
        # new_item['title'] = '这是一个新闻标题 '
        # new_item['description'] = '这是一个新闻描述'
        # yield new_item

        #测试六 关键字 标红字段冲突测试
        #测试七 无标题
        # new_item = NewsletterItem()
        # new_item['title'] = None
        # new_item['description'] = '这是一个新闻描述 主网'
        # new_item['is_red'] = 0
        # yield new_item

        #时间段 关键字测试
        # new_item = AttentionItem()
        # new_item['author'] = '金色财经'
        # new_item['content'] = '这是一个微博内容 牛市】'
        # yield new_item



