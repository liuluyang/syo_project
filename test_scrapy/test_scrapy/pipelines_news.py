# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from test_scrapy.items import NewsItem
from test_scrapy.settings import TIME_PERIOD_CHECK
import time

def time_period_check(created_at, updated_at, period=600):
    format_list = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
    timestamps_c = time.time()
    for f in format_list:
        try:
            timestamps_c = int(
                time.mktime(time.strptime(created_at, f)))
            break
        except:
            pass
    timestamps_u = int(
        time.mktime(time.strptime(updated_at, "%Y-%m-%d %H:%M:%S")))
    if timestamps_u-timestamps_c<period:
        return True
    return False

class NewsPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not isinstance(item, NewsItem):
            return item
        if TIME_PERIOD_CHECK:
            result = time_period_check(item['created_at'], item['updated_at'])
            if not result:
                self.redis_update(spider, item)
                return

        spider.cursor.execute(
            """insert into uce_spider_news(group_id, origin_url, origin_from, thumb, title, 
                    created_at, updated_at, nickname, description, content) 
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                item['group_id'],
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
        spider.connect.commit()

        self.redis_update(spider, item)

        return item

    @staticmethod
    def redis_update(spider, item):
        spider.redis.sadd('news_urls', item['origin_url'])
