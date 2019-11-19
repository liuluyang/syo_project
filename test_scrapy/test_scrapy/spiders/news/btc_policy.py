#coding:utf8


import scrapy
from test_scrapy.items import NewsItem
import time
from scrapy.selector import Selector

class PolicySpider(scrapy.Spider):
    name = 'btc_policy'
    allowed_domains = ['8btc.com']
    url = 'https://www.8btc.com/news?cat_id=572'
    need_UserAgent = True

    group_id = 6
    origin_from = '巴比特'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        articles = response.xpath('//div[@id="news"]/div/div')

        if articles:
            for article in articles:
                group_id = self.group_id
                origin_from = self.origin_from
                origin_url = article.css('.article-item__thumb a::attr(href)').extract_first() #内容页链接
                origin_url = response.urljoin(origin_url)
                thumb = article.css('.article-item__thumb a img::attr(src)').extract_first()    #缩略图链接
                thumb = response.urljoin(thumb)
                title = article.css('.article-item__title a::text').extract_first()
                author = article.css('.article-item__info .article-item__author .link-dark-major::text').extract_first()
                author = author.strip()
                description = article.css('.article-item__content::text').extract_first()
                description = ''.join(description.split())
                updated_at = time.strftime('%Y-%m-%d %X', time.localtime())


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

                yield scrapy.Request(origin_url, callback=self.content, meta={'item':item})

    def content(self, response):
        content = response.xpath('//div[@class="bbt-html"]/*').extract()
        created_at = response.css('.header__info-item::text').extract_first()
        created_at = created_at.strip()
        content_new = ''
        for cont in content:
            content_new+=self.delete_img_attr(cont)

        item = response.meta['item']
        item['content'] = content_new
        item['created_at'] = created_at

        yield item

    def delete_img_attr(self, tag):
        check = ['原文：','作者：','本文由作者']
        text = Selector(text=tag)

        for c in check:
            if c in tag:
                return ''

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


