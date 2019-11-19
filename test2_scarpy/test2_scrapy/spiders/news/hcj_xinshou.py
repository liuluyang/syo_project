#coding:utf8


import scrapy
from test2_scrapy.items import PolicyItem
from test2_scrapy.redis_link import LinkRedis
import time

'''
核财经数据抓取 请求头需要User_Agent信息
之后会通过头部信息判断 请求是PC端还是移动端
来进行请求重定向

'''
class ActivitySpider(scrapy.Spider):
    name = 'hcj_xinshou'
    allowed_domains = ['m.hecaijing.com']
    url = 'http://m.hecaijing.com'
    need_UserAgent = True


    def start_requests(self):
        self.redis = LinkRedis().redis

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        print (response)
        articles = response.css('.con')[6].css('.li')
        for article in articles:
            thumb = article.css('.a .slide::attr(data-original)').extract_first()
            origin_from = article.css('.a::attr(href)').extract_first()
            origin_from = response.urljoin(origin_from)
            title = article.css('.a .main .title::text').extract_first()
            created_at = article.css('.a .main .bottom::text').extract_first()
            created_at = created_at.replace('\n','').strip()

            print (thumb, origin_from, title,created_at)

            item = PolicyItem()
            item['thumb'] = thumb
            item['origin_from'] = origin_from
            item['title'] = title
            item['created_at'] = created_at
            item['updated_at'] = time.strftime('%Y-%m-%d %X', time.localtime())

            if self.redis.sismember('policy_urls', origin_from):
                continue

            yield scrapy.Request(origin_from, self.content, meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        author = response.css('.author_name::text').extract_first()
        author = author.replace('\n','').strip()
        content = response.xpath('//div[@class="main"]/*').extract()
        content = ''.join(content)

        item['author'] = author
        item['content'] = content
        item['origin_url'] = None
        item['description'] = None

        #print (author, content)

        yield item
