from websocket import create_connection
import json
import time

import zlib

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

send_f = {'event': 'addChannel','channel': 'ok_sub_spot_eos_usdt_deals'}
ws = create_connection('wss://real.okex.com:10441/websocket')
ws.send(json.dumps(send_f))

buy = 0
sell = 0


while True:
    try:
        data_recv = ws.recv()
        data_recv = inflate(data_recv).decode()
        data_recv = json.loads(data_recv)

        data = data_recv[0]
        if data['binary'] == 0:
            data = data['data']
            for d in data:
                if d[-1] == 'bid':
                    buy += float(d[-3])
                else:
                    sell += float(d[-3])
            print(data, '买: {} 卖: {}'.format(buy,sell), round(buy/sell, 2))
    except Exception as e:
        time.sleep(1)
        ws = create_connection('wss://real.okex.com:10441/websocket')
        ws.send(json.dumps(send_f))
