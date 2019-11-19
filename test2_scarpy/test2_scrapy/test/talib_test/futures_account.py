import hmac
import base64
import requests
import json
import time
import redis
import copy

#用户信息
users_data = [
{'apiKey': '146537f4-7692-4821-ad5a-af03c8cca385',
'secretKey': '9681E893CC577593280A82FB43B3DD43',
'Passphrase':'lly123456', 'id':1},
]


CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'


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


class FuturesAccount(object):

    def __init__(self, **kwargs):
        """
        
        :param kwargs: 
        """
        self.apiKey = kwargs.get('apiKey')
        self.secretKey = kwargs.get('secretKey')
        self.Passphrase = kwargs.get('Passphrase')
        self.id = str(kwargs.get('id'))
        self.base_url = 'https://www.okex.me'
        self.instrument_id_dict = {}
        self.underlying_index_dict = {}
        self.futures_account = {}
        self.futures_ticker = {}
        self.spot_instruments = {}
        self.spot_instrument_id = {}
        self.spot_tick_size = {}
        self.spot_account = {}
        self.spot_ticker = {}
        self.swap_account = {}
        self.swap_ticker = {}

    def data_get(self, request_path=''):
        """
        构造请求数据
        :param request_path: 
        :return: 
        """
        timestamp = str(round(time.time(), 3))
        # set request header
        header = get_header(self.apiKey, signature(timestamp, 'GET', request_path, '',
                            self.secretKey), timestamp, self.Passphrase)
        # do request
        response = requests.get(self.base_url + request_path, headers=header)
        # json
        status_code = response.status_code
        if status_code != 200:
            raise Exception('{} request is error'.format(request_path), response.json())
        result = response.json()

        return result

    def futures_account_get(self, is_one_time=False):
        """
        获取所有币种交割合约账户信息
        限速规则：1次/10s
        :return: 
        """
        if is_one_time:
            request_path = '/api/futures/v3/accounts'
            result = self.data_get(request_path)
            if not result:
                return

            futures_account = result.get('info', {})
            self.futures_account = futures_account
            print(futures_account)
        else:
            #通过单币种接口获取所有
            futures_account = {}
            for currency in self.underlying_index_dict.keys():
                result = self.futures_account_get_one(currency)
                if float(result.get('equity', 0)):
                    futures_account[currency] = result
            self.futures_account = futures_account
            print(futures_account)

        return futures_account

    def futures_account_get_one(self, currency):
        """
        获取单个币种交割合约账户信息
        限速规则：20次/2s
        :param currency: 
        :return: 
        """
        request_path = '/api/futures/v3/accounts/{currency}'
        result = self.data_get(request_path.format(currency=currency))
        if not result:
            return

        return result

    def futures_instruments_get(self):
        """
        获取交割合约信息（交割合约代号）
        限速规则：20次/2s
        :return: 
        """
        request_path = '/api/futures/v3/instruments'
        result = self.data_get(request_path)
        if not result:
            return

        instrument_id_dict = {} #作用：获取代号对应的合约类型
        underlying_index_dict = {} #作用：获取币种所有合约代号
        for r in result:
            instrument_id = r['instrument_id']
            underlying_index = r['underlying_index']
            instrument_id_dict[instrument_id] = r
            if underlying_index in underlying_index_dict:
                underlying_index_dict[underlying_index].append(instrument_id)
            else:
                underlying_index_dict[underlying_index]=[instrument_id]

        self.instrument_id_dict = instrument_id_dict
        self.underlying_index_dict = underlying_index_dict
        print(instrument_id_dict)
        print(underlying_index_dict)

    def futures_orders_get(self):
        """
        获取交割合约订单列表
        限速规则：20次/2s
        {'instrument_id': 'EOS-USD-190628', 'size': '25', 'timestamp': 1555078862.0, 
        'filled_qty': '25', 'fee': '-0.01373878', 'order_id': '2643909861285888', 
        'price': '5.458', 'price_avg': '5.459', 'status': '2', 'type': '3', 
        'contract_val': '10', 'leverage': '10', 'client_oid': 'lvjiantest20190227', 
        'pnl': '0.13461968', 'order_type': '0', 'alias': 'quarter', 'currency': 'EOS', 
        'time_str': '2019-04-12 22:21:02'}
        :return: 
        """
        request_path = '/api/futures/v3/orders/{instrument_id}?status=2&limit=30'

        order_info_all = []
        for currency in self.futures_account.keys():
            for instrument_id in self.underlying_index_dict[currency.upper()]:
                result = self.data_get(request_path.format(
                    instrument_id=instrument_id))
                if not result:
                    continue
                order_info = result.get('order_info', [])
                for o in order_info:
                    o['alias'] = self.instrument_id_dict[instrument_id]['alias']
                    o['currency'] = instrument_id.split('-')[0]
                    t_change = self.timestamp_change(o['timestamp'])
                    o['timestamp'], o['time_str'] = t_change[0], t_change[1]
                order_info_all.extend(order_info)

        order_info_all.sort(key=lambda x: x['timestamp'], reverse=True)
        for o in order_info_all:
            print(o['time_str'], o['currency'], o['alias'], o['filled_qty'],
                  o['price_avg'], o['type'])
        print(order_info_all)

        return order_info_all

    def futures_position_get(self):
        """
        获取交割合约持仓信息
        限速规则：5次/2s
        {'qty': 14, 'avg_cost': 5.687, 'pnl_ratio': 47.52, 'leverage': 10, 
        'currency': 'EOS', 'alias': 'quarter', 'type': 'short', 'short_liqui_price': 0.0}
        :return: 
        """
        request_path = '/api/futures/v3/position'
        result = self.data_get(request_path)
        if not result:
            return

        holding = []
        for p in result['holding'][0]:
            instrument_id = p['instrument_id']
            p['alias'] = self.instrument_id_dict[instrument_id]['alias']
            p['currency'] = instrument_id.split('-')[0]
            round_num = len(self.instrument_id_dict.get(instrument_id, {}).
                            get('tick_size', '-'*5)) - 2

            long_avg_cost, short_avg_cost = float(p.get('long_avg_cost', 0)), \
                                            float(p.get('short_avg_cost', 0))
            long_qty, short_qty = int(p.get('long_qty', 0)), \
                                  int(p.get('short_qty', 0))
            if p['margin_mode'] == 'crossed':
                now_price = self.futures_ticker[instrument_id]
                leverage = int(p.get('leverage'))
                long_leverage = short_leverage = leverage
                long_liqui_price = short_liqui_price = float(p.get('liquidation_price', 0))
                long_pnl_ratio, short_pnl_ratio = (
                                                  now_price - long_avg_cost) / now_price * 100 * leverage, \
                                                  (
                                                  short_avg_cost - now_price) / now_price * 100 * leverage
            else:
                long_qty, short_qty = int(p.get('long_qty', 0)), \
                                      int(p.get('short_qty', 0))
                long_pnl_ratio, short_pnl_ratio = float(p.get('long_pnl_ratio', 0)) * 100, \
                                                  float(p.get('short_pnl_ratio', 0)) * 100
                long_leverage, short_leverage = int(p.get('long_leverage')), \
                                                int(p.get('short_leverage'))
                long_liqui_price = float(p.get('long_liqui_price', 0))
                short_liqui_price = float(p.get('short_liqui_price', 0))
            if long_qty > 0:
                h = {'qty':long_qty, 'avg_cost':round(long_avg_cost, round_num),
                     'pnl_ratio':round(long_pnl_ratio, 2), 'leverage':long_leverage,
                     'currency':p['currency'], 'alias':p['alias'], 'type':'long',
                     'liqui_price':long_liqui_price}
                holding.append(h)
            if short_qty > 0:
                h = {'qty':short_qty, 'avg_cost':round(short_avg_cost, round_num),
                     'pnl_ratio':round(short_pnl_ratio, 2), 'leverage':short_leverage,
                     'currency':p['currency'], 'alias':p['alias'], 'type':'short',
                     'liqui_price': short_liqui_price}
                holding.append(h)
        print(holding)

        return holding

    def futures_account_ledger_get(self):
        """
        获取交割合约账单
        限速规则：5次/2s
        :return: 
        """
        request_path = '/api/futures/v3/accounts/{currency}/ledger?limit=30'
        results = []
        for k, v in self.underlying_index_dict.items():
            result = self.data_get(request_path.format(currency=k.lower()))
            if not result:
                continue

            for r in result:
                if r['type'] == 'transfer':
                    t_change = self.timestamp_change(r['timestamp'])
                    r['timestamp'], r['time_str'] = t_change[0], t_change[1]
                    results.append(r)
            time.sleep(0.5)

        results.sort(key=lambda x: x['timestamp'], reverse=True)
        print(results)

        return results

    def futures_price_get(self, currency, type):
        """
        获取合约价格
        :param currency: 
        :param type: 
        :return: 
        """
        futures_url = 'https://www.okex.me/v2/futures/pc/market/klineData.do?' \
                      'symbol=f_usd_{}&type=5min&contractType={}&limit=100&coinVol=1'
        data = requests.get(futures_url.format(currency.lower(), type)).json()
        data = data['data']

        return data[-1][-2]

    def futures_ticker_get(self):
        """
        获取所有交割合约最新价
        限速规则：20次/2s
        :return: 
        """
        request_path = '/api/futures/v3/instruments/ticker'
        result = self.data_get(request_path)
        if not result:
            return

        futures_ticker = {}
        for r in result:
            futures_ticker[r['instrument_id']] = float(r['last'])

        self.futures_ticker = futures_ticker
        print(futures_ticker)

        return futures_ticker

    def timestamp_change(self, timestamp):
        """
        时间转化
        2019-04-13T08:40:11.000Z
        :param timestamp: 
        :return: 
        """
        t = timestamp.replace('T', ' ')[:-5]
        t_new = time.strptime(t, '%Y-%m-%d %H:%M:%S')
        tt = time.mktime(t_new) + 28800
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tt))

        return tt, time_str

    def spot_account_get(self):
        """
        获取现货账户信息
        限速规则：20次/2s
        :return: 
        """
        self.spot_instruments_get()
        request_path = '/api/spot/v3/accounts'
        result = self.data_get(request_path)
        if not result:
            return

        spot_account = {}
        for r in result:
            currency = r['currency']
            if currency == 'USDT' or float(r['balance']) > float(self.spot_instruments[currency]['min_size']):
                spot_account[currency] = r
                print(currency, r)

        self.spot_account = spot_account

        return spot_account

    def spot_instruments_get(self):
        """
        获取币对信息
        限速规则：20次/2s
        :return: 
        """
        request_path = '/api/spot/v3/instruments'
        result = self.data_get(request_path)
        if not result:
            return

        spot_instruments = {}  #作用：隐藏小额币种
        spot_instrument_id = {}  #作用：获取币种交易对
        spot_tick_size = {}  #作用：获取交易对价格精度
        for r in result:
            base_currency = r['base_currency']
            quote_currency = r['quote_currency']
            instrument_id = r['instrument_id']
            if base_currency in spot_instrument_id:
                spot_instrument_id[base_currency].append(instrument_id)
            else:
                spot_instrument_id[base_currency] = [instrument_id]

            if quote_currency == 'USDT':
                spot_instruments[base_currency] = r

            spot_tick_size[instrument_id] = len(r['tick_size']) - 2
        self.spot_instruments = spot_instruments
        self.spot_instrument_id =spot_instrument_id
        self.spot_tick_size = spot_tick_size
        print(spot_instruments)
        print(spot_instrument_id)
        print(spot_tick_size)

    def spot_orders_get(self):
        """
        获取现货订单列表
        限速规则：20次/2s
        {'client_oid': '', 'created_at': '2019-01-05T23:39:27.000Z', 
        'filled_notional': '5.26', 'filled_size': '2', 'funds': '', 
        'instrument_id': 'EOS-USDT', 'notional': '', 'order_id': '2096861483776000', 
        'order_type': '0', 'price': 2.63, 'product_id': 'EOS-USDT', 'side': 'buy', 
        'size': '2', 'status': 'filled', 'timestamp': 1546731567.0, 'type': 'limit', 
        'time_str': '2019-01-06 07:39:27'}
        :return: 
        """
        request_path = '/api/spot/v3/orders?instrument_id={}&status=filled&limit=30'
        order_info_all = []
        for currency in self.spot_account.keys():
            for instrument_id in self.spot_instrument_id.get(currency, []):
                tick_size = self.spot_tick_size.get(instrument_id, 5)
                result = self.data_get(request_path.format(instrument_id))
                for r in result:
                    t_change = self.timestamp_change(r['timestamp'])
                    r['timestamp'], r['time_str'] = t_change[0], t_change[1]
                    r['price'] = round(float(r['filled_notional'])/float(r['filled_size']),
                                       tick_size)
                order_info_all.extend(result)

        order_info_all.sort(key=lambda x: x['timestamp'], reverse=True)
        for o in order_info_all:
            print(o['time_str'], o['instrument_id'], o['side'], o['filled_size'], o['price'])

        return order_info_all

    def spot_ticker_get(self):
        """
        获取所有现货价格
        限速规则：50次/2s
        :return: 
        """
        request_path = '/api/spot/v3/instruments/ticker'
        result = self.data_get(request_path)
        if not result:
            return

        spot_ticker = {}
        for r in result:
            instrument_id = r['instrument_id'].split('-')
            if instrument_id[-1] == 'USDT':
                spot_ticker[instrument_id[0]] = float(r['last'])
        print(spot_ticker)

        self.spot_ticker = spot_ticker

        return spot_ticker

    def spot_account_ledger_get(self):
        """
        获取现货账单
        限速规则：20次/2s
        :return: 
        """
        request_path = '/api/spot/v3/accounts/{currency}/ledger?limit=30'
        results = []
        for k, v in self.spot_account.items():
            result = self.data_get(request_path.format(currency=k))
            if not result:
                continue

            for r in result:
                if r['type'] == 'transfer':
                    t_change = self.timestamp_change(r['timestamp'])
                    r['timestamp'], r['time_str'] = t_change[0], t_change[1]
                    results.append(r)

        results.sort(key=lambda x: x['timestamp'], reverse=True)
        print(results)

        return results

    def swap_account_get(self, is_one_time=False):
        """
        获取永续合约账户信息
        限速规则：1次/10s
        :return: 
        """
        if is_one_time:
            request_path = '/api/swap/v3/accounts'
            result = self.data_get(request_path)
            if not result:
                return

            swap_account = {}
            for r in result['info']:
                swap_account[r['instrument_id'].split('-')[0]] = r
            self.swap_account = swap_account
            print(swap_account)
        else:
            swap_account = {}
            for instrument_id in self.swap_ticker.keys():
                result = self.swap_account_get_one(instrument_id=instrument_id)
                r = result['info']
                if float(r.get('equity', 0)):
                    swap_account[r['instrument_id'].split('-')[0]] = r
            self.swap_account = swap_account
            print(swap_account)

        return swap_account

    def swap_account_get_one(self, instrument_id):
        """
        获取单个币种永续合约账户信息
        限速规则：20次/2s
        :param currency: 
        :return: 
        """
        request_path = '/api/swap/v3/{instrument_id}/accounts'
        result = self.data_get(request_path.format(instrument_id=instrument_id))
        if not result:
            return

        return result

    def swap_position_get(self, is_one_time=False):
        """
        获取永续合约持仓信息
        限速规则：1次/10s
        :return: 
        """
        holding = []
        def position_make(p):
            instrument_id = p['instrument_id']
            currency = instrument_id.split('-')[0]
            avg_cost = float(p['avg_cost'])
            leverage = float(p['leverage'])
            side = p['side']
            now_price = self.swap_ticker[instrument_id]
            if side == 'long':
                pnl_ratio = (now_price - avg_cost) / now_price * 100 * leverage
            else:
                pnl_ratio = (avg_cost - now_price) / now_price * 100 * leverage
            h = {'qty': p['position'], 'avg_cost': avg_cost,
                 'pnl_ratio': round(pnl_ratio, 2),
                 'leverage': leverage, 'currency': currency, 'alias': 'swap',
                 'type': side, 'liqui_price': p['liquidation_price']}
            holding.append(h)

        if is_one_time:
            request_path = '/api/swap/v3/position'
            result = self.data_get(request_path)
            for r in result:
                for p in r['holding']:
                    position_make(p)
        else:
            for instrument_id in self.swap_ticker.keys():
                result = self.swap_position_get_one(instrument_id=instrument_id)
                for p in result.get('holding', []):
                    if float(p.get('position', 0)):
                        position_make(p)
        print(holding)

        return holding

    def swap_position_get_one(self, instrument_id):
        """
        获取永续单个合约持仓信息
        :param instrument_id: 
        :return: 
        """
        request_path = '/api/swap/v3/{instrument_id}/position'
        result = self.data_get(request_path.format(instrument_id=instrument_id))
        if not result:
            return {}

        return result

    def swap_ticker_get(self):
        """
        获取永续合约最新价
        限速规则：20次/2s
        :return: 
        """
        request_path = '/api/swap/v3/instruments/ticker'
        result = self.data_get(request_path)
        if not result:
            return

        swap_ticker = {}
        for r in result:
            swap_ticker[r['instrument_id']] = float(r['last'])

        self.swap_ticker = swap_ticker
        print(swap_ticker)

        return swap_ticker

    def swap_orders_get(self):
        """
        获取永续订单列表
        限速规则：20次/2s
        {'client_oid': '', 'contract_val': '10', 'fee': '-0.001863', 
        'filled_qty': '5', 'instrument_id': 'EOS-USD-SWAP', 
        'order_id': '6a-7-5bf1be2b8-0', 'order_type': '0', 'price': '5.370', 
        'price_avg': '5.370', 'size': '5', 'status': '2', 'timestamp': 1555401112.0, 
        'type': '4', 'alias': 'swap', 'currency': 'EOS', 'time_str': '2019-04-16 15:51:52'}
        :return: 
        """
        request_path = '/api/swap/v3/orders/{instrument_id}?status=2&limit=30'

        order_info_all = []
        for k, v in self.swap_account.items():
            instrument_id = v['instrument_id']
            result = self.data_get(request_path.format(
                instrument_id=instrument_id))
            if not result:
                continue
            order_info = result.get('order_info', [])
            for o in order_info:
                o['alias'] = 'swap'
                o['currency'] = instrument_id.split('-')[0]
                t_change = self.timestamp_change(o['timestamp'])
                o['timestamp'], o['time_str'] = t_change[0], t_change[1]
            order_info_all.extend(order_info)

        order_info_all.sort(key=lambda x: x['timestamp'], reverse=True)

        for o in order_info_all:
            print(o['time_str'], o['currency'], o['alias'], o['filled_qty'],
                  o['price_avg'], o['type'])
        print(order_info_all)

        return order_info_all

    def swap_account_ledger_get(self):
        """
        获取永续合约账单
        限速规则：5次/2s
        :return: 
        """
        request_path = '/api/swap/v3/accounts/{instrument_id}/ledger?limit=30'
        results = []
        for k, v in self.swap_account.items():
            instrument_id = v['instrument_id']
            result = self.data_get(request_path.format(
                instrument_id=instrument_id))
            if not result:
                continue

            for r in result:
                if r['type'] == 'transfer':
                    t_change = self.timestamp_change(r['timestamp'])
                    r['timestamp'], r['time_str'] = t_change[0], t_change[1]
                    results.append(r)
            time.sleep(0.5)

        results.sort(key=lambda x: x['timestamp'], reverse=True)
        print(results)

        return results


