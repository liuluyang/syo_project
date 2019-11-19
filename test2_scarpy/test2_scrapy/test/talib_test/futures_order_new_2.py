import hmac
import base64
import requests
import json
import time
import redis


users_data = [
{'apiKey': '146537f4-7692-4821-ad5a-af03c8cca385',
'secretKey': '9681E893CC577593280A82FB43B3DD43',
'Passphrase':'lly123456',
'name':'liuluyang',
'leverage':10,
'size':1,
'is_host':1,

 'loss':-4,
 'profit':0,
 'type':'5min',
 'ma1':7,
 'ma2':30,
 },
]

loss_fixed = -4

long_start_ratio = 1
long_ratio = -4
short_start_ratio = 1
short_ratio = -4
instrument_id = "EOS-USD-190628"
timestamp = str(round(time.time(), 3))

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'


def data_redis(data):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=8, password='lvjian')
    r = redis.Redis(connection_pool=pool)
    time_now = time.strftime('%Y-%m-%d %X', time.localtime())
    data['updated_at'] = time_now
    data.pop('apiKey', 0)
    data.pop('secretKey', 0)
    data.pop('Passphrase', 0)
    data = json.dumps(data)
    r.lpush('order_history_5', data)


# signature
def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


# set request header
def get_header(api_key, sign, timestamp, passphrase):
    header = dict()
    header[CONTENT_TYPE] = APPLICATION_JSON
    header[OK_ACCESS_KEY] = api_key
    header[OK_ACCESS_SIGN] = sign
    header[OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[OK_ACCESS_PASSPHRASE] = passphrase
    return header


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]


def setting_data_get():
    """
    获取配置信息
    :return: 
    """
    # pool = redis.ConnectionPool(host='localhost', port=6379, db=8, password='lvjian')
    # r = redis.Redis(connection_pool=pool)
    # data = r.hget('setting_data', 'lvjian')
    # data = json.loads(data.decode())
    # print(type(data), data)
    data = users_data[0]
    return data


def position_size_get(**kwargs):
    """
    获取仓位多少
    :param kwargs: 
    :return: 
    """
    timestamp = str(round(time.time(), 3))
    base_url = 'https://www.okex.me'
    request_path = '/api/futures/v3/{}/position'.format(instrument_id)
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                                                        request_path, '',
                                                        kwargs.get(
                                                            'secretKey')),
                        timestamp,
                        kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    if result.get('result') is True:
        print(status_code, result)
        result = result.get('holding', [{}])[0]
        long_qty, short_qty = int(result.get('long_avail_qty', 0)), \
                              int(result.get('short_avail_qty', 0))
        return long_qty, short_qty
    return 0,0


#1:开多 2:开空 3:平多 4:平空
#开仓平仓
def futures_order(**kwargs):
    try:
        type = kwargs.get('type')
        size = kwargs.get('size', 1)
        long, short = position_size_get(**kwargs)
        if (long > 0 and type=='1') or (short > 0 and type=='2'):
            return
        if type in ['3', '4']:
            #long, short = position_size_get(**kwargs)
            size = long if type == '3'else short
        timestamp = str(round(time.time(), 3))
        base_url = 'https://www.okex.me'
        request_path = '/api/futures/v3/order'
        params = {"client_oid": "lvjiantest20190227","instrument_id":instrument_id,
                  "type":type,"price":"","size":size,"match_price":"1",
                  "leverage":kwargs.get('leverage', 10)}

        # request path
        request_path_new = request_path + parse_params_to_str(params)
        url = base_url + request_path_new

        # request header and body
        body = json.dumps(params)
        header = get_header(kwargs.get('apiKey'), signature(timestamp, 'POST',
                    request_path_new, body, kwargs.get('secretKey')), timestamp,
                    kwargs.get('Passphrase'))

        # do request
        response = requests.post(url, data=body, headers=header)
        status_code = response.status_code
        result = response.json()
        print(status_code, result)
        result.update(kwargs)
        data_redis(result)
    except Exception as e:
        kwargs.update({'error':str(e), 'content':'futures_order process is error'})
        print('futures_order', e)
    return


def main(type=''):
    try:
        users_data = [setting_data_get()]
        print(users_data)
        for user in users_data:
            user.pop('type', 0)
            if user.get('is_host'):
                futures_order(type=type, **user)
    except Exception as e:
        data_redis({'error':str(e), 'content':'main order process is error'})
        print('main', e)

