import redis

"""
redis数据库迁移
"""

def redis_link(host, db, passwd='lvjian'):
    pool = redis.ConnectionPool(host=host, port=6379, db=db, password=passwd)
    redis_obj = redis.Redis(connection_pool=pool)

    return redis_obj

redis_from = redis_link(host='47.52.115.31',db=2)
redis_to = redis_link(host='localhost', db=2)

if __name__ == '__main__':
    # key_list = ['news_urls', 'newsletter_urls', 'mblog_urls', 'currency_name']
    # for key_name in key_list:
    #     members = redis_from.smembers(key_name)
    #     print (members)
    #     redis_to.sadd(key_name, *members)

    # key_list = ['gateio_ticker_new', 'binance_ticker_new', 'okex_ticker_new',
    #             'huobi_ticker_new']
    # for key_name in key_list:
    #     members = redis_from.hgetall(key_name)
    #     print(members)
    #     redis_to.hmset(key_name, members)

    key_list = ['binance_market']
    for key_name in key_list:
        members = redis_from.hgetall(key_name)
        print(len(members), members)
        redis_to.hmset(key_name, members)
