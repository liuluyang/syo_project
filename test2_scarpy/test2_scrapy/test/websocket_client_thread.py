import websocket
import time
import threading
import json
import redis

#SERVER_URL = "ws://127.0.0.1:9001/uce/echo"
SERVER_URL = "wss://ws.gateio.io/v3/"
pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
r = redis.Redis(connection_pool=pool)

def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    # markets = r.smembers('gateio_market')
    # data_send_f = {'id': 1, 'method': 'ticker.query', 'params': None}
    def send_trhead():
        #send_info = 'AE_BTC'
        send_info = '{"id":1, "method":"ticker.query", "params":["BTC_USDT", 86400]}'
        while True:
            time.sleep(1)
            ws.send(send_info)

    t = threading.Thread(target=send_trhead)
    t.start()




def on_start(a):
    print (a)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(SERVER_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


from threadpool import ThreadPool, makeRequests
if __name__ == "__main__":
    pool = ThreadPool(1)
    test = list()
    for ir in range(1):
        test.append(ir)
    requests = makeRequests(on_start, test)
    [pool.putRequest(req) for req in requests]
    pool.wait()