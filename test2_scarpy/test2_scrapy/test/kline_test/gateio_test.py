
from websocket import create_connection
# wss://webws.gateio.io/v3/
# wss://ws.gateio.io/v3/
ws = create_connection("wss://webws.gateio.io/v3/")
ws.send('{"id":12312, "method":"kline.subscribe", "params":["BTC_USDT", 900]}')


while True:
    print(ws.recv())
