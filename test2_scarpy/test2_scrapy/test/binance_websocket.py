
from websocket import create_connection

import time
import json
#ws = create_connection('wss://stream.binance.com:9443/ws/btcusdt@ticker')
#ws = create_connection('wss://stream.binance.com:9443/ws/!miniTicker@arr')
ws = create_connection('wss://stream.binance.com:9443/ws/!ticker@arr')
#ws = create_connection('wss://stream.binance.com:9443/stream?streams=bnbbtc@ticker/btcusdt@ticker')
print (ws)
while True:
    data_recv = ws.recv()
    data_recv = json.loads(data_recv)
    #print (ws.recv())
    print (type(data_recv),len(data_recv),data_recv)


# import websocket
# import websocket
# import threading
# import time
#
# def on_message(ws, message):
#     print(message)
#
# def on_error(ws, error):
#     print(error)
#
# def on_close(ws):
#     print("### closed ###")
#
# def on_open(ws):
#     def run(*args):
#         for i in range(3):
#             time.sleep(1)
#             data = ws.recv()
#             print(data)
#         time.sleep(1)
#         ws.close()
#         print("thread terminating...")
#     #thread.start_new_thread(run, ())
#
#
#
# websocket.enableTrace(True)
# ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/bnbbtc@ticker",
#                             on_message = on_message,
#                             on_error = on_error,
#                             on_close = on_close)
# ws.on_open = on_open
#
# ws.run_forever()
