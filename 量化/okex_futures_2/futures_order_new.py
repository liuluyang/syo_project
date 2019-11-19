import hmac
import base64
import requests
import json
import time
import redis

users_data = [
{'apiKey': 'ee7e9331-f2c6-45e2-b13b-340150d7c685',
'secretKey': '1072BFFCF279957C707D06943B9F8EC3',
'Passphrase':'G498807gsl',
'name':'lvjian',
'leverage':10,
'size':10,
'is_host':1},
]

profit = 5
pnl_ratio = -10
instrument_id = "EOS-USD-190329"
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
    r.lpush('order_history_2', data)


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


#1:开多 2:开空 3:平多 4:平空
#开仓平仓
def futures_order(**kwargs):
    try:
        timestamp = str(round(time.time(), 3))
        base_url = 'https://www.okex.me'
        request_path = '/api/futures/v3/order'
        params = {"client_oid": "lvjiantest20190227","instrument_id":instrument_id,
                  "type":kwargs.get('type'),"price":"","size":kwargs.get('size', 1),"match_price":"1",
                  "leverage":kwargs.get('leverage', 20)}

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
        for user in users_data:
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
    #print(status_code, result)
    if result.get('result') is True:
        print(status_code, result)
        result = result.get('holding', [{}])[0]
        long_qty, short_qty = int(result.get('long_qty', 0)), \
                              int(result.get('short_qty', 0))
        long_pnl_ratio, short_pnl_ratio = float(result.get('long_pnl_ratio', 0)), \
                                          float(result.get('short_pnl_ratio', 0))
        long_leverage, short_leverage = int(result.get('long_leverage')), \
                                        int(result.get('short_leverage'))
        print('多：', long_qty, long_pnl_ratio, long_leverage)
        print('空：', short_qty, short_pnl_ratio, short_leverage)
        if long_qty > 0 and (long_pnl_ratio*100 < pnl_ratio or long_pnl_ratio*100 > profit):
            #平多
            print('平多')
            kwargs['leverage'] = long_leverage
            kwargs['size'] = long_qty
            futures_order(type='3', **kwargs)
        if short_qty > 0 and (short_pnl_ratio*100 < pnl_ratio or short_pnl_ratio*100 > profit):
            #平空
            print('平空')
            kwargs['leverage'] = short_leverage
            kwargs['size'] = short_qty
            futures_order(type='4', **kwargs)
    # result.update(kwargs)
    # data_redis(result)


def main_2():
    while True:
        try:
            for user in users_data:
                if user.get('is_host'):
                    check_position(**user)
            time.sleep(3)
        except Exception as e:
            data_redis({'error':str(e), 'content':'main_2 check position process is error'})
            print('main_2', e)
            time.sleep(3)


if __name__ == '__main__':
    #main(type='2')
    main_2()
