import redis
import json
from django.http import JsonResponse
from django.shortcuts import render, render_to_response

REDIS_PASSWORD = 'lvjian'
pool_8 = redis.ConnectionPool(host='localhost', port=6379, db=8, password=REDIS_PASSWORD)
redis_8 = redis.Redis(connection_pool=pool_8)


# {'apiKey': 'ee7e9331-f2c6-45e2-b13b-340150d7c685',
# 'secretKey': '1072BFFCF279957C707D06943B9F8EC3',
# 'Passphrase':'G498807gsl',
# 'name':'lvjian',
# 'leverage':10,
# 'size':10,
# 'is_host':0,
#
#  'loss':-4,
#  'profit':0,
#  'type':'5min',
#  'ma1':7,
#  'ma2':30,
#  }

def setting_data_get(request):
    if request.method == 'GET':
        data_redis_get = redis_8.hget('setting_data', 'lvjian')
        if data_redis_get:
            data_redis_get = json.loads(data_redis_get.decode())
            data = data_redis_get
        return render_to_response('setting_data.html', locals())
    if request.method == 'POST':
        keys = ['apiKey', 'secretKey', 'Passphrase', 'leverage', 'size', 'is_host',
                'loss', 'profit', 'type',  'ma1',  'ma2'
                ]
        data_redis = {}
        for k in keys:
            v = request.POST.get(k)
            if k in ['leverage', 'size', 'is_host', 'loss', 'profit','ma1', 'ma2']:
                v = int(v)
            data_redis[k] = v
        print(data_redis)
        redis_8.hset('setting_data', 'lvjian', json.dumps(data_redis))
        return JsonResponse({'status':'ok'})

