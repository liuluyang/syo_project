
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
import time
import redis
import json
import uuid
import uwsgi
from websocket import create_connection
from mysite.settings import REDIS_PASSWORD, MYSQL_REMOTE
import pymysql
from binance.client import Client
from mysite.settings import api_key, api_secret
import requests
import random
import base64, gzip
#ticker new
pool_3 = redis.ConnectionPool(host='localhost', port=6379, db=3, password=REDIS_PASSWORD)
redis_3 = redis.Redis(connection_pool=pool_3)

client_dict = {}
mysql_dict = {}

def bigone_time_change(time_now, is_str=False):
    """
    bigone0时区时间转化为8时区
    :param time_now: 
    :param is_str: 
    :return: timestamp or time_str
    """
    time_utc0 = time_now[:-1]
    time_utc0 = time_utc0.replace('T', ' ')
    time_struct = time.strptime(time_utc0, '%Y-%m-%d %X')
    timestamp = time.mktime(time_struct) + 28800
    if is_str:
        time_new = time.strftime('%Y-%m-%d %X', time.localtime(timestamp))
        return time_new

    return timestamp

def okex_kline_get(symbol, type, size=100):
    """
    symbol:ltc_usdt
    type:1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
    size:default and max 2000
    :return: 
    """
    url = 'https://www.okex.com/api/v1/kline.do?symbol={symbol}&type={type}&size={size}'
    url = url.format(symbol=symbol, type=type, size=size)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    return data

def huobi_kline_get(symbol, period, size=100):
    """
    symbol:btcusdt
    type:1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year
    size:default and max 2000
    :return: 
    """
    url = 'https://api.huobi.pro/market/history/kline?symbol={symbol}&period={period}&size={size}'
    url = url.format(symbol=symbol, period=period, size=size)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    return data

def okex_trade_get(symbol, since=0):
    """
    symbol:ltc_usdt
    since:
    :return: max 60条
    """
    url = 'https://www.okex.com/api/v1/trades.do?symbol={symbol}&since={since}'
    url = url.format(symbol=symbol, since=since)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    return data

def huobi_trade_get(symbol, size=200):
    """
    symbol:btcusdt
    size:default and max 2000
    :return: 
    """
    url = 'https://api.huobi.pro/market/history/trade?symbol={symbol}&size={size}'
    url = url.format(symbol=symbol, size=size)
    data = requests.get(url, headers={
        'content-type': 'application/x-www-form-urlencoded'}).json()
    return data

