import asyncio
import requests

class B(object):
    async def hello(self):
        print("Hello world!")
        #r = await asyncio.sleep(1)
        requests.get('http://www.baidu.com')
        print("Hello again!")

b = B()
loop = asyncio.get_event_loop()
tasks = [b.hello(), b.hello(), b.hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()


