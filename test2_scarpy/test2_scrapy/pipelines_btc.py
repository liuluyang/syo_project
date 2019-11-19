# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re, time
from test2_scrapy.redis_link import LinkRedis
from test2_scrapy.items import PolicyItem


class TestScrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class PolicyPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.r = LinkRedis().r
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='btc',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=True
        )

        self.cursor = self.connect.cursor()
        pass

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        if not isinstance(item, PolicyItem):
            return item
        self.cursor.execute(
            """insert into policy(origin_url, origin_from, thumb, title, created_at, updated_at, author, description, content) value (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                item['origin_url'],
                item['origin_from'],
                item['thumb'],
                item['title'],
                item['created_at'],
                item['updated_at'],
                item['author'],
                item['description'],
                item['content']

            )
        )
        self.connect.commit()
        self.r.sadd('policy_urls', item['origin_from'])
        return item
