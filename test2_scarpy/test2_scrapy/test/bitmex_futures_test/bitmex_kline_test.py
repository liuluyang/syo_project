import requests
import threading

def kline_get():
    r = requests.get('https://www.bitmex.com/api/udf/history?'
            'symbol=LTCZ18&resolution=1&from=1542953295&to=1543125839')

    headers = r.headers
    print(headers.get('X-RateLimit-Limit'))
    print(headers.get('X-RateLimit-Remaining'))
    # for k, v in headers.items():
    #     print(k, v)
    # for k,v in r.json().items():
    #     print(k, v)

for i in range(5):
    t = threading.Thread(target=kline_get)
    t.start()