def redis_connection():
    """
    连接redis
    :return: 
    """
    pool = redis.ConnectionPool(host='localhost', port=6379, db=9, password='lvjian')
    r = redis.Redis(connection_pool=pool)

    return r


def data_redis(data):
    """
    报错记录
    :param data: 
    :return: 
    """
    r = redis_connection()
    time_now = time.strftime('%Y-%m-%d %X', time.localtime())
    data['updated_at'] = time_now
    # data.pop('apiKey', 0)
    # data.pop('secretKey', 0)
    # data.pop('Passphrase', 0)
    data = json.dumps(data)
    r.lpush('error_history', data)


def profit_count(profit_list, num):
    """
    计算累计收益
    :param profit_list: 
    :param num: 
    :return: 
    """
    if num == -1:
        num = 'all'
    else:
        profit_list = profit_list[0:num]
    profit, profit_percent = 0, 1
    for p in profit_list:
        profit += p['profit']
        profit_percent *= (1 + p['profit_percent']/100)
    profit_percent -= 1
    profit_percent = round(profit_percent*100, 2)
    profit = round(profit, 2)
    result = {'profit_'+str(num):profit, 'profit_percent_'+str(num):profit_percent}

    return result


def main_futures(user_data):
    """
    主函数(期货)
    :param user_data: 
    :return: 
    """
    r = redis_connection()       #连接redis
    timestamp = time.time()
    time_now = time.strftime('%Y-%m-%d %X', time.localtime())
    f = FuturesAccount(**user_data)
    f.spot_ticker_get()          #现货价格
    f.futures_ticker_get()       #交割合约价格
    f.swap_ticker_get()          #永续合约价格
    f.futures_instruments_get()  #交割合约代号
    f.futures_account_get()      #交割合约账户信息
    f.swap_account_get()         #永续合约账户信息
    #整合合约币种、数目、价值
    futures_assets = {}          #交割合约币种、数目、价值
    swap_assets = {}             #永续合约币种、数目、价值
    for currency, d in f.futures_account.items():
        equity = float(d['equity'])
        futures_assets[currency] = {'equity':equity,
                                    'value':f.spot_ticker.get(currency, 0)*equity}
    for currency, d in f.swap_account.items():
        equity = float(d['equity'])
        swap_assets[currency] = {'equity':equity, 'instrument_id':d['instrument_id'],
                                    'value':f.spot_ticker.get(currency, 0)*equity}

    futures_currencies_old = r.hget('account', 'futures_currencies_'+f.id)
    futures_currencies_old = json.loads(
        futures_currencies_old.decode()) if futures_currencies_old else {}
    f.futures_account.update(futures_currencies_old)
    swap_currencies_old = r.hget('account', 'swap_currencies_' + f.id)
    swap_currencies_old = json.loads(
        swap_currencies_old.decode()) if swap_currencies_old else {}
    f.swap_account.update(swap_currencies_old)
    #合约总资产数目
    f_s_assets = {}
    f_s_assets.update(copy.deepcopy(futures_assets))
    for k, v in swap_assets.items():
        if k in f_s_assets:
            f_s_assets[k]['equity'] += v['equity']
            f_s_assets[k]['value'] += v['value']
        else:
            f_s_assets[k] = v
    assets_all = round(sum([v['value'] for v in f_s_assets.values()]), 2)
    #合约总资产配比
    match = []
    for k, v in f_s_assets.items():
        v['currency'] = k
        v['percent'] = round(v['value']/assets_all*100, 2)
        match.append(v)
    match.sort(key=lambda x: x['percent'], reverse=True)
    #当日合约总资产信息
    account_redis = r.hget('account', 'futures_account_'+f.id)
    account_redis = json.loads(account_redis.decode()) if account_redis else {}
    #前一日合约总资产信息
    futures_profit = r.lindex('futures_profit_list_' + f.id, 0)
    futures_profit = json.loads(futures_profit.decode()) if futures_profit else {}
    #初始化合约总资产信息
    futures_account = {'assets':assets_all, 'profit':0, 'profit_percent':0,
                       'out':0, 'in':0, 'change':0, 'match':match,
                       'updated_at':time_now, 'timestamp':timestamp
                       }
    #合约总流水账单
    futures_transfer = []
    ledger_ids = []
    futures_transfer.extend(f.futures_account_ledger_get())
    futures_transfer.extend(f.swap_account_ledger_get())
    for t in futures_transfer:
        if futures_profit and account_redis and \
            t['timestamp'] > futures_profit['timestamp'] \
            and not r.sismember('futures_ledger_set_'+f.id, t['ledger_id']):
            amount = float(t['amount'])
            ledger_id = t['ledger_id']
            currency = t['currency'] if t.get('currency') else \
                t['instrument_id'].split('-')[0]
            price = f.spot_ticker.get(currency, 0)
            if amount > 0:
                account_redis['in'] += amount * price
            else:
                account_redis['out'] += amount * price
            ledger_ids.append(ledger_id)
    if account_redis and futures_profit:
        account_redis['timestamp'] = timestamp
        account_redis['updated_at'] = time_now
        account_redis['change'] = account_redis['out'] + account_redis['in']
        account_redis['match'] = match
        account_redis['assets'] = assets_all
        profit = assets_all - futures_profit['assets'] - account_redis['change']
        profit_percent = profit/(futures_profit['assets']+account_redis['in'])*100
        account_redis['profit'] = round(profit, 2)
        account_redis['profit_percent'] = round(profit_percent, 2)
    else:
        account_redis = futures_account
    if not futures_profit or account_redis['updated_at'].split(' ')[0] != \
        futures_profit['updated_at'].split(' ')[0]:
        r.lpush('futures_profit_list_'+f.id, json.dumps(account_redis))
        account_redis = futures_account
    if ledger_ids:
        r.sadd('futures_ledger_set_'+f.id, *ledger_ids)
    # 计算合约账户累计收益
    futures_profit_redis = r.lrange('futures_profit_list_' + f.id, 0, -1)
    futures_profit_redis = [json.loads(d.decode()) for d in
                            futures_profit_redis]
    futures_profit_redis.pop(-1)
    futures_profit_redis = [account_redis] + futures_profit_redis
    print(len(futures_profit_redis), futures_profit_redis)
    for num in [7, 30, -1]:
        result = profit_count(futures_profit_redis, num)
        account_redis.update(result)
    #记录合约账户信息
    r.hset('account', 'futures_currencies_'+f.id, json.dumps(futures_assets))
    r.hset('account', 'swap_currencies_' + f.id, json.dumps(swap_assets))
    r.hset('account', 'futures_account_'+f.id, json.dumps(account_redis))
    print('当前合约账户信息：', account_redis)

    #记录合约持仓信息
    position_all = f.futures_position_get() + f.swap_position_get()
    position_all = {'holding':position_all}
    r.hset('account', 'futures_position_'+f.id, json.dumps(position_all))
    print('当前合约账户所有持仓信息：', position_all)

    #合约交易记录
    futures_orders = f.futures_orders_get() + f.swap_orders_get()
    futures_orders.sort(key=lambda x: x['timestamp'], reverse=True)
    for o in futures_orders[::-1]:
        order_id = o['order_id']
        if not r.sismember('futures_order_set_'+f.id, order_id):
            r.lpush('futures_order_list_'+f.id, json.dumps(o))
            r.sadd('futures_order_set_'+f.id, order_id)
    print('当前合约账户交易记录：', futures_orders)


    print('#'*30)


