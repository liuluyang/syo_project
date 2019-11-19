from websocket import create_connection
import time
import base64
import gzip
import json


ws = create_connection('wss://push.bibox.com/')
print(ws)

data_send = {
  "event": "addChannel",
  "channel": "bibox_sub_spot_BIX_BTC_deals"
}
data_send = json.dumps(data_send)
ws.send(data_send)

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
    data_recv = json.loads(data_recv)[0]
    data_type = data_recv.get('data_type')
    if data_type == 1:
        data = data_recv['data']
        data = inflate(data)
        for d in data:
            d['type'] = 'buy' if d['side'] == 1 else 'sell'
            if d['type'] == 'buy':
                print('买入 ', d)
            else:
                print('卖出 ', d)