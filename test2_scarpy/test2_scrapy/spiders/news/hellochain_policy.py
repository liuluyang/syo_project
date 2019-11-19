#coding:utf8


import scrapy
from test2_scrapy.items import PolicyItem
from test2_scrapy.redis_link import LinkRedis
import time

class PolicySpider(scrapy.Spider):
    name = 'hc_policy'
    allowed_domains = ['hellochain.info']
    url = 'http://www.hellochain.info/policy.html'

    def start_requests(self):
        self.redis = LinkRedis().redis

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        materials = response.css('.item-material')
        print (len(materials))
        if materials:
            for material in materials:
                thumb = material.css('.pic-material .pic img::attr(src)').extract_first() or None
                created_at = material.css('.date-material .date::text').extract_first().replace('.','-')
                title = material.css('.href-material::text').extract_first()
                description = material.css('#content p::text').extract_first() or None
                origin_from = material.css('.href-material::attr(href)').extract_first()
                author = material.css('.author-material span::text').extract_first()
                updated_at = time.strftime('%Y-%m-%d %X', time.localtime())

                print (thumb, created_at, title, origin_from, author, updated_at)
                print (description)

                item = PolicyItem()
                item['thumb'] = thumb
                item['created_at'] = created_at
                item['title'] = title
                item['description'] = description
                item['origin_from'] = origin_from
                item['author'] = author
                item['updated_at'] = updated_at

                if self.redis.sismember('policy_urls', origin_from):
                    continue

                yield scrapy.Request(origin_from, callback=self.content, meta={'item':item})

        else:
            print ('not get material data')
            time.sleep(1)
            yield scrapy.Request(self.url, callback=self.parse, dont_filter=True)

    def content(self, response):
        item = response.meta['item']
        content = response.css('.con p').extract()
        content = ''.join(content)
        #print (content)
        if content:
            item['content'] = content
            item['origin_url'] = None

            yield item
        else:
            print('not get content data')
            yield scrapy.Request(item['origin_from'], callback=self.content, meta={'item':item},
                                 dont_filter=True)
        pass


