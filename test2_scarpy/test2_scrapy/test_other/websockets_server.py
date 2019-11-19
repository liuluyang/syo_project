import asyncio
import websockets
import time
# async def echo(websocket, path):
#     async for message in websocket:
#         await websocket.send(message)
#
# asyncio.get_event_loop().run_until_complete(
#     websockets.serve(echo, 'localhost', 8765))
# asyncio.get_event_loop().run_forever()

data = '{"name":"ll","num":"22"}'
#单线程
async def hello(websocket, path):
    #while True:
    name = await websocket.recv()
    print(f"A new client : {name}")
    greeting = "Welcome " + name
    time.sleep(5)
    await websocket.send(data)
    print(f"send '{greeting}' to '{name}'")


start_server = websockets.serve(hello, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
