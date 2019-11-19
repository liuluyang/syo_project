#coding:utf8


import redis
from test_scrapy.redis_link import LinkRedis

def link():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    #r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    print (type(r.get('a')))

    value = str(r.get('b'), encoding='utf8')
    print (type(value), value)
    print (r.smembers('url'), r.sismember('url', 'a'))




if __name__ == '__main__':
    #link()
    r = LinkRedis().r
    print (r.sismember('pic_ids', 'a'))
    pass