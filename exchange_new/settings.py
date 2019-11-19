
#REDIS_HOST = '47.52.115.31'
REDIS_HOST = 'localhost'
REDIS_PASSWORD = 'lvjian'

#binance
api_key_b = 'VlbfmsWUZR8HeYFyyH251aED8EzoAj7OfhVfgX7BWO1mx5aOzPCbi1zSIrdWpznw'
api_secret_b = 'CePdSYImKP9vOSzelsixg9M2gAuKm6XnwQNK1e1m0M69OumeNAd49EMlYRi0LLzj'
binance_ticker_name_new = 'binance_ticker_new'

ticker_new_list = [
                    'gateio_ticker_new',
                    'binance_ticker_new',
                    'okex_ticker_new',
                    'huobi_ticker_new',

                    # 'bigone_ticker_new',
                    'bibox_ticker_new',

                    # 'zb_ticker_new',
                   ]

#生产数据库
# MYSQL_PRO = {'host':'47.75.163.235', 'port':3306, 'db':'bitbcs_com', 'user':'bitbcs_com',
#          'passwd':'Z76fXifXJbeGWp3T', 'use_unicode':True}
MYSQL_PRO = {'host':'localhost', 'port':3306, 'db':'lvjian', 'user':'root',
         'passwd':'123456', 'use_unicode':True}

#测试数据库
# MYSQL_TES = {'host':'47.75.163.235', 'port':3306, 'db':'test_bitbcs_com', 'user':'bitbcs_com',
#          'passwd':'Z76fXifXJbeGWp3T', 'use_unicode':True}
MYSQL_TES = {'host':'localhost', 'port':3306, 'db':'lvjian_test', 'user':'root',
         'passwd':'123456', 'use_unicode':True}

#是否测试
IS_TEST = True

#大笔监控阈值
Threshold_usd = 50000

#友盟推送
production_mode = "true"
appkey = '5b441123b27b0a6e5f00009d'
app_master_secret = 'c5col1l3jijfl16titxvbf8iloc3gkdt'
method = 'POST'
url = 'http://msg.umeng.com/api/send'

#是否开启预警异动推送
IS_PUSH = True