#coding:utf8


import redis

#连接redis数据库
class LinkRedis(object):
    def __init__(self, db=1):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=db, password='lvjian')
        self.redis = redis.Redis(connection_pool=pool)