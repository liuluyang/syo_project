
from test_scrapy.items import EthToken

class EthTokenPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not isinstance(item, EthToken):
            return item
        #测试数据库
        #spider.cursor, spider.connect = spider.cursor_test, spider.connect_test
        spider.cursor.execute(
            """insert into uce_token(name, en_name, token, decimal_point, created_at)
                      value (%s, %s, %s, %s, %s)""",
            (
                item['name'],
                item['en_name'],
                item['token'],
                item['decimal_point'],
                item['created_at']
            )
        )
        spider.connect.commit()

        self.redis_update(spider, item)

        return item

    @staticmethod
    def redis_update(spider, item):
        spider.redis.sadd('eth_token', item['token'])
