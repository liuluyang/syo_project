from websocket import create_connection
import time
import base64
import gzip
import json


ws = create_connection('wss://push.bibox.com/')
print(ws)

data_send = {
  "event": "addChannel",
  "channel": "bibox_sub_spot_BIX_BTC_kline_1min"
}
data_send = json.dumps(data_send)
ws.send(data_send)

data_remove = {
  "event": "removeChannel",
  "channel": "bibox_sub_spot_BIX_BTC_kline_1min"
}
data_remove = json.dumps(data_remove)

def inflate(data):
    """
    解压数据
    :param data: 
    :return: 
    """
    data = base64.b64decode(data)
    data = gzip.decompress(data)
    data = json.loads(data.decode())

    return data

while True:
    data_recv = ws.recv()
    data_recv = json.loads(data_recv)
    print(data_recv)
    data_recv = data_recv[0]
    data_type = data_recv.get('data_type')
    data = data_recv['data']
    data = inflate(data)
    if data_type == 1:
        print(data)
    else:
        pass
        #print(len(data), data)
    ws.send(data_remove)
    ws.send(data_send)
    time.sleep(1)