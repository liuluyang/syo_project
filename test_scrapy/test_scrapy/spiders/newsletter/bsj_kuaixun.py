#coding:utf8


import scrapy
from test_scrapy.items import NewsletterItem
import time, re


'''
user_agent 有没有都可以（请求网页版）
但user_agent是移动端类型时会返回移动端数据
如果请求的是网页版 会重定向到移动端
'''

class KuaixunSpider(scrapy.Spider):
    name = 'bsj_kuaixun'
    allowed_domains = ['bishijie.com']
    url = 'https://www.bishijie.com/kuaixun/'
    need_UserAgent = True
    group_id = 8
    origin_from = '币世界'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        lives = response.css('.live ul')

        for live in lives[:5]:
            group_id = self.group_id
            origin_from = self.origin_from
            time_at = live.css('span::text').extract_first()
            title = live.css('.lh32 h2 a::attr(title)').extract_first()
            origin_url = live.css('.lh32 h2 a::attr(href)').extract_first()
            origin_url = response.urljoin(origin_url)
            description = live.css('.lh32 div a::text').extract_first()
            description = description.strip()
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())

            thumb = None
            is_red = 0
            is_more = 0
            to_url = None
            if len(live.css('li'))==3:
                is_more = 1
                to_url = live.css('li')[1].css('a::attr(href)').extract_first()
            if live.css('span::attr(style)').extract_first():
                is_red = 1

            #print (time_at, title, origin_url, description, is_more, to_url, is_red)

            item = NewsletterItem()
            item['group_id'] = group_id
            item['origin_url'] = origin_url
            item['origin_from'] = origin_from
            item['title'] = title
            item['description'] = description
            item['created_at'] = time_at
            item['updated_at'] = updated_at
            item['is_red'] = is_red
            item['is_more'] = is_more
            item['to_url'] = to_url
            item['thumb'] = thumb

            if self.check_title(title):
                continue
            if self.redis.sismember('newsletter_urls', origin_url):
                continue

            yield scrapy.Request(origin_url, callback=self.content, meta={'item':item})


    def content(self, response):
        item = response.meta['item']
        content = response.css('.lh32 div::text').extract()
        content = '<br>'.join(content)
        date_at = response.css('.xq_time::text').extract_first()
        date_at = re.findall(r'(\d{2})',date_at)
        date_at = time.strftime('%Y', time.localtime())+'-'+'-'.join(date_at)
        created_at = date_at+' '+item['created_at']

        #print (content, date_at, created_at)

        item['content'] = self.check_content(content)
        item['description'] = item['content']
        item['created_at'] = created_at
        #print (created_at, item['content'], created_at)

        yield item

    def check_title(self, title):
        """
        过滤数据
        :param title: str
        :return: boolean
        """
        check_list = ['币世界','龙虎榜','推广','名家论市']
        for s in check_list:
            if s in title:
                return True

        return False

    def check_content(self, content):
        word_list = re.findall(r'(《币.*世.*界》)', content)
        for i in set(word_list):
            content = content.replace(i, '')

        return content

