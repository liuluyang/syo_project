
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=1, password='lvjian')
redis_local = redis.Redis(connection_pool=pool)

try:
    redis_local.ping()
except Exception as e:
    print (type(e), e)