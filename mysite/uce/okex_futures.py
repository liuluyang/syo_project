import redis
import json
from django.http import JsonResponse

REDIS_PASSWORD = 'lvjian'
pool_6 = redis.ConnectionPool(host='localhost', port=6379, db=6, password=REDIS_PASSWORD)
redis_6 = redis.Redis(connection_pool=pool_6)

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

def currency_data_get(request):
    if request.method == 'GET':
        currency = request.GET.get('currency')
        type = request.GET.get('type')
        page = request.GET.get('page')
        size = request.GET.get('size')
        try:
            page = int(page) if page and int(page) > 0 else 1
            size = int(size) if size and int(size) > 0 else 50
        except:
            result = error('参数错误')
            return JsonResponse(result)
        if currency:
            data = redis_6.hgetall(currency.lower())
            data = redis_data_decode(data)
            if data:
                types = type.split(',') if type else None
                data_filter = {}
                if types:
                    for t in types:
                        data_filter[t] = data.get(t)
                else:
                    data_filter = data
                blastingOrders = data_filter.get('blastingOrders')
                if blastingOrders:
                    index_num = (page - 1) * size
                    data_filter['blastingOrders']['list'] = \
                    data['blastingOrders']['list'][index_num:index_num + size]
                    data_filter['page'] = page
                    data_filter['size'] = size
                if data_filter:
                    result = success(data=data_filter, currency=currency)
                    return JsonResponse(result)
        result = error('参数错误')
        return JsonResponse(result)

def futures_spots_kline_get_all(request):
    if request.method == 'GET':
        currencies = request.GET.get('currencies')
        if currencies:
            currencies = [c.lower() for c in currencies.split(',')]
        else:
            currencies = 'btc,ltc,eth,etc,eos,xrp'.split(',')
        result = {}
        for c in currencies:
            data = redis_6.hgetall(c)
            data = redis_data_decode(data)
            data = data.get('futures_spots_kline')
            result[c] = data
        result = success(data=result)
        return JsonResponse(result)

def blasting_orders_get_all(request):
    if request.method == 'GET':
        page = request.GET.get('page')
        size = request.GET.get('size')
        try:
            page = int(page) if page and int(page)>0 else 1
            size = int(size) if size and int(size)>0 else 50
        except:
            result = error('参数错误')
            return JsonResponse(result)
        data = redis_6.hgetall('global')
        data = redis_data_decode(data)
        index_num = (page-1)*size
        data['blastingOrders']['list'] = data['blastingOrders']['list'][
                                         index_num:index_num + size]
        data['page'] = page
        data['size'] = size
        result = success(data=data)
        return JsonResponse(result)

def currency_get_all(request):
    if request.method == 'GET':
        symbols = 'btc,ltc,eth,etc,eos,xrp'.split(',')
        symbols = [s.upper() for s in symbols]
        img_url = 'https://topcoin.oss-cn-hangzhou.aliyuncs.com/leekassit/img/{}.png'
        img_urls = {}
        for symbol in symbols:
            img_urls[symbol] = img_url.format(symbol)
        result = success(data={'currencies': symbols, 'img_urls': img_urls})
        return JsonResponse(result)