#检查持仓亏损情况
def check_position(**kwargs):
    timestamp = str(round(time.time(), 3))
    base_url = 'https://www.okex.me'
    request_path = '/api/futures/v3/{}/position'.format(instrument_id)
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                request_path, '', kwargs.get('secretKey')), timestamp,
                kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    loss = kwargs.get('loss', -4)
    profit = kwargs.get('profit', 0)
    loss_fixed = loss if loss < 0 else -4
    if result.get('result') is True:
        print(status_code, result)
        result = result.get('holding', [{}])[0]
        long_qty, short_qty = int(result.get('long_qty', 0)), \
                              int(result.get('short_qty', 0))
        long_pnl_ratio, short_pnl_ratio = float(result.get('long_pnl_ratio', 0))*100, \
                                          float(result.get('short_pnl_ratio', 0))*100
        long_leverage, short_leverage = int(result.get('long_leverage')), \
                                        int(result.get('short_leverage'))
        print('多：', long_qty, long_pnl_ratio, long_leverage)
        print('空：', short_qty, short_pnl_ratio, short_leverage)
        global long_start_ratio, long_ratio, short_start_ratio, short_ratio
        if long_qty > 0:
            if long_pnl_ratio < long_ratio or long_pnl_ratio > profit > 0:
                #平多
                print('平多')
                kwargs['leverage'] = long_leverage
                kwargs['size'] = long_qty
                futures_order(type='3', **kwargs)
            elif long_pnl_ratio > long_start_ratio:
                long_start_ratio += 1
                long_ratio += 1
        else:
            long_ratio = loss_fixed
            long_start_ratio = 1
        if short_qty > 0:
            if short_pnl_ratio < short_ratio or short_pnl_ratio > profit > 0:
                #平空
                print('平空')
                kwargs['leverage'] = short_leverage
                kwargs['size'] = short_qty
                futures_order(type='4', **kwargs)
            elif short_pnl_ratio > short_start_ratio:
                short_start_ratio += 1
                short_ratio += 1
        else:
            short_ratio = loss_fixed
            short_start_ratio = 1
    # result.update(kwargs)
    # data_redis(result)


def futures_price():
    futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                  'symbol=f_usd_eos&type=5min&contractType=quarter&limit=100&coinVol=1'
    data = requests.get(futures_url).json()
    data = data['data']

    return data[-1][-2]


#检查持仓亏损情况(全仓)
def check_position_crossed(**kwargs):
    now_price = float(futures_price())
    #print(now_price)
    timestamp = str(round(time.time(), 3) - 30)
    print(timestamp)
    base_url = 'https://www.okex.me'
    request_path = '/api/futures/v3/{}/position'.format(instrument_id)
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                request_path, '', kwargs.get('secretKey')), timestamp,
                kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    print(result)
    loss = kwargs.get('loss', -4)
    profit = kwargs.get('profit', 0)
    loss_fixed = loss if loss < 0 else -4
    if result.get('result') is True:
        print(status_code, result)
        result = result.get('holding', [{}])[0]
        long_qty, short_qty = int(result.get('long_avail_qty', 0)), \
                              int(result.get('short_avail_qty', 0))
        leverage = int(result.get('leverage'))
        long_avg_cost, short_avg_cost = float(result.get('long_avg_cost', 0)), \
                                        float(result.get('short_avg_cost', 0))
        long_pnl_ratio, short_pnl_ratio = (now_price-long_avg_cost)/now_price*100*leverage, \
                                          (short_avg_cost-now_price)/now_price*100*leverage
        global long_start_ratio, long_ratio, short_start_ratio, short_ratio
        print('现价：', now_price)
        print('多：', long_qty, long_pnl_ratio, leverage, long_ratio)
        print('空：', short_qty, short_pnl_ratio, leverage, short_ratio)
        if long_qty > 0:
            if long_pnl_ratio < long_ratio or long_pnl_ratio > profit > 0 or long_pnl_ratio < loss_fixed:
                #平多
                print('平多')
                kwargs['leverage'] = leverage
                kwargs['size'] = long_qty
                futures_order(type='3', **kwargs)
            elif long_pnl_ratio > long_start_ratio:
                long_start_ratio += 1
                long_ratio += 1
        else:
            long_ratio = loss_fixed
            long_start_ratio = 1
        if short_qty > 0:
            if short_pnl_ratio < short_ratio or short_pnl_ratio > profit > 0 or short_pnl_ratio < loss_fixed:
                #平空
                print('平空')
                kwargs['leverage'] = leverage
                kwargs['size'] = short_qty
                futures_order(type='4', **kwargs)
            elif short_pnl_ratio > short_start_ratio:
                short_start_ratio += 1
                short_ratio += 1
        else:
            short_ratio = loss_fixed
            short_start_ratio = 1
    # result.update(kwargs)
    # data_redis(result)


