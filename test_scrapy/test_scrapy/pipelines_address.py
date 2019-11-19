
from test_scrapy.items import TokenAddress, TokenTransaction
from test_scrapy.settings import address_change
import json

class TokenAddressPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not isinstance(item, TokenAddress):
            if isinstance(item, TokenTransaction):
                # 测试数据库
                #spider.cursor, spider.connect = spider.cursor_test, spider.connect_test
                self.token_transaction(item, spider)
            return item
        # 测试数据库
        #spider.cursor, spider.connect = spider.cursor_test, spider.connect_test
        token = item['token']
        time_now = item['time_now']
        data_list = item['data_list']
        top_list = item['top_list']
        if not spider.redis.sismember('token_address', token):
            for data in data_list:
                spider.cursor.execute(
                    """insert into uce_token_address(panking, address, market, 
                              amount, percent, token, created_at)
                              value (%s, %s, %s, %s, %s, %s, %s)""",
                    (
                        data['panking'],
                        data['address'],
                        data['market'],
                        data['amount'],
                        data['percent'],
                        token,
                        time_now
                    )
                )
            self.redis_update(spider, item)
        else:
            for data in data_list:
                spider.cursor.execute(
                    """update uce_token_address set address=%s, market=%s, 
                              amount=%s, percent=%s, updated_at=%s where 
                              token=%s and panking=%s""",
                    (
                        data['address'],
                        data['market'],
                        data['amount'],
                        data['percent'],
                        time_now,
                        token,
                        data['panking'],
                    )
                )

        #抓取历史记录
        spider.cursor.execute(
            """insert into uce_token_history(addresses, top_10, top_20, top_50,
                      top_100, token, created_at)
                      value (%s, %s, %s, %s, %s, %s, %s)""",
            (
                item['addresses'],
                top_list[0],
                top_list[1],
                top_list[2],
                top_list[3],
                token,
                time_now
            )
        )

        #币址历史记录
        for data in data_list:
            spider.cursor.execute(
                """insert into uce_token_address_detail(panking, address, market, 
                          amount, percent, token, created_at)
                          value (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    data['panking'],
                    data['address'],
                    data['market'],
                    data['amount'],
                    data['percent'],
                    token,
                    time_now
                )
            )
        spider.connect.commit()
        self.transaction_amount(item, spider)

        return item

    @staticmethod
    def redis_update(spider, item):
        spider.redis.sadd('token_address', item['token'])

    def transaction_amount(self, item, spider):
        """
        top20持币数量大量增加减少 监控数据存储
        :param item: 
        :param spider: 
        :return: 
        """
        token = item['token']
        time_now = item['time_now']
        top_amount_list = item['top_amount_list']
        top20_amount = top_amount_list[1]

        result = spider.redis.hget('token_transaction', token)
        if result is not None:
            amount_befor = json.loads(result.decode())['amount']
            amount_change = top20_amount-amount_befor
            amount_abs = abs(amount_change)
            if amount_abs > address_change:
                is_up = 1 if amount_change>0 else -1
                is_enter = 0
                spider.cursor.execute(
                    """insert into uce_token_transaction(token, is_up, is_enter,
                              amount, created_at) value (%s, %s, %s, %s, %s)""",
                    (
                        token,
                        is_up,
                        is_enter,
                        amount_abs,
                        time_now
                    )
                )
                spider.connect.commit()

        result = {'amount':top20_amount, 'created_at':time_now}
        spider.redis.hset('token_transaction', token, json.dumps(result))

    def token_transaction(self, item, spider):
        """
        单笔大额充币提币 监控数据存储
        :param item: 
        :param spider: 
        :return: 
        """
        spider.cursor.execute(
            """insert into uce_token_transaction(address, token, is_up, is_enter,
              amount, market, created_at) value (%s, %s, %s, %s, %s, %s, %s)""",
            (
                item['address'],
                item['token'],
                0,
                item['is_enter'],
                item['amount'],
                item['market'],
                item['time_now']
            )
        )
        spider.connect.commit()

        return item
