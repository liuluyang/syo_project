from websocket import create_connection
import json
import zlib

"""
合约指数 本周 下周 季度(价)
"""

def index_price():
    symbols = 'btc,ltc,eth,etc,bch,eos,xrp,btg'.split(',')
    send_list = []
    for symbol in symbols:
        send_1 = {'event': 'addChannel',
                  'channel': 'ok_sub_futureusd_{}_ticker_this_week'.format(symbol)}
        send_2 = {'event': 'addChannel',
                  'channel': 'ok_sub_futureusd_{}_ticker_next_week'.format(symbol)}
        send_3 = {'event': 'addChannel',
                  'channel': 'ok_sub_futureusd_{}_ticker_quarter'.format(symbol)}
        send_index = {'event': 'addChannel',
                      'channel': 'ok_sub_futureusd_{}_index'.format(symbol)}
        send_list.extend([send_1, send_2, send_3, send_index])

    ws = create_connection('wss://real.okex.com:10440/ws/v1')
    ws.send(json.dumps(send_list))


    def inflate(data):
        decompress = zlib.decompressobj(
                -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated

    while True:
        data_recv = ws.recv()
        data_recv = inflate(data_recv)
        print(data_recv)

index_price()