def main_2():
    while True:
        try:
            users_data = [setting_data_get()]
            print(users_data)
            for user in users_data:
                user.pop('type', 0)
                if user.get('is_host'):
                    check_position_crossed(**user)
            time.sleep(2)
        except Exception as e:
            data_redis({'error':str(e), 'content':'main_2 check position process is error'})
            print('main_2', e)
            time.sleep(2)


def trades_get(**kwargs):
    """
    获取成交数据
    :param kwargs: 
    :return: 
    """
    timestamp = str(round(time.time(), 3) - 30)
    base_url = 'https://www.okex.me'
    request_path = '/api/futures/v3/instruments/{}/trades?limit=50'.format(instrument_id)
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                                                        request_path, '',
                                                        kwargs.get(
                                                            'secretKey')),
                        timestamp,
                        kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    print(result)


def account_get(**kwargs):
    """
    获取现货账户数据
    :param kwargs: 
    :return: 
    """
    timestamp = str(round(time.time(), 3) - 30)
    base_url = 'https://www.okex.me'
    request_path = '/api/spot/v3/accounts'
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                                                        request_path, '',
                                                        kwargs.get(
                                                            'secretKey')),
                        timestamp,
                        kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    print(result)
    for r in result:
        print(r)

def account_ledger_get(**kwargs):
    """
    获取订单列表
    :param kwargs: 
    :return: 
    """
    timestamp = str(round(time.time(), 3) - 30)
    base_url = 'https://www.okex.me'
    #request_path = '/api/spot/v3/orders?instrument_id=OKB-USDT&status=filled'
    request_path = '/api/futures/v3/orders/EOS-USD-190628?status=2'
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                                                        request_path, '',
                                                        kwargs.get(
                                                            'secretKey')),
                        timestamp,
                        kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    print(result)
    for r in result['order_info']:
        print(r)
        # print(r['timestamp'], r['side'], r['filled_notional'], r['filled_size'],
        #       (float(r['filled_notional'])/float(r['filled_size'])))


def instruments_get(**kwargs):
    """
    获取币对信息
    :param kwargs: 
    :return: 
    """
    timestamp = str(round(time.time(), 3) - 30)
    base_url = 'https://www.okex.me'
    request_path = '/api/spot/v3/instruments'
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                                                        request_path, '',
                                                        kwargs.get(
                                                            'secretKey')),
                        timestamp,
                        kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    print(result)
    for r in result:
        if r['base_currency'] in ['BTC', 'EOS', 'OKB', 'BTT', 'BLOC']:
            print(r)


def position_all_get(**kwargs):
    """
    获取持仓信息
    :param kwargs: 
    :return: 
    """
    timestamp = str(round(time.time(), 3) - 30)
    base_url = 'https://www.okex.me'
    request_path = '/api/futures/v3/position'
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                                                        request_path, '',
                                                        kwargs.get(
                                                            'secretKey')),
                        timestamp,
                        kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    print(result)
    for r in result['holding'][0]:

        print(r)


def futures_account_get(**kwargs):
    """
    获取交割合约账户数据
    :param kwargs: 
    :return: 
    """
    timestamp = str(round(time.time(), 3) - 30)
    base_url = 'https://www.okex.me'
    request_path = '/api/futures/v3/accounts'
    # set request header
    header = get_header(kwargs.get('apiKey'), signature(timestamp, 'GET',
                                                        request_path, '',
                                                        kwargs.get(
                                                            'secretKey')),
                        timestamp,
                        kwargs.get('Passphrase'))
    # do request
    response = requests.get(base_url + request_path, headers=header)
    # json
    status_code = response.status_code
    result = response.json()
    print(result)
    for k, v in result['info'].items():
        print(k, v)


if __name__ == '__main__':
    #main(type='3')
    #main_2()
    #setting_data_get()
    #trades_get(**users_data[0])
    #account_get(**users_data[0])
    #account_ledger_get(**users_data[0])
    #instruments_get(**users_data[0])
    #position_all_get(**users_data[0])
    futures_account_get(**users_data[0])
