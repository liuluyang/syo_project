
import redis

pool = redis.ConnectionPool(host='203.195.153.53', port=6379, db=0,
                              password='lvjian')
redis_client = redis.Redis(connection_pool=pool)
ps = redis_client.pubsub()
ps.subscribe('kuaixun_bsj')

#print (redis_client.hgetall('binance_market'))

#ok
# for item in ps.listen():
#     print (item)
num = 0
while True:
    msg = ps.parse_response(block=False, timeout=10)
    print (msg)
    if not msg or msg[-1] == 1:
        pass
        #uwsgi.websocket_send('0')
    else:
        num+=1
        print(msg[-1].decode())
        #uwsgi.websocket_send('1')
    print ('当前有%s条新消息未读'%(num))

# l = ps.listen()
# while True:
#     data = next(l)
#     print (data)



