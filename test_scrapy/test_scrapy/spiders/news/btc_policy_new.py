#coding:utf8


import scrapy
from test_scrapy.items import NewsItem
import time
from scrapy.selector import Selector
import json

class PolicySpider(scrapy.Spider):
    name = 'btc_policy_new'
    allowed_domains = ['8btc.com']
    url = 'https://app.blockmeta.com/w1/news/list?num=20&page=1&cat_id=572'
    need_UserAgent = True

    group_id = 6
    origin_from = '巴比特'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        articles = json.loads(response.text)['list']
        #key_name = ['id', 'post_date_format', 'title',
        # 'desc', 'image', 'author_info/display_name']
        if articles:
            for article in articles:
                group_id = self.group_id
                origin_from = self.origin_from
                origin_url = article['id'] #内容页链接
                origin_url = 'https://m.8btc.com/article/{}'.format(origin_url)
                thumb = article['image']    #缩略图链接
                title = article['title']
                author = article.get('author_info',{}).get('display_name', None)
                description = article['desc']
                description = ''.join(description.split())
                created_at = article['post_date_format']
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
                item['created_at'] = created_at

                if self.redis.sismember('news_urls', origin_url):
                     continue

                yield scrapy.Request(origin_url, callback=self.content, meta={'item':item})

    def content(self, response):
        content = response.xpath('//div[@class="article-content"]/*').extract()
        content_new = ''
        self.is_need = 1
        for cont in content:
            content_new+=self.delete_img_attr(cont)

        item = response.meta['item']
        item['content'] = content_new

        yield item

    def delete_img_attr(self, tag):
        not_need_class = ['content-bottom', 'ad akp-adv', 'content-source-info']
        check = ['原文：','作者：','本文由作者', '转载']
        text = Selector(text=tag)
        class_name = text.css('::attr(class)').extract_first()
        if not self.is_need:
            return ''
        if class_name in not_need_class:
            self.is_need = 0
            return ''

        for c in check:
            if c in tag:
                self.is_need = 0
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


