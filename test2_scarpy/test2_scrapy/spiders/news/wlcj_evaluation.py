#coding:utf8

import scrapy
import time
import re
from test2_scrapy.items import PolicyItem
from test2_scrapy.redis_link import LinkRedis

class EvaluationSpider(scrapy.Spider):
    name = 'wlcj_eval'
    allowed_domains = ['weilaicaijing.com']
    url = 'http://www.weilaicaijing.com/evaluation'

    def start_requests(self):
        self.redis = LinkRedis().redis

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        articles = response.css('.content-left-content ul li')
        for article in articles:
            #print (article)
            thumb = article.css('.item .img::attr(style)').extract_first()
            thumb = re.search(r'http.*\'', thumb).group()[:-1]
            origin_from = article.css('.item .img::attr(href)').extract_first()
            origin_from = response.urljoin(origin_from)
            title = article.css('.item-right a::attr(title)').extract_first()
            description = article.css('.item-right .item-text1::text').extract_first()
            author = article.css('.item-right .item-information .username::text').extract_first()
            author = author.strip()
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())

            print (thumb, origin_from, title, description, author, updated_at)

            item = PolicyItem()
            item['origin_from'] = origin_from
            item['thumb'] = thumb
            item['title'] = title
            item['author'] = author
            item['description'] = description
            item['updated_at'] = updated_at

            if self.redis.sismember('policy_urls', origin_from):
                continue

            yield scrapy.Request(origin_from, callback=self.content, meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@class="text"]//div[@class="text-content"]/*').extract()
        content = ''.join(content)
        created_at = response.css('.text .information .itemlook::text').extract()[-1]
        created_at = created_at.replace('/\n','').strip()

        #print ({'1':created_at})

        item['content'] = content
        item['created_at'] = created_at
        item['origin_url'] = None

        yield item
        pass



