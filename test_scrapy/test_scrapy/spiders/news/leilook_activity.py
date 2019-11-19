#coding:utf8


import scrapy
from test_scrapy.items import NewsItem
import time
from scrapy.selector import Selector


class ActivitySpider(scrapy.Spider):
    name = 'll_activity'
    allowed_domains = ['leilook.com']
    url = 'http://www.leilook.com/archives/category/active'

    group_id = 13
    origin_from = '雷鹿财经'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        excerpts = response.css('.content .excerpt')
        for excerpt in excerpts:
            group_id = self.group_id
            origin_from = self.origin_from
            thumb = excerpt.css('.focus img::attr(src)').extract_first()
            origin_url = excerpt.css('header a::attr(href)').extract_first()
            title = excerpt.css('header a::text').extract_first()
            description = excerpt.css('.note::text').extract_first()
            author = excerpt.css('.meta .author::text').extract_first()
            created_at = excerpt.css('.meta time::text').extract()[-1]

            #print (thumb, origin_from, title, description, author, created_at)

            item = NewsItem()
            item['thumb'] = thumb
            item['origin_url'] = origin_url
            item['title'] = title
            item['description'] = description
            item['author'] = author
            item['created_at'] = created_at
            item['updated_at'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['group_id'] = group_id
            item['origin_from'] = origin_from

            if self.redis.sismember('news_urls', origin_url):
                continue

            yield scrapy.Request(origin_url, self.content, meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        created_time = response.css('.content .article-infos .article-info')[0]
        created_time = created_time.css('.time::text').extract_first()
        created_time = created_time.split(' ')[-1]
        content = response.xpath('//div[@class="content"]//article[@class="'
                                 'article-content"]/*').extract()
        content_new = ''
        for cont in content:
            content_new+=self.delete_img_attr(cont)

        item['created_at'] = item['created_at']+' '+created_time
        item['content'] = content_new

        #print (created_time, content)

        yield item

    def delete_img_attr(self, tag):

        text = Selector(text=tag)
        if text.css('img'):
            class_value = text.css('img::attr(class)').extract()
            width = text.css('img::attr(width)').extract()
            height = text.css('img::attr(height)').extract()
            for c in class_value:
                tag = tag.replace('class="'+c+'"', "")
            for w in width:
                tag = tag.replace('width="'+w+'"', "")
            for h in height:
                tag = tag.replace('height="'+h+'"', "")

        return tag