def main_2(user_data):
    """
    主函数(现货)
    :param user_data: 
    :return: 
    """
    r = redis_connection()    # 连接redis
    timestamp = time.time()
    time_now = time.strftime('%Y-%m-%d %X', time.localtime())
    f = FuturesAccount(**user_data)
    f.spot_ticker_get()        # 现货价格
    f.spot_account_get()       # 现货账户信息
    spot_assets = {}           # 现货币种、数目、价值
    for currency, d in f.spot_account.items():
        equity = float(d['balance'])
        spot_assets[currency] = {'equity': equity,
                                    'value': f.spot_ticker.get(currency.upper(),
                                                               0) * equity}
        if currency == 'USDT':
            spot_assets[currency]['value'] = equity
    print(spot_assets)
    spot_currencies_old = r.hget('account', 'spot_currencies_' + f.id)
    spot_currencies_old = json.loads(
        spot_currencies_old.decode()) if spot_currencies_old else {}
    f.spot_account.update(spot_currencies_old)
    print(f.spot_account)



if __name__ == '__main__':
    f = FuturesAccount(**users_data[0])
    # f.futures_instruments_get() #基础
    # f.futures_ticker_get()      #基础
    # f.futures_account_get()     #基础
    # f.futures_account_get_one('eos')
    # f.futures_orders_get()
    # f.futures_position_get()
    # f.futures_account_ledger_get()
    # f.spot_instruments_get() #基础
    # f.spot_account_get()     #基础
    # f.spot_orders_get()
    # f.spot_ticker_get()
    # f.spot_account_ledger_get()
    # f.swap_ticker_get()   #基础
    # f.swap_account_get()  #基础
    # f.swap_account_get_one('EOS-USD-SWAP')
    # f.swap_position_get()
    # f.swap_position_get_one('EOS-USD-SWAP')
    # f.swap_orders_get()
    # f.swap_account_ledger_get()
    while True:
        try:
            main_futures(users_data[0])
            time.sleep(15)
        except Exception as e:
            print('!'*20, e, type(e))
            error = {}
            error.update(users_data[0])
            error['error'] = str(e)
            data_redis(error)
            time.sleep(15)
    # main_2(users_data[0])
    pass
