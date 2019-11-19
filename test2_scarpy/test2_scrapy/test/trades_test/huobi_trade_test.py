from websocket import create_connection
import gzip
import json
ws = create_connection('wss://api.huobi.pro/ws')
data_send = {"sub": "market.shebtc.trade.detail"}
data_send = json.dumps(data_send)
ws.send(data_send)

while True:
    data_recv = ws.recv()
    data_recv = gzip.decompress(data_recv).decode('utf8')
    data_recv = json.loads(data_recv)
    print (data_recv)

    if data_recv.get('ping'):
        ws.send(json.dumps({'pong':data_recv.get('ping')}))
    else:
        data = data_recv.get('tick', {}).get('data', None)
        if data:
            for d in data:
                print(d)
