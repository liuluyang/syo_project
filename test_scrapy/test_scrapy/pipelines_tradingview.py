# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from test_scrapy.items import TradingViewItem
from test_scrapy.settings import TIME_PERIOD_CHECK
import time
import json

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

class TradingViewPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        if spider.name == 'trading_view':
            url = 'http://bzg.one/uploads/'
            spider.cursor.execute(
                """
                select uuid, author_avatar from uce_spider_weibott where
                group_id=14 and status=1
                """
            )
            author_list = spider.cursor.fetchall()
            author_avatar = {}
            for author in author_list:
                if author[-1]:
                    author_avatar[author[0]] = url+author[-1]
                else:
                    author_avatar[author[0]] = None
            # 测试数据库
            spider.cursor, spider.connect = spider.cursor_test, spider.connect_test
            fields = ('id', 'origin_url', 'orgin_from', 'title', 'nickname',
                      'thumb', 'description', 'content', 'symbol', 'label',
                      'created_at')
            spider.cursor.execute(
                """
                select id, origin_url, origin_from, title, nickname, thumb, description,
                content, symbol, label, created_at from uce_spider_news where
                group_id=14 order by created_at desc limit 30
                """
            )
            idea_list = spider.cursor.fetchall()
            new_list = []

            for idea in idea_list:
                new = {}
                for index, v in enumerate(idea):
                    k = fields[index]
                    if k == 'created_at':
                        new[k] = str(v)
                    elif k == 'nickname':
                        new['author_avatar'] = author_avatar.get(v)
                        new[k] = v
                    elif k == 'description':
                        new['desc'] = v
                    else:
                        new[k] = v
                if not new['author_avatar']:
                    continue
                new_list.append(new)

            data_redis = {}
            data_redis['data'] = new_list
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            data_redis['updated_at'] = time_now
            spider.redis.hset('tradingview', 'idea', json.dumps(data_redis))

    def process_item(self, item, spider):
        if not isinstance(item, TradingViewItem):
            return item
        TIME_PERIOD_CHECK = False
        if TIME_PERIOD_CHECK:
            result = time_period_check(item['created_at'], item['updated_at'])
            if not result:
                self.redis_update(spider, item)
                return
        # 测试数据库
        spider.cursor, spider.connect = spider.cursor_test, spider.connect_test

        spider.cursor.execute(
            """insert into uce_spider_news(group_id, origin_url, origin_from, thumb, title, 
                    created_at, updated_at, nickname, description, content,
                    symbol, label) 
                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
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
                item['content'],
                item['symbol'],
                item['label']

            )
        )
        spider.connect.commit()

        self.redis_update(spider, item)

        return item

    @staticmethod
    def redis_update(spider, item):
        spider.redis.sadd('TradingView_idea', item['origin_url'])
