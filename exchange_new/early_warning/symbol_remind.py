import sys
sys.path.append('/root/exchange_new')
import json
import threading
from queue import Queue
import time
import pymysql
from settings import MYSQL_PRO, MYSQL_TES, IS_TEST
from utils._logger import Logger as logger
from utils._redis_link import redis_2, redis_3, redis_4
from utils.message_push import MessagePush


#IS_TEST = True
class Remind(object):
    redis_3 = redis_3
    redis_4 = redis_4

    def __init__(self):
        """
        self.compare_data = {'gateio':{'BTC_USDT':{'close':123,'change':3}},
                             'binance':{'BTC_USDT':{'close':123,'change':3}}
                             }
        """
        self.IS_TEST = IS_TEST
        self.compare_data = {}
        self.frequency_change = {1:604800, 2:86400, 3:60}  #提醒频率

    def mysql_obj_get(self):
        """
        连接数据库
        :return: 
        """
        MYSQL = MYSQL_TES if self.IS_TEST else MYSQL_PRO
        self.connect = pymysql.connect(**MYSQL,
                                       cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connect.cursor()

    def _device_token_get(self):
        """
        获取用户device_token
        :return: 
        """
        data_obj = []
        users_device = {}
        try:
            sql = 'select *from uce_sys_device where user_id!=0'
            self.cursor.execute(sql)
            data_obj = self.cursor.fetchall()
            self.connect.commit()
        except Exception as e:
            logger.warning('预警监控mysql数据获取异常3:{}'.format(e))
            num = 1
            while True:
                try:
                    self.connect.ping()
                    break
                except Exception as e:
                    logger.warning('预警监控mysql连接异常3:{}'.format(e))
                    time.sleep(60 * num)
                    num += 1
            time.sleep(5)

        for obj in data_obj:
            user_id = obj['user_id']
            if user_id in users_device:
                users_device[user_id].append(obj['device_token'])
            else:
                users_device[user_id] = [obj['device_token']]
        self.users_device = users_device

    def _send_remind(self, message, market, symbol, user_id, mode=None,
                     message_type=1):
        """
        发送提醒
        :return: 
        """
        title = '币掌柜行情提醒'
        device_tokens = self.users_device.get(user_id, [])
        def send():
            _symbol, currency = symbol.split('_')
            alert = {'title':title, 'body':message}
            message_info = {"message_type": message_type,
                            "market": market.capitalize(),
                            "symbol": _symbol,
                            "currency": currency}
            m = MessagePush(mode)
            for device_token in device_tokens:
                try:
                    status_code = m.ios_unicast(device_token=device_token,
                                                message_info=message_info,
                                                alert=alert)
                    if status_code!=200:
                        logger.warning('预警推送失败 {}'.format(status_code))
                except Exception as e:
                    logger.warning('预警推送异常 {}'.format(e))

        t = threading.Thread(target=send)
        t.start()

    def _change_monitor(self):
        """
        24h 价格、涨幅变动监测
        :return: 
        """
        def time_check(time_field):
            if start_timestamp - remind_info[time_field] > remind_info['rule']:
                return True
            return False

        start_timestamp = time.time()
        for market, symbols in list(self.remind_data.items()):
            for symbol in symbols.keys():
                symbol_data = self.redis_3.hget('{}_ticker_new'.format(market), symbol)
                symbol_data = json.loads(symbol_data.decode()) if symbol_data else None
                compare_price = self.compare_data.get(market, {}).get(symbol, {}).get('close')
                compare_change = self.compare_data.get(market, {}).get(symbol, {}).get('change')
                if symbol_data:
                    now_price = symbol_data['close']
                    now_price = float(now_price)
                    cny_price = symbol_data['cny_price']
                    change = symbol_data['change']
                    change = self.num_parse(float(change))
                    is_price = 1 if compare_price and now_price!=compare_price else 0
                    is_change = 1 if compare_change and change!=compare_change else 0
                    if is_price or is_change:
                        """
                        价格或涨跌幅有变动
                        """
                        for id in symbols[symbol]:
                            is_send = 0
                            remind_info = self.redis_data.get(id)
                            if not remind_info:
                                continue
                            now_price = self.num_parse(cny_price) if \
                                remind_info['unit']=='cny' else now_price
                            time_now = time.strftime('%H:%M', time.localtime())
                            if is_price and time_check('up_timestamp') and \
                                            remind_info['up_status'] and \
                                            now_price>remind_info['up']:
                                """
                                上涨提醒
                                """
                                #print ('上涨提醒:', id, market, symbol, now_price, time_now)
                                remind_info['up_timestamp'] = start_timestamp
                                is_send = 1
                                price_type = '¥' if remind_info['unit']=='cny' else ''
                                message = '{market} {symbol}当前价格为{price_type}' \
                                          '{now_price} 高于预警值{price_type}{up} [{time_now}]'.\
                                    format(market=market.capitalize(),
                                           symbol=symbol,now_price=now_price,
                                           price_type=price_type,
                                           up=remind_info['up'], time_now=time_now)
                                self._send_remind(message, market, symbol,
                                                  remind_info['user_id'])
                            elif is_price and time_check('down_timestamp') and \
                                    remind_info['down_status'] \
                                    and now_price<remind_info['down']:
                                """
                                下跌提醒
                                """
                                #print('下跌提醒:', id, market, symbol, now_price, time_now)
                                remind_info['down_timestamp'] = start_timestamp
                                is_send = 1
                                price_type = '¥' if remind_info['unit'] == 'cny' else ''
                                message = '{market} {symbol}当前价格为{price_type}' \
                                          '{now_price} 低于预警值{price_type}{down} [{time_now}]'. \
                                    format(market=market.capitalize(),
                                           symbol=symbol, now_price=now_price,
                                           price_type=price_type,
                                           down=remind_info['down'],
                                           time_now=time_now)
                                self._send_remind(message, market, symbol,
                                                  remind_info['user_id'])
                            if is_change and time_check('up_p_timestamp') and \
                                    remind_info['up_p_status'] \
                                    and change>remind_info['up_p']:
                                """
                                涨幅提醒
                                """
                                #print('涨幅提醒:', id, market, symbol, change, time_now)
                                remind_info['up_p_timestamp'] = start_timestamp
                                is_send = 1
                                message = '{market} {symbol}当前涨幅为{change}%' \
                                          ' 高于预警值{up_p}% [{time_now}]'. \
                                    format(market=market.capitalize(),
                                           symbol=symbol, change=change,
                                           up_p=remind_info['up_p'],
                                           time_now=time_now)
                                self._send_remind(message, market, symbol,
                                                  remind_info['user_id'])
                            elif is_change and time_check('down_p_timestamp') and \
                                    remind_info['down_p_status'] \
                                    and change<-remind_info['down_p']:
                                """
                                跌幅提醒
                                """
                                #print('跌幅提醒:', id, market, symbol, change, time_now)
                                remind_info['down_p_timestamp'] = start_timestamp
                                is_send = 1
                                message = '{market} {symbol}当前跌幅为{change}%' \
                                          ' 低于预警值{down_p}% [{time_now}]'. \
                                    format(market=market.capitalize(),
                                           symbol=symbol, change=change,
                                           down_p=remind_info['down_p'],
                                           time_now=time_now)
                                self._send_remind(message, market, symbol,
                                                  remind_info['user_id'])
                            if is_send:
                                self.redis_3.hset('remind_data',
                                                  remind_info['id'],
                                                  json.dumps(remind_info))
                    if not self.compare_data.get(market):
                        self.compare_data[market] = {}
                    self.compare_data[market][symbol] = {'close':now_price,
                                                         'change':change}

    def _sub_info_update(self):
        """
        对比redis数据 添加新订阅
        :return: 
        """
        self.redis_data = {}
        for info in self.users_info:
            id = info['id']
            redis_info = self.redis_3.hget('remind_data', id)
            redis_info = json.loads(redis_info.decode()) if redis_info else {}
            if redis_info.get('updated_at')!=info['updated_at']:
                info['up_timestamp'], info['down_timestamp'] = 0, 0
                info['up_p_timestamp'], info['down_p_timestamp'] = 0, 0
                self.redis_3.hset('remind_data', id, json.dumps(info))
            else:
                self.redis_data[id] = redis_info

    def _remind_data_get(self):
        """
        获取用户订阅提醒信息
        :return: 
        """
        data_obj = []
        try:
            sql = 'select *from uce_remind where top_status=1 or down_status=1 or ' \
                  'top_p_status=1 or down_p_status=1'
            self.cursor.execute(sql)
            data_obj = self.cursor.fetchall()
            self.connect.commit()
        except Exception as e:
            logger.warning('预警监控mysql数据获取异常:{}'.format(e))
            num = 1
            while True:
                try:
                    self.connect.ping()
                    break
                except Exception as e:
                    logger.warning('预警监控mysql连接异常:{}'.format(e))
                    time.sleep(60*num)
                    num+=1
            time.sleep(5)

        users_info = []
        remind_data = {}
        for obj in data_obj:
            rule = self.frequency_change.get(obj['frequency'])
            if not rule:
                continue
            market = obj['platform'].lower()
            symbol = '{}_{}'.format(obj['symbol'],obj['currency'])
            user_info = {'id':obj['id'],'user_id':obj['user_id'],
                    'unit':obj['unit'].lower(), 'up':obj['top'],
                    'down':obj['down'],'down_p_status':obj['down_p_status'],
                    'up_p':obj['top_p'], 'down_p':obj['down_p'],
                    'up_status':obj['top_status'],'down_status':obj['down_status'],
                    'up_p_status':obj['top_p_status'],
                    'updated_at':str(obj['updated_at']), 'rule':rule}
            users_info.append(user_info)
            market_dict = remind_data.get(market)
            if market_dict:
                symbol_dict = market_dict.get(symbol)
                if symbol_dict:
                    symbol_dict.append(obj['id'])
                else:
                    market_dict[symbol] = [obj['id']]
            else:
                remind_data[market] = {symbol:[obj['id']]}
        self.users_info = users_info
        self.remind_data = remind_data

    def main(self, sleep_time=5):
        """
        主函数(价格预警监控)
        :return: 
        """
        self.mysql_obj_get()
        while True:
            start = time.time()
            self._remind_data_get()
            self._device_token_get()
            self._sub_info_update()
            self._change_monitor()
            used_time = time.time()-start
            if used_time>5:
                logger.warning('预警监控耗时异常：{}s'.format(used_time))
            #print('用时：',used_time)
            time.sleep(sleep_time)

    def _remind_data_get_2(self):
        """
        获取用户订阅提醒信息
        为异动监控提供数据（盘中大涨大跌 大笔买入卖出等）
        :return: 
        """
        data_obj = []
        try:
            sql = 'select *from uce_remind where platform=%s'
            self.cursor.execute(sql, (self.market,))
            data_obj = self.cursor.fetchall()
            self.connect.commit()
        except Exception as e:
            logger.warning('预警监控mysql数据获取异常2:{}'.format(e))
            num = 1
            while True:
                try:
                    self.connect.ping()
                    break
                except Exception as e:
                    logger.warning('预警监控mysql连接异常2:{}'.format(e))
                    time.sleep(60*num)
                    num+=1
            time.sleep(5)

        remind_data = {}
        for obj in data_obj:
            symbol = '{}_{}'.format(obj['symbol'],obj['currency'])
            if symbol in remind_data:
                remind_data[symbol].append(obj)
            else:
                remind_data[symbol] = [obj]

        self.remind_data = remind_data
        self.remind_data['timestamp'] = time.time()

    def _change_monitor_2(self):
        """
        异动监测
        :return: 
        """
        while True:
            change_data = self.q_remind.get()
            symbol = change_data['symbol']
            signal_type = change_data['signal_type']
            data = change_data['data']
            users_info = self.remind_data.get(symbol)
            data_interval = time.time()-self.remind_data['timestamp']
            if users_info and data_interval<10:
                for user in users_info:
                    if user.get(signal_type):
                        time_now = time.strftime('%H:%M', time.localtime())
                        #print ('异动提醒：',signal_type, self.market, symbol, data)
                        if signal_type=='signal_2':
                            message = '{market} {symbol}{con_type}${con} [{time_now}]'\
                                .format(market=self.market.capitalize(),
                                        symbol=symbol, con_type=data['con_type'],
                                        con=round(data['con'],2), time_now=time_now)
                        else:
                            message = '{market} {symbol}{con_type}{con}% [{time_now}]' \
                                .format(market=self.market.capitalize(),
                                        symbol=symbol, con_type=data['con_type'],
                                        con=round(data['con'],2), time_now=time_now)
                        self._send_remind(message, self.market, symbol,
                                          user['user_id'])

            elif data_interval>=10:
                logger.warning('异动数控更新异常 时间间隔:{}'.format(data_interval))

            self.q_remind.task_done()

    def main_2(self, market, sleep_time=5):
        """
        主函数(异动预警监控)
        :param market: 
        :return: 
        """
        self.remind_data = {'timestamp':time.time()}
        self.users_device = {}
        self.market = market
        self.mysql_obj_get()
        self.q_remind = Queue()

        t = threading.Thread(target=self._change_monitor_2)
        t.start()
        #测试数据
        # t = threading.Thread(target=self.test_data_put)
        # t.start()

        def data_get():
            while True:
                self._remind_data_get_2()
                self._device_token_get()
                #测试数据
                #self.test_data_get()
                time.sleep(sleep_time)
        t = threading.Thread(target=data_get)
        t.start()

    def test_data_put(self):
        while True:
            self.q_remind.put({'symbol':'BNB_USDT','signal_type':'signal_1',
                               'data':{'con_type':'盘中大涨','con':11}})
            self.q_remind.put({'symbol': 'BNB_USDT', 'signal_type': 'signal_2',
                               'data': {'con_type':'大笔买入','con':70000}})
            self.q_remind.put({'symbol': 'BNB_USDT', 'signal_type': 'signal_3',
                               'data': {'con_type':'急速拉升','con':3}})
            self.q_remind.put({'symbol': 'BNB_USDT', 'signal_type': 'signal_4',
                               'data': {'con_type':'快速反弹','con':6}})
            time.sleep(1)

    def test_data_get(self):

        symbols = self.redis_3.hkeys('{}_ticker_new'.format(self.market))
        remind_data = {}
        for symbol in symbols:
            user_info = {'signal_1':1,'signal_2':1,'signal_3':1,'signal_4':1,
                         'id':1,'user_id':1}
            remind_data[symbol.decode()] = [user_info]

        self.remind_data = remind_data
        self.remind_data['timestamp'] = time.time()

    def num_parse(self, num):
        """
        对价格、涨跌幅进行有效数字截取
        :param num: 
        :return: num
        """
        if num == 0:
            return num
        # 是否负数
        is_negative = True if num < 0 else False
        num = abs(num)
        num_str = str(num)
        new_num = num
        if num >= 1:
            new_num = round(num, 2)
        elif num < 1:
            others = {'0', '.'}
            for index, s in enumerate(num_str):
                if s not in others:
                    new_num = float(num_str[0:index + 3])
                    if new_num >= 1:
                        new_num = round(num, 6)
                    break

        return new_num / -1 if is_negative else new_num

    def remind_history(self, **kwargs):
        time_now = time.strftime('%Y-%m-%d %X', time.localtime())
        self.cursor.execute(
            """
            insert into uce_remind_history(user_id, content, type, is_read, 
                created_at, updated_at) value(%s, %s, %s, %s, %s, %s)
            """,
            (
                kwargs.get('user_id', 0),
                kwargs.get('content'),
                kwargs.get('type', 0),
                0,
                time_now,
                time_now
            )
        )


if __name__ == '__main__':
    r = Remind()
    r.main()



