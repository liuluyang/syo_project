# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from test_scrapy.items import AttentionItem
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

class AttentionPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not isinstance(item, AttentionItem):
            return item
        if TIME_PERIOD_CHECK:
            result = time_period_check(item['published_at'], item['created_at'])
            if not result:
                self.redis_update(spider, item)
                return

        spider.cursor.execute(
            """insert into uce_spider_guanzhu(parent_id, group_id, author, 
                    author_avatar, content, img_urls, media_url, from_url,
                    forward, published_at, created_at)
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                item['parent_id'],
                item['group_id'],
                item['author'],
                item['author_avatar'],
                item['content'],
                item['img_urls'],
                item['media_url'],
                item['from_url'],
                item['forward'],
                item['published_at'],
                item['created_at'],

            )
        )
        spider.connect.commit()

        self.redis_update(spider, item)

        return item

    @staticmethod
    def redis_update(spider, item):
        # 已爬数据加入去重数据库
        if spider.name == 'weibo_mblog':
            spider.redis.sadd('mblog_urls', item['from_url'])
        if spider.name == 'cf_twitter':
            spider.redis.sadd('twitter_content', item['content'])
