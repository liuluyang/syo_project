
from websocket import create_connection
import threading
import  time

ws_list = [create_connection("wss://ws.gateio.io/v3/") for i in range(10)]
error = set()

def ping(ws, num=None):
    try:
        ws.send('{"id":12312, "method":"server.ping", "params":[]}')
        print('返回值',num, ws.recv())
    except:
        error.add(ws)
        print (error)
    # ws.send('{"id":12312, "method":"server.ping", "params":[]}')
    # print('返回值', num, ws.recv())
    pass

is_f = True
while True:
    for i in range(10):
        print (i, ws_list[i])
        if is_f and i==5:
            ws_list[i].close()
            is_f = False
        for y in range(3):
            t = threading.Thread(target=ping, args=(ws_list[i], i))
            t.start()

    time.sleep(10)
    if error:
        for i in error:
            ws_list.remove(i)
            ws_list.append(create_connection("wss://ws.gateio.io/v3/"))
        error = set()


