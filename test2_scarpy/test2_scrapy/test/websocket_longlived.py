import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import threading
import time
import redis
import json

pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
r = redis.Redis(connection_pool=pool)

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    markets = r.smembers('gateio_market')
    data_send_f = {'id': 1, 'method': 'ticker.query', 'params': None}
    # while True:
    for market in markets:
        market = market.decode('utf8')
        data_send_f['params'] = [market, 86400]
        data_send = json.dumps(data_send_f)
        def run(data_send):
            time.sleep(0.01)
            ws.send(data_send)
        #run(data_send)
        t = threading.Thread(target=run, args=(data_send,))
        t.start()
        time.sleep(0.02)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.gateio.io/v3/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()