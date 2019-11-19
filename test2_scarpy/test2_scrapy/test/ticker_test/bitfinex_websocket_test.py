
from websocket import create_connection
import json, time
import threading
import random

def ticker_thread(num):
    data_send = {
      "event": "subscribe",
      "channel": "ticker",
      "symbol": "tBTCUSD"
    }
    data_send = json.dumps(data_send)

    ws = create_connection('wss://api.bitfinex.com/ws')
    ws.send(data_send)

    while True:
        try:
            data_recv = ws.recv()
            print(num,'_____________', data_recv)
        except:
            time.sleep(random.random()*10)
            ws = create_connection('wss://api.bitfinex.com/ws')
            ws.send(data_send)

if __name__ == '__main__':
    error_num = 0
    for i in range(100):
        t = threading.Thread(target=ticker_thread, args=(i,))
        t.start()
        time.sleep(1)
    pass