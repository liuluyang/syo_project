

from websocket import create_connection

# ws = create_connection('ws://127.0.0.1:8000/uce/echo')
#
# for i in range(4):
#     ws.send('hello')
#     print (ws.recv())
#
# # ws.send('once')
# # print (ws.recv())
# ws.close()
ws_list = [create_connection('ws://127.0.0.1:8000/uce/echo') for i in range(100)]
while True:
    for num,ws in enumerate(ws_list):
        ws.send(str(num))
        print(ws.recv())

# for w in ws_list:
#     w.close()