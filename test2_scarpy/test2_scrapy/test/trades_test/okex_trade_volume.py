from websocket import create_connection
import json
import time
import zlib
import redis
import copy
import threading

class TradeVolume(object):

    def __init__(self):
        self.buy = 1
        self.sell = 1
        self.price = 0

    def data_redis(self, data):
        """
        存入redis
        :param data: 
        :return: 
        """
        pool = redis.ConnectionPool(host='localhost', port=6379, db=8,
                                    password='lvjian')
        r = redis.Redis(connection_pool=pool)
        data['date'] = time.strftime('%Y-%m-%d %X', time.localtime())
        data['timestamp'] = time.time()
        data = json.dumps(data)
        r.lpush('trade_volume', data)

    def inflate(self, data):
        """
        数据解码
        :param data: 
        :return: 
        """
        decompress = zlib.decompressobj(
                -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated

    def trade_get(self):
        """
        获取交易量
        :return: 
        """
        send_f = {'event': 'addChannel','channel': 'ok_sub_spot_eos_usdt_deals'}
        ws = create_connection('wss://real.okex.com:10441/websocket')
        ws.send(json.dumps(send_f))

        while True:
            try:
                data_recv = ws.recv()
                data_recv = self.inflate(data_recv).decode()
                data_recv = json.loads(data_recv)
                data = data_recv[0]
                if data['binary'] == 0:
                    data = data['data']
                    for d in data:
                        self.price = float(d[1])
                        if d[-1] == 'bid':
                            self.buy += float(d[-3])
                        else:
                            self.sell += float(d[-3])
                    print(data, '买: {} 卖: {}'.format(self.buy,self.sell), round(self.buy/self.sell, 2))
            except Exception as e:
                error  = {'status':'error', 'error':str(e)}
                self.data_redis(error)
                while True:
                    try:
                        time.sleep(1)
                        ws = create_connection('wss://real.okex.com:10441/websocket')
                        ws.send(json.dumps(send_f))
                        break
                    except Exception as e:
                        error = {'status': 'error', 'error': str(e)}
                        self.data_redis(error)

    def recording(self):
        """
        数据计算
        :return: 
        """
        buy, sell, price = copy.deepcopy(self.buy), copy.deepcopy(self.sell), self.price
        self.buy = self.sell = 1
        volume_percent = round(buy/sell, 2)
        data = {'volume_percent':volume_percent, 'buy':buy, 'sell':sell, 'price':price}
        data['status'] = 'ok'
        self.data_redis(data)

    def main(self):
        """
        主函数
        :return: 
        """
        t = threading.Thread(target=self.trade_get)
        t.start()
        while True:
            try:
                time.sleep(60)
                self.recording()
            except Exception as e:
                error = {'status': 'error', 'error': str(e)}
                self.data_redis(error)


if __name__ == '__main__':
    t = TradeVolume()
    t.main()
