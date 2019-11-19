
from websocket import create_connection
import time
import json
"""
[1534381200, '6300', '6273.59', '6300', '6271.43', '4.6190948', '29026.1544342722', 'BTC_USDT']
1534381807
[1534381800, '6273.59', '6273.59', '6273.59', '6273.59', '0', '0', 'BTC_USDT']
"""
#ws = create_connection('ws://127.0.0.1:9001/uce/echo')
print (time.time())
ws = create_connection('wss://ws.gateio.io/v3/')
print (ws)
print (time.time())
data_send_f = {"id":12312, "method":"kline.query", "params":["BTC_USDT", 1, 1516951219, 1800]}

data_now = None
num = 0
time_list = []
while True:
    num+=1
    #ws.send('AE_BTC')
    timestamp = int(time.time())
    print (timestamp)
    one_day = 86400
    params = ["BTC_USDT",timestamp-100,timestamp,60]
    data_send_f['params'] = params
    data_send = json.dumps(data_send_f)
    ws.send(data_send)
    #print ('send now')
    data_recv = ws.recv()
    data_recv = json.loads(data_recv)
    print (data_recv)
    # for i in data_recv['result']:
    #     print (i[0])
    #print(len(data_recv['result']))
    last_data = data_recv['result'][-1]
    print (data_recv['result'][-1])
    if last_data==data_now:
        print ('~~~same')
    else:
        data_now = last_data
        print ('~~~not same')
        time_list.append(num)
        print (time_list)
    time.sleep(1)