class Date(object):

    def __init__(self, request_uuid):
        self.uuid = request_uuid
        self.market_default = ['gateio','binance']
        self.error_data = {'error':'参数错误','data':None}
        self.success_data = {'error':None,'data':'sucess'}

    def make_data(self, message):
        message = message.decode()
        try:
            message = json.loads(message)
        except:
            return self.__error('type of parameter is error')
        id = message.get('id', None)
        market = message.get('market', None)
        method = message.get('method', None)
        symbol = message.get('symbol', None)
        params = message.get('params', None)
        if method=='ticker':
            data = None
            if isinstance(symbol, str):
                data = self.ticker_data_one(symbol, market)
            elif isinstance(symbol, list):
                data = self.ticker_data_list(symbol, market)
            if data:
                return self.__success(data)
            return self.__error('symbol is error')
        elif method=='kline':
            data = self.__data_kline(market, symbol, params)
            if data:
                return self.__success(data)
            return self.__error('request %s is error'%(market))
        elif method=='uce_ranking':
            data = self.__data_market_val(market, symbol, params)
            if data:
                return self.__success(data)
            return self.__error('request %s mysql data is error' % (market))
        elif method=='trade':
            data = self.__data_trade(market, symbol, params)
            if data is not None:
                return self.__success(data)
            return self.__error('request %s trade is error'%(market))

        return self.__error('market or method is error')

    def __error(self, error):
        self.error_data['error'] = error

        return self.error_data

    def __success(self, data):
        self.success_data['data'] = data

        return self.success_data

    def __data_kline(self, market, symbol, params):
        data = None
        if market=='gateio':
            data = self.kline_gateio(market, symbol, params)
        elif market=='binance':
            data = self.kline_binance(market, symbol, params)
        elif market=='okex':
            data = self.kline_okex(market, symbol, params)
        elif market=='huobi':
            data = self.kline_huobi(market, symbol, params)
        elif market=='bigone':
            data = self.kline_bigone(market, symbol, params)
        elif market=='bibox':
            data = self.kline_bibox(market, symbol, params)
        elif market=='zb':
            data = self.kline_zb(market, symbol, params)

        return data

    def kline_gateio(self, market, symbol, params):
        ws = client_dict.get(self.uuid, None)
        if not ws:
            try:
                # wss://webws.gateio.io/v3/
                # wss://ws.gateio.io/v3/
                ws = create_connection('wss://webws.gateio.io/v3/', timeout=2)
            except:
                return False
            client_dict[self.uuid] = ws

        period = params.get('period', None)
        item_num = params.get('num', 100)
        data_send_f = {"id": 123, "method": "kline.query",
                       "params": ["BTC_USDT", 1, 1516951219, 1800]}
        period_set = {60, 300, 900, 1800, 3600, 3600 * 24, 3600 * 24 * 7}
        timestamp = int(time.time())
        if period in period_set:
            try:
                params = [symbol, timestamp - period * item_num, timestamp,
                          period]
                data_send_f['params'] = params
                data_send = json.dumps(data_send_f)
                ws.send(data_send)
                data_recv = ws.recv()
                data_recv = json.loads(data_recv)
                result = data_recv['result']
                result = self.kline_data_change(result, market)
                return result
            except:
                client_dict.pop(self.uuid, None)
                return False
        else:
            return False

    def kline_binance(self, market, symbol, params):
        client = client_dict.get(self.uuid, None)
        if not client:
            try:
                client = Client(api_key, api_secret)
            except:
                return False
            client_dict[self.uuid] = client

        period = params.get('period', None)
        item_num = params.get('num', 100)
        #BCH->BCC 2018/8/29
        symbol = symbol.replace('BCH_', 'BCC_')
        symbol_new = symbol.replace('_', '')
        timestamp = int(time.time())
        change_period_dict = {60: '1m', 300: '5m', 900:'15m', 1800: '30m', 3600: '1h',
                              3600 * 24: '1d', 3600 * 24 * 7: '1w'}
        period_binance = change_period_dict.get(period, None)
        if period_binance:
            try:
                result = client.get_historical_klines(symbol_new, period_binance,
                                                (timestamp - item_num * period) * 1000,
                                                    timestamp * 1000)
                result = self.kline_data_change(result, market)
                return result
            except:
                client_dict.pop(self.uuid, None)
                return False
        else:
            return False

    def kline_okex(self, market, symbol, params):
        period = params.get('period', None)
        item_num = params.get('num', 100)
        symbol_new = symbol.lower()
        change_period_dict = {60: '1min', 300: '5min', 900:'15min', 1800: '30min',
                              3600: '1hour',3600 * 24: '1day', 3600 * 24 * 7: '1week'}
        period_okex = change_period_dict.get(period, None)
        if period_okex:
            try:
                result = okex_kline_get(symbol_new, period_okex, item_num)
                result = self.kline_data_change(result, market)
                return result
            except:
                return False
        else:
            return False

    def kline_huobi(self, market, symbol, params):
        period = params.get('period', None)
        item_num = params.get('num', 100)
        symbol_new = symbol.lower().replace('_', '')
        change_period_dict = {60: '1min', 300: '5min', 900:'15min', 1800: '30min',
                              3600: '60min',3600 * 24: '1day', 3600 * 24 * 7: '1week'}
        period_okex = change_period_dict.get(period, None)
        if period_okex:
            try:
                result = huobi_kline_get(symbol_new, period_okex, item_num)
                if result.get('status', None) == 'ok':
                    result = result['data']
                    result = self.kline_data_change(result, market)
                    return result
            except:
                return False
        else:
            return False

    def kline_bigone(self, market, symbol, params):
        #ws = client_dict.get(self.uuid, None)
        ws = None
        if not ws:
            try:
                ws = create_connection('wss://big.one/ws/v2',
                            header={'sec-websocket-protocol': 'json'},
                            subprotocols=['json'])
            except:
                return False
            client_dict[self.uuid] = ws

        period = params.get('period', None)
        item_num = params.get('num', 100)
        data_send_f = {"requestId": str(time.time()).replace('.',''),
                       "subscribeMarketCandlesRequest":
                       {"market":"BTC-USDT", "period": "MIN1"}}
        period_dict = {60:'MIN1', 300:'MIN5', 900:'MIN15', 1800:'MIN30',
                       3600:'HOUR1', 3600*24:'DAY1', 3600*24*7:'WEEK1'}
        period = period_dict.get(period)
        if period:
            try:
                data_send_f["subscribeMarketCandlesRequest"] = \
                    {"market":symbol.replace('_', '-'), "period": period}
                data_send = json.dumps(data_send_f)
                ws.send(data_send)
                data_recv = ws.recv()
                ws.close()
                data_recv = json.loads(data_recv.decode())
                result = data_recv.get('candlesSnapshot', {}).get('candles')
                if result:
                    result = self.kline_data_change(result[:item_num], market)
                    return result
                else:
                    return False
            except:
                client_dict.pop(self.uuid, None)
                return False
        else:
            return False

    def kline_bibox(self, market, symbol, params):
        #ws = client_dict.get(self.uuid, None)
        ws = None
        if not ws:
            try:
                ws = create_connection('wss://push.bibox.com/')
            except:
                return False
            client_dict[self.uuid] = ws

        period = params.get('period', None)
        item_num = params.get('num', 100)
        period_dict = {60: '1min', 300: '5min', 900: '15min', 1800: '30min',
                       3600: '1hour', 3600 * 24: 'day', 3600 * 24 * 7: 'week'}
        period = period_dict.get(period)
        data_send = {
            "event": "addChannel",
            "channel": "bibox_sub_spot_{}_kline_{}".format(symbol, period)
        }
        data_send = json.dumps(data_send)
        data_remove = {
            "event": "removeChannel",
            "channel": "bibox_sub_spot_{}_kline_{}".format(symbol, period)
        }
        data_remove = json.dumps(data_remove)
        if period:
            try:
                ws.send(data_send)
                data_recv = ws.recv()
                ws.close()
                data_recv = json.loads(data_recv)[0]
                data_type = data_recv.get('data_type')
                if data_type == 0:
                    data = data_recv['data']
                    result = self.bibox_inflate(data)
                    result = result[-item_num:]
                    result = self.kline_data_change(result, market)
                else:
                    return False
                #ws.send(data_remove)
                return result
            except:
                client_dict.pop(self.uuid, None)
                return False
        else:
            return False

    def kline_zb(self, market, symbol, params):
        time.sleep(random.random()+0.5)
        symbol_change = {'bchusdt': 'bccusdt', 'bchbtc': 'bccbtc',
                              'bchzb': 'bcczb', 'bchpax': 'bccpax',
                              'hcusdt': 'hsrusdt', 'hcbtc': 'hsrbtc',
                              'hczb': 'hsrzb','hcqc':'hsrqc','bchqc':'bccqc'}
        symbol = ''.join(symbol.split('_')).lower()
        symbol_new = symbol_change.get(symbol)
        #ws = client_dict.get(self.uuid, None)
        ws = None
        if not ws:
            try:
                ws = create_connection('wss://kline.zb.cn/websocket')
            except:
                return False
            client_dict[self.uuid] = ws

        period = params.get('period', None)
        item_num = params.get('num', 100)
        period_dict = {60: '1min', 300: '5min', 900: '15min', 1800: '30min',
                       3600: '1hour', 3600 * 24: '1day', 3600 * 24 * 7: '1week'}
        period = period_dict.get(period)
        data_send = {
            'event':'addChannel',
            'channel': '{}_kline_{}'.format(
                symbol if not symbol_new else symbol_new, period)
        }
        data_send = json.dumps(data_send)
        if period:
            try:
                ws.send(data_send)
                data_recv = ws.recv()
                ws.close()
                data_recv = json.loads(data_recv)
                result = data_recv.get('datas', {}).get('data')
                if result:
                    result = result[-item_num:]
                    result = self.kline_data_change(result, market)
                else:
                    return False
                return result
            except:
                client_dict.pop(self.uuid, None)
                return False
        else:
            return False

    def bibox_inflate(self, data):
        """
        bibox解压数据
        :param data: 
        :return: 
        """
        data = base64.b64decode(data)
        data = gzip.decompress(data)
        data = json.loads(data.decode())

        return data

    def __data_market_val(self, market, symbol, params):
        con_remote = mysql_dict.get(self.uuid, None)
        if not con_remote:
            con_remote = pymysql.connect(**MYSQL_REMOTE,
                                         cursorclass=pymysql.cursors.DictCursor)
            mysql_dict[self.uuid] = con_remote
        if isinstance(symbol, str):
            sql = 'select * from uce_ranking where symbol="%s"'%(symbol)
            cur_remote = con_remote.cursor()
            cur_remote.execute(sql)
            data = cur_remote.fetchone()
            con_remote.commit()
            if data:
                data['updated_at'] = str(data['updated_at'])
                return data
            else:
                return False
        elif isinstance(symbol, list):
            sql = 'select * from uce_ranking where symbol in (%s)' % ','.join(['%s'] * len(symbol))
            cur_remote = con_remote.cursor()
            cur_remote.execute(sql, symbol)
            data = cur_remote.fetchall()
            con_remote.commit()
            data_new = {}
            if data:
                for d in data:
                    d['updated_at'] = str(d['updated_at'])
                    data_new[d['symbol']] = d
                return data_new
            else:
                return False

        return False

    def kline_data_change(self, result, market):
        #time close high low open volume
        new_result = []
        if market=='gateio':
            for r in result:
                new_result.append([r[0] * 1000, r[2], r[3],r[4], r[1],r[5]])
        elif market=='binance':
            for r in result:
                new_result.append([r[0], r[4], r[2], r[3], r[1], r[5]])
        elif market=='okex':
            for r in result:
                new_result.append([r[0], r[4], r[2], r[3], r[1], r[5]])
        elif market=='huobi':
            for r in result[::-1]:
                new_result.append([r['id']*1000, r['close'], r['high'], r['low'],
                                   r['open'], r['amount']])
        elif market=='bigone':
            for r in result[::-1]:
                new_result.append([bigone_time_change(r['time'])*1000, r['close'],
                                   r['high'], r['low'], r['open'], 0])
        elif market=='bibox':
            for r in result:
                new_result.append([r['time'], r['close'],r['high'], r['low'],
                                   r['open'], r['vol']])
        elif market=='zb':
            for r in result:
                new_result.append([r[0], r[-2],r[2], r[3], r[1], r[-1]])

        return new_result

    def ticker_data_one(self, symbol, market):
        hash_key = market+'_ticker_new'
        data = redis_3.hget(hash_key, symbol)
        if data:
            # redis数据库取出的数据是bytes，需要转换
            data = json.loads(data.decode())
            # 添加返回数据(app need)
            data['sym_cur'] = symbol
            data['market'] = market.capitalize()
            data['p_change'] = data['change']
            data['quote_vol'] = data['quoteVolume']
            return data
        return False

    def ticker_data_list(self, symbol, market):
        data = {}
        for s in symbol:
            array = s.split('/')
            hash_key = array[1].lower() + '_ticker_new'
            data_s =  redis_3.hget(hash_key, array[0])
            if data_s:
                data[s] = json.loads(data_s.decode())
        return data if data else False

    def __data_trade(self, market, symbol, params):
        data = None
        if market=='gateio':
            data = self.trade_gateio(market, symbol, params)
        elif market=='binance':
            data = self.trade_binance(market, symbol, params)
        elif market=='okex':
            data = self.trade_okex(market, symbol, params)
        elif market=='huobi':
            data = self.trade_huobi(market, symbol, params)

        return data

    def trade_gateio(self, market, symbol, params):
        """
        新-旧 返回的数据不包含last_id这条
        交易时间单位m
        :param market: 
        :param symbol: 
        :param params: 
        :return: 
        """
        ws = client_dict.get(self.uuid, None)
        if not ws:
            try:
                ws = create_connection('wss://ws.gateio.io/v3/', timeout=2)
            except:
                return None
            client_dict[self.uuid] = ws

        item_num = params.get('num', 500)
        last_id = params.get('last_id', 1)
        data_send_f = {"id": 123, "method": "trades.query","params": ["BTC_USDT", 2, 7177813]}
        try:
            params = [symbol, item_num, last_id]
            data_send_f['params'] = params
            data_send = json.dumps(data_send_f)
            ws.send(data_send)
            data_recv = ws.recv()
            data_recv = json.loads(data_recv)
            result = data_recv['result']
            result = self.trade_data_change(result, market)
            return result
        except:
            client_dict.pop(self.uuid, None)
            return None

    def trade_binance(self, market, symbol, params):
        """
        旧-新 返回的数据包含last_id这条
        交易时间单位ms
        :param market: 
        :param symbol: 
        :param params: 
        :return: 
        """
        client = client_dict.get(self.uuid, None)
        if not client:
            try:
                client = Client(api_key, api_secret)
            except:
                return None
            client_dict[self.uuid] = client

        item_num = params.get('num', 500)
        last_id = params.get('last_id', None)
        #BCH->BCC
        symbol = symbol.replace('BCH_', 'BCC_')
        symbol_new = symbol.replace('_', '')
        if last_id:
            params = {'symbol':symbol_new, 'limit':item_num, 'fromId':last_id}
        else:
            params = {'symbol':symbol_new, 'limit':item_num}
        try:
            result = client.get_historical_trades(**params)
            result = self.trade_data_change(result, market)
            return result
        except:
            client_dict.pop(self.uuid, None)
            return None

    def trade_okex(self, market, symbol, params):
        """
        旧-新 返回的数据不包含last_id这条
        交易时间单位ms
        最多返回60条
        :param market: 
        :param symbol: 
        :param params: 
        :return: 
        """
        item_num = params.get('num', 500)
        last_id = params.get('last_id', 0)
        symbol_new = symbol.lower()
        try:
            result = okex_trade_get(symbol_new, last_id)
            result = self.trade_data_change(result, market)
            return result
        except:
            return None

    def trade_huobi(self, market, symbol, params):
        """
        新-旧 
        交易时间单位ms
        :param market: 
        :param symbol: 
        :param params: 
        :return: 
        """
        item_num = params.get('num', 500)
        last_id = params.get('last_id', 0)
        symbol_new = symbol.lower().replace('_', '')
        try:
            result = huobi_trade_get(symbol_new, item_num)
            if result.get('status', None) == 'ok':
                result = result['data']
                result = self.trade_data_change(result, market, last_id)
                return result
        except:
            return None

    def trade_data_change(self, result, market, last_id=0):
        #如果传入last_id 返回的数据为last_id之后的最新数据
        #[{'id':int,'time':float,'price':float,'amount':float,'type':''}]
        #旧-新
        new_result = []
        if market=='gateio':
            for r in result:
                r['price'] = float(r['price'])
                r['amount'] = float(r['amount'])
            new_result = result[::-1]
        elif market=='binance':
            for r in result:
                r['price'], r['amount']= float(r['price']), float(r['qty'])
                r['time'] = r['time']/1000
                r['type'] = 'buy' if not r['isBuyerMaker'] else 'sell'
                r.pop('isBuyerMaker')
                r.pop('isBestMatch')
                r.pop('qty')
            new_result = result[1:]
        elif market=='okex':
            for r in result:
                r['id'], r['time'] = int(r['tid']), float(r['date'])
                r.pop('tid')
                r.pop('date_ms')
            new_result = result
        elif market=='huobi':
            for r in result:
                id = r['id']
                time = r['ts']/1000
                if id>last_id:
                    for d in r['data']:
                        d['id'], d['time'] = id, time
                        d['type'] = d['direction']
                        d.pop('direction')
                        d.pop('ts')
                        new_result.append(d)
                else:
                    break
            new_result = new_result[::-1]

        return new_result


def other_info(request):
    time_now = time.strftime('%Y-%m-%d %X', time.localtime())
    ip = request.META['REMOTE_ADDR']
    #print(time_now, ip)

def echo(request):
    uwsgi.websocket_handshake()
    print('new websocket')
    request_uuid = uuid.uuid1()
    while True:
        try:
            msg = uwsgi.websocket_recv()
            data = Date(request_uuid).make_data(msg)
            data = json.dumps(data).encode('utf8')
            uwsgi.websocket_send(data)
        except:
            client_dict.pop(request_uuid, None)
            mysql_dict.pop(request_uuid, None)
            print('websocket is done')
            break

def echo_once(request):
    uwsgi.websocket_handshake()
    while True:
      msg = uwsgi.websocket_recv()
      uwsgi.websocket_send(msg)