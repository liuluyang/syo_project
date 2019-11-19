from websocket import create_connection
import json
import pandas as pd
import time

def data_kline_get():
    """
    kline数据获取
    :return: 
    """
    data_send = {'market': 'okex', 'method': 'kline', 'symbol': 'BTC_USDT',
         'params': {'num': 2000, 'period': 3600 * 24}, 'id': 1}
    data_send = json.dumps(data_send)
    ws = create_connection('ws://47.52.115.31/v1/market/')
    ws.send(data_send)

    data_recv = ws.recv()
    data = json.loads(data_recv)['data']
    for d in data:
        for i in range(1, 6):
            d[i] = float(d[i])
        d[0] = time.strftime('%Y-%m-%d %X', time.localtime(d[0]/1000))

    dataFrame = pd.DataFrame(data, columns=['date', 'close', 'high', 'low', 'open', 'volume'])
    dataFrame.index = dataFrame.date
    dataFrame = dataFrame.iloc[:, 1:]

    return dataFrame