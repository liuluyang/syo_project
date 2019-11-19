import requests
import threading
import time

def data_get():
    r = requests.get('http://47.52.115.31/v1/okex-futures/futures-spots-kline-all/').json()
    print(r)


for i in range(100):
    t = threading.Thread(target=data_get)
    t.start()
    time.sleep(0.1)
