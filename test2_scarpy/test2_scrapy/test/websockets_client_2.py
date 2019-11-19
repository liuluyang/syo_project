import asyncio
import websockets

# async def hello(uri):
#     async with websockets.connect(uri) as websocket:
#         await websocket.send("Hello world!")
#
# asyncio.get_event_loop().run_until_complete(
#     hello('ws://localhost:8765'))


async def hello():
	async with websockets.connect('ws://localhost:8765') as websocket:
		name = input("what's your name?")
		await websocket.send(name)
		print(f"send server:{name}")
		greeting = await websocket.recv()
		print(f"receive from server:{greeting}")
asyncio.get_event_loop().run_until_complete(hello())