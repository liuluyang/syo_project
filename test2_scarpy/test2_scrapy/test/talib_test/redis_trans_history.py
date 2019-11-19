
import redis
import json
pool = redis.ConnectionPool(host='47.75.223.85', port=6379, db=8, password='lvjian')
redis_remot = redis.Redis(connection_pool=pool)

profit = 0
pp = []
nn = []
price = 0
try:
    redis_remot.ping()
    print('ok')
    trans = redis_remot.lrange('trans_new_5', 0, -1)[::-1][250:]
    for index, d in enumerate(trans):
        d = json.loads(d.decode())
        #print(d)

        p = 0
        signal_text = d.get('signal_text')
        if signal_text in  ['开空', '开多']:
            price = d['price']
            # p = d['price'] - price
            # profit += p
            # price = d['price']
        else:
            if signal_text == '平空':
                p = price - d['price']
            elif signal_text == '平多':
                p = d['price'] - price
            profit += p
        # elif d['signal_text'] == '开多 平空' and price != 0:
        #     p = price - d['price']
        #     profit += p
        #     price = d['price']
        # if price == 0:
        #     price = d['price']
        p = round(p, 3)
        print(d, p)
        # if d['p'] > 0:
        #     #print(trans[index-1])
        #     print(d)
        # p = d.get('p', 0)
        # signal = ''
        # if p>0:
        #     pp.append(p)
        #     signal = '>>>>>>>>>>>>>'
        # elif p<0:
        #     nn.append(p)
        #     signal = '-------------'
        # profit += p

        # print(index, d, round(profit, 2)*100, signal)
    # print(profit)
    # print(pp.sort(), sum(pp), len(pp), pp)
    # print(nn.sort(), sum(nn), len(nn), nn)
    print(profit)
except Exception as e:
    print (type(e), e)