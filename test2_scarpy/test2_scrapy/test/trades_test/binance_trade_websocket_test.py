from websocket import create_connection
import threading
import redis
import time
import json
from queue import Queue



def redis_link(host, db, passwd='lvjian'):
    pool = redis.ConnectionPool(host=host, port=6379, db=db, password=passwd)
    redis_obj = redis.Redis(connection_pool=pool)

    return redis_obj

redis_2 = redis_link(host='localhost',db=2)
redis_3 = redis_link(host='localhost',db=3)
symbols = redis_2.hgetall('binance_market')
symbols = {k.decode():v.decode().lower() for k,v in symbols.items()}
print (symbols)
symbols = {'BTC_USDT':'btcusdt'}

times = {}

def trade_get(k_name, v_name, q):
    ws = create_connection('wss://stream.binance.com:9443/ws/{}@trade'.format(v_name))
    while True:
        data_recv = ws.recv()
        data_recv = json.loads(data_recv)
        print(data_recv)
        q.put({'symbol':k_name, 'data':data_recv})
        if k_name in times:
            times[k_name] += 1
        else:
            times[k_name] = 1

def tickers_get():
    tickers = redis_3.hgetall('binance_ticker_new')
    tickers = {k.decode():json.loads(v.decode()) for k,v in tickers.items()}

    return tickers

def data_compare(q, tickers, num):

    while True:
        data = q.get()
        symbol, data = data['symbol'], data['data']
        if symbol in tickers:
            usd_price = tickers[symbol]['usd_price']
            if usd_price*float(data['q']) >= 1000:
                time_trade = time.strftime('%Y-%m-%d %X',time.localtime(data['E']/1000))
                time_now = time.strftime('%Y-%m-%d %X',time.localtime())
                print (time_trade, time_now)
                print ('线程：{}'.format(num),data)
                pass

        q.task_done()

if __name__ == '__main__':
    tickers = tickers_get()
    q = Queue()

    for i in range(10):
        t = threading.Thread(target=data_compare, args=(q, tickers, i))
        t.setDaemon(True)
        t.start()

    for k,v in symbols.items():
        t = threading.Thread(target=trade_get, args=(k,v, q))
        t.start()
    print ('start')
    while True:
        print (times)
        print ('管道队列剩余任务:', q.qsize())
        time.sleep(1)
