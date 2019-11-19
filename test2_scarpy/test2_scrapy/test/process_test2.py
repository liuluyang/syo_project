from multiprocessing import Pool, Process, Manager
from websocket import create_connection
from binance.client import Client
import time

class G(object):

    def data_get(self):
        try:
            ws = create_connection("wss://ws.gatei.io/v3/", timeout=2)
            print (ws)
            while True:
                ws.send(
                    '{"id":12312, "method":"ticker.query", "params":["EOS_USDT", 86400]}')
                print ('一次ws',time.time(), ws.recv())
                time.sleep(2)
        except:
            #raise AttributeError('1')
            return '1'

class G2(object):

    def data_get(self):
        ws = create_connection("wss://ws.gateio.io/v3/")
        #print (ws)
        while True:
            ws.send(
                '{"id":12312, "method":"ticker.query", "params":["EOS_USDT", 86400]}')
            print ('一次新ws',time.time(), ws.recv())
            time.sleep(2)

class B(object):

    def data_get(self):
        try:
            api_key = 'VlbfmsWUZR8HeYFyyH251aED8EzoAj7OfhVfgX7BWO1mx5aOzPCbi1zSIrdWpznw'
            api_secret = 'CePdSYImKP9vOSzelsixg9M2gAuKm6XnwQNK1e1m0M69OumeNAd49EMlYRi0LLzj'
            client = Client(api_key, api_secret)
            while True:
                tickers = client.get_ticker()
                print ('一次client',time.time(), tickers)
                time.sleep(2)
        except:
            return '2'

def error(e):
    print ('这是错误信息:',type(e), str(e))
    error_l.append(e)

if __name__ == '__main__':
    d = Manager().dict()
    d['1'] = G().data_get
    d['2'] = B().data_get
    d['3'] = G2().data_get
    error_l = Manager().list()
    p = Pool(2)
    target = [G().data_get, B().data_get]
    r1 = p.apply_async(G().data_get, error_callback=error)
    r2 = p.apply_async(B().data_get, error_callback=error)
    # for t in target:
    #     result = p.apply_async(t, error_callback=error)
    result = [r1, r2]
    while True:
        print ('检查')
        # if error_l:
        #     print ('有服务异常', error_l)
        #     for k in error_l:
        #         p.apply_async(d[k], error_callback=error)
        #     error_l = Manager().list()
        #print (r1.get(), r2.get() , type(r1.get()))
        for num, r in enumerate(result):
            try:
                k = r.get(timeout=1)
                if k:
                    print (k)
                    r3 = p.apply_async(d['3'], error_callback=error)
                    result[num] = r3
            except:
                pass


        #time.sleep(2)
