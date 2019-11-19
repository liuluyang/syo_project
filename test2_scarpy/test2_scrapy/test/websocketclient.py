
from websocket import create_connection
from websocket import WebSocket, WebSocketApp
import time


ws = create_connection('ws://47.75.223.85:9001')
#ws.close()

while True:
    ws.send('requset 1')
    #print ('send now')
    print(ws.recv())

    time.sleep(2)