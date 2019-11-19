#coding:utf8


import scrapy
from test2_scrapy.items import PolicyItem
from test2_scrapy.redis_link import LinkRedis
import time


class ActivitySpider(scrapy.Spider):
    name = 'll_activity'
    allowed_domains = ['leilook.com']
    url = 'http://www.leilook.com/archives/category/active'

    def start_requests(self):
        self.redis = LinkRedis().redis

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        excerpts = response.css('.content .excerpt')
        for excerpt in excerpts:
            thumb = excerpt.css('.focus img::attr(src)').extract_first()
            origin_from = excerpt.css('header a::attr(href)').extract_first()
            title = excerpt.css('header a::text').extract_first()
            description = excerpt.css('.note::text').extract_first()
            author = excerpt.css('.meta .author::text').extract_first()
            created_at = excerpt.css('.meta time::text').extract()[-1]

            print (thumb, origin_from, title, description, author, created_at)

            item = PolicyItem()
            item['thumb'] = thumb
            item['origin_from'] = origin_from
            item['title'] = title
            item['description'] = description
            item['author'] = author
            item['created_at'] = created_at
            item['updated_at'] = time.strftime('%Y-%m-%d %X', time.localtime())

            if self.redis.sismember('policy_urls', origin_from):
                continue

            yield scrapy.Request(origin_from, self.content, meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        created_time = response.css('.content .article-infos .article-info')[0]
        created_time = created_time.css('.time::text').extract_first()
        created_time = created_time.split(' ')[-1]
        content = response.xpath('//div[@class="content"]//article[@class="article-content"]/*').extract()
        content = ''.join(content)

        item['created_at'] = item['created_at']+' '+created_time
        item['content'] = content
        item['origin_url'] = None

        #print (created_time, content)

        yield item
