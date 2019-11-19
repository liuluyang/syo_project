# -*- coding: utf-8 -*-

from test_scrapy.items import NewsletterItem
import requests
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

class NewsletterPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not isinstance(item, NewsletterItem):
            return item
        if TIME_PERIOD_CHECK:
            result = time_period_check(item['created_at'], item['updated_at'])
            if not result:
                self.redis_update(spider, item)
                return

        spider.cursor.execute(
            """insert into uce_spider_kuaixun(group_id, origin_url, origin_from, is_red, title, thumb,
                            description, content, created_at, updated_at, is_more, to_url)
                        value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                item['group_id'],
                item['origin_url'],
                item['origin_from'],
                item['is_red'],
                item['title'],
                item['thumb'],
                item['description'],
                item['content'],
                item['created_at'],
                item['updated_at'],
                item['is_more'],
                item['to_url']
            )
        )
        spider.connect.commit()

        self.redis_update(spider, item)

        return item

    @staticmethod
    def redis_update(spider, item):
        # 把已抓取的数据链接添加到redis去重队列
        huoqiu = ['huoqiu_foreign', 'huoqiu_project']
        spider_name = spider.name
        if spider_name in huoqiu:
            spider.redis.sadd('newsletter_urls', item['data_id'])
        elif spider_name == 'bsj_kuaixun':
            spider.redis.sadd('newsletter_urls', item['origin_url'])
            # websocket消息推送 2018/8/29
            spider.redis.publish('kuaixun_bsj', item['title'])
        elif spider_name == 'fxh_notice':
            if item['origin_url']:
                spider.redis.sadd('newsletter_urls', item['origin_url'])
            else:
                spider.redis.sadd('newsletter_urls', item['to_url'])
        else:
            spider.logger.warning('已抓取数据添加到redis去重队列错误！！！')

