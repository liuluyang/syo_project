#coding:utf8


import scrapy
from test_scrapy.items import NewsItem
import time
from scrapy.selector import Selector

class PolicySpider(scrapy.Spider):
    name = 'hc_policy'
    allowed_domains = ['hellochain.info']
    url = 'http://www.hellochain.info/policy.html'

    group_id = 6
    origin_from = 'HelloChain'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        materials = response.css('.item-material')

        for material in materials:
            group_id = self.group_id
            origin_from = self.origin_from
            thumb = material.css('.pic-material .pic img::attr(src)').extract_first() or None
            created_at = material.css('.date-material .date::text').extract_first().replace('.', '-')
            title = material.css('.href-material::text').extract_first()
            description = material.css('#content p::text').extract_first() or None
            origin_url = material.css('.href-material::attr(href)').extract_first()
            author = material.css('.author-material span::text').extract_first()
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())

            item = NewsItem()
            item['thumb'] = thumb
            item['created_at'] = created_at
            item['title'] = title
            item['description'] = description
            item['origin_url'] = origin_url
            item['author'] = author
            item['updated_at'] = updated_at
            item['group_id'] = group_id
            item['origin_from'] = origin_from

            if self.redis.sismember('news_urls', origin_url):
                continue

            yield scrapy.Request(origin_url, callback=self.content, meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@class="con line30 font18"]/*').extract()
        content_new = ''
        for cont in content:
            content_new+=self.delete_img_attr(cont)
        if content:
            item['content'] = content_new

            yield item

    def delete_img_attr(self, tag):

        text = Selector(text=tag)
        if text.css('img'):
            tag = tag.replace('id="image"', "")

        return tag


