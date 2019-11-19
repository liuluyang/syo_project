
from websocket import create_connection
import time, json, random
import threading

class ZbTrade(object):
    
    def __init__(self):
        pass
    
    def socket_ping(self):
        while True:
            time.sleep(10)
            try:
                self.ws.send('{"ping":"123"}')
            except Exception as e:
                print('~~~~~~~~~~~~~~~ ping异常')
    
    def trade_get(self):
        symbol = 'btcusdt'
        data_send = {'event': 'addChannel',
                     'channel': '{}_trades'.format(symbol)}
        data_send = json.dumps(data_send)
        self.ws = create_connection('wss://api.zb.cn:9999/websocket')
        self.ws.send(data_send)

        while True:
            try:
                data_recv = self.ws.recv()
                data_recv = json.loads(data_recv)
                data = data_recv.get('data')
                if not data:
                    print(data_recv)
                    continue
                for d in data:
                    is_buy = True if d['type'] == 'buy' else False
                    if is_buy:
                        print('买入：', d)
                    else:
                        print('卖出：', d)
                print('__________________')
            except Exception as e:
                print('!!!!!!!!!! 数据处理异常', e)
                while True:
                    try:
                        self.ws = create_connection('wss://api.zb.cn:9999/websocket')
                        self.ws.send(data_send)
                        break
                    except Exception as e:
                        print('???????????? websocket连接异常', e)
                        time.sleep(random.random())

    
    def main(self):
        t = threading.Thread(target=self.trade_get)
        t.start()

        # t = threading.Thread(target=self.socket_ping)
        # t.start()

if __name__ == '__main__':
    z = ZbTrade()
    z.main()