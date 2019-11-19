#coding:utf8

import scrapy
from test_scrapy.items import AttentionItem
import json, time

class TwitterSpider(scrapy.Spider):
    name = 'cf_twitter'
    allowed_domains = ['chainfor.com']

    parent_id = 5   #类型ID

    def start_requests(self):
        self.url = 'https://www.chainfor.com/news/list/flashnew/data.do?' \
                   'type=2&pageSize=15&pageNo={page}'

        yield scrapy.Request(self.url.format(page=1), callback=self.parse)

    def parse(self, response):
        """
        功能尚不完善 未进行作者数据调取（数据库推特作者数据不完善）
        :param response: 
        :return: 
        """
        data_json = json.loads(response.text)
        obj_list = data_json['obj']['list']

        for obj in obj_list:
            data = json.loads(obj['introduction'])
            parent_id = self.parent_id
            group_id = 0
            author = data['name']
            screenName = data['screenName']
            author_avatar = 'http://39.107.25.11/image/twitter/{name}.jpg'.\
                            format(name=screenName)     #头像
            content = data['text']
            t = float(data['date']['time']/1000)
            published_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            created_at = time.strftime('%Y-%m-%d %X', time.localtime())
            from_url = data.get('url', None)
            forward = data['zhuanfa']
            img_urls = None
            media_url = None
            if self.redis.sismember('twitter_content', content):
                continue

            item = AttentionItem()
            item['parent_id'] = parent_id
            item['group_id'] = group_id
            item['author'] = author
            item['author_avatar'] = author_avatar
            item['content'] = content
            item['img_urls'] = img_urls
            item['media_url'] = media_url
            item['from_url'] = from_url
            item['published_at'] = published_at
            item['created_at'] = created_at
            item['forward'] = None

            if forward:
                author = forward['name']
                content = forward['text']
                t = float(forward['date']['time'] / 1000)
                published_at = time.strftime('%Y-%m-%d %H:%M:%S',
                                             time.localtime(t))
                forward = {
                    'author':author, 'content':content,
                    'published_at':published_at
                }
                #转成str
                item['forward'] = json.dumps(forward)

            yield item



