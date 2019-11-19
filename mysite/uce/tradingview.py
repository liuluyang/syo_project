import redis
import json
from django.http import JsonResponse
import pymysql

MYSQL_REMOTE = {'host':'47.75.163.235', 'port':3306, 'db':'bitbcs_com', 'user':'bitbcs_com',
         'passwd':'Z76fXifXJbeGWp3T', 'use_unicode':True}
# MYSQL_REMOTE = {'host':'localhost', 'port':3306, 'db':'lvjian_test', 'user':'root',
#          'passwd':'123456', 'use_unicode':True}

REDIS_PASSWORD = 'lvjian'
pool_1 = redis.ConnectionPool(host='localhost', port=6379, db=1, password=REDIS_PASSWORD)
redis_1 = redis.Redis(connection_pool=pool_1)

def error(error):
    return {'error':error, 'data':None}

def success(**kwargs):
    SUCCESS = {'error': None, 'data': 'data'}
    SUCCESS.update(kwargs)
    return SUCCESS

def redis_data_decode(data):
    data = {k.decode(): json.loads(v.decode()) for k, v in
            data.items()} if data else {}
    return data

def tradingview_idea_get(request):
    if request.method == 'GET':
        data = redis_1.hget('tradingview', 'idea')
        if data:
            data = json.loads(data.decode())
            result = success(data=data)
            return JsonResponse(result)
        else:
            result = error('数据获取失败')
            return JsonResponse(result)

def remind_history(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        try:
            connection = pymysql.connect(**MYSQL_REMOTE,
                                         cursorclass=pymysql.cursors.DictCursor)
            cursor = connection.cursor()
            cursor.execute(
                """
                select * from uce_remind_history where user_id=%s order by created_at
                 desc limit 30
                """, (user_id)
            )
            history = cursor.fetchall()
            connection.commit()
            for per in history:
                per['created_at'] = str(per['created_at'])
            result = success(data={"history":history})
            return JsonResponse(result)
        except:
            result = error('数据获取失败')
            return JsonResponse(result)
