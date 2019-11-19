
from websocket import create_connection
ws = create_connection("wss://ws.gateio.io/v3/")
#ws.send('{"id":12312, "method":"ticker.subscribe", "params":["BTC_USDT"]}')
ws.send('{"id":12312, "method":"ticker.update","params":["BTC_USDT"]}')
while True:
    print ('waiting...')
    print(ws.recv())