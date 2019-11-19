#coding:utf8


import scrapy
from test_scrapy.items import NewsItem
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

    group_id = 12
    origin_from = '核财经'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        articles = response.css('.con')[6].css('.li')
        for article in articles:
            group_id = self.group_id
            origin_from = self.origin_from
            thumb = article.css('.a .slide::attr(data-original)').extract_first()
            origin_url = article.css('.a::attr(href)').extract_first()
            origin_url = response.urljoin(origin_url)
            title = article.css('.a .main .title::text').extract_first()
            created_at = article.css('.a .main .bottom::text').extract_first()
            created_at = created_at.replace('\n','').strip()

            #print (thumb, origin_from, title,created_at)

            item = NewsItem()
            item['thumb'] = thumb
            item['origin_url'] = origin_url
            item['title'] = title
            item['created_at'] = created_at
            item['updated_at'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['group_id'] = group_id
            item['origin_from'] = origin_from

            if self.redis.sismember('news_urls', origin_url):
                continue

            yield scrapy.Request(origin_url, self.content, meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        author = response.css('.author_name::text').extract_first()
        author = author.replace('\n','').strip()
        content = response.xpath('//div[@class="main"]/*').extract()
        content = ''.join(content)

        item['author'] = author
        item['content'] = content
        item['description'] = None

        #print (author, content)

        yield item
