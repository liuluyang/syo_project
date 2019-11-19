import redis
from settings import REDIS_HOST, REDIS_PASSWORD

#market list and exchange rate
pool_2 = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=2,
                              password=REDIS_PASSWORD)
redis_2 = redis.Redis(connection_pool=pool_2)

#ticker
pool_3 = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=3,
                              password=REDIS_PASSWORD)
redis_3 = redis.Redis(connection_pool=pool_3)

#short_elves
pool_4 = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=4,
                              password=REDIS_PASSWORD)
redis_4 = redis.Redis(connection_pool=pool_4)

#futures
pool_6 = redis.ConnectionPool(host=REDIS_HOST, port=6379, db=6,
                              password=REDIS_PASSWORD)
redis_6 = redis.Redis(connection_pool=pool_6)
