#coding:utf8

import scrapy
import time
import re
from test_scrapy.items import NewsItem
from scrapy.selector import Selector

class EvaluationSpider(scrapy.Spider):
    name = 'wlcj_eval'
    allowed_domains = ['weilaicaijing.com']
    url = 'http://www.weilaicaijing.com/evaluation'

    group_id = 7
    origin_from = '未来财经'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        articles = response.css('.content-left-content ul li')
        for article in articles:
            group_id = self.group_id
            origin_from = self.origin_from
            thumb = article.css('.item .img::attr(style)').extract_first()
            thumb = re.search(r'http.*\'', thumb).group()[:-1]
            origin_url = article.css('.item .img::attr(href)').extract_first()
            origin_url = response.urljoin(origin_url)
            title = article.css('.item-right a::attr(title)').extract_first()
            description = article.css('.item-right .item-text1::text').extract_first()
            author = article.css('.item-right .item-information .username::text').extract_first()
            author = author.strip()
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())

            #print (thumb, origin_from, title, description, author, updated_at)

            item = NewsItem()
            item['origin_url'] = origin_url
            item['thumb'] = thumb
            item['title'] = title
            item['author'] = author
            item['description'] = description
            item['updated_at'] = updated_at
            item['group_id'] = group_id
            item['origin_from'] = origin_from

            if self.redis.sismember('news_urls', origin_url):
                continue

            yield scrapy.Request(origin_url, callback=self.content,
                                 meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@class="text"]//div[@class="'
                                 'text-content"]/*').extract()
        content_new = ''
        for cont in content[:-1]:
            content_new+=self.delete_img_attr(cont)
        created_at = response.css('.text .information .itemlook::text').extract()[-1]
        created_at = created_at.replace('/\n','').strip()

        item['content'] = content_new
        item['created_at'] = created_at

        yield item

    def delete_img_attr(self, tag):

        text = Selector(text=tag)
        if text.css('img'):
            class_value = text.css('img::attr(class)').extract()
            width = text.css('img::attr(width)').extract()
            height = text.css('img::attr(height)').extract()
            style = text.css('img::attr(style)').extract()
            for c in class_value:
                tag = tag.replace('class="'+c+'"', "")
            for w in width:
                tag = tag.replace('width="'+w+'"', "")
            for h in height:
                tag = tag.replace('height="'+h+'"', "")
            for s in style:
                tag = tag.replace('style="'+s+'"', "")

        return tag



