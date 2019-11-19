import redis
import json
import pandas as pd
from test2_scrapy.test.trades_test.IndexTool import IndexTool


it = IndexTool()

pool = redis.ConnectionPool(host='47.75.223.85', port=6379, db=8,
                                    password='lvjian')
r = redis.Redis(connection_pool=pool)

trade_volume = r.lrange('trade_volume', 0, -1)[::-1]
print(trade_volume)
volume_percent = []
price = []
for d in trade_volume:
    d = json.loads(d.decode())
    if d['status'] == 'ok':
        print(d)
        date = d['date']
        volume_percent.append([date, d['volume_percent']])
        price.append([date, d['price']])

v = pd.DataFrame(volume_percent, columns=['date', 'percent'])
v.index = v.date
v = v.iloc[:, 1:]
print(v)
