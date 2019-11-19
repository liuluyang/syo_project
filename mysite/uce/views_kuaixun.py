#coding:utf8


from django.shortcuts import render_to_response, HttpResponse
from django.http import JsonResponse

from uce.models import Spider_kuaixun
from mysite.settings import REDIS_PASSWORD
import uwsgi
import redis


pool = redis.ConnectionPool(host='localhost', port=6379, db=0, password=REDIS_PASSWORD)
redis_client = redis.Redis(connection_pool=pool)

def push_message(request):
    uwsgi.websocket_handshake()
    pub = redis_client.pubsub()
    pub.subscribe('kuaixun_bsj')
    while True:
        try:
            msg = pub.parse_response(block=False, timeout=10)
            print(msg)
            if not msg or msg[-1]==1:
                uwsgi.websocket_send('0')
            else:
                print(msg[-1].decode())
                uwsgi.websocket_send('1')
        except:
            pub.unsubscribe('kuaixun_bsj')
            print ('websocket client离开并取消订阅')
            break
