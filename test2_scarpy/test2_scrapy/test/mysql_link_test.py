import pymysql
import threading
import multiprocessing
from multiprocessing import Pool
import time

MYSQL = {'host':'localhost', 'port':3306, 'db':'lvjian', 'user':'root',
         'passwd':'123456', 'use_unicode':True}

con_remote = pymysql.connect(**MYSQL, cursorclass=pymysql.cursors.DictCursor)
cur_remote =  con_remote.cursor()
print (con_remote)

def price_get():
    # con_remote = pymysql.connect(**MYSQL)
    # cur_remote = con_remote.cursor()
    # print(cur_remote)
    #while True:
        # cur_remote.execute('select * from uce_ranking where symbol="BTC"')
        # data_obj = cur_remote.fetchone()
        # print (data_obj, type(data_obj))
        # time.sleep(2)
    # cur_remote.execute(
    #     'insert into uce_trade(data_id,time,price) values '
    #     '(1,"15:28","22"),(2,"15:28","33") on duplicate key update data_id=values(id)'
    # )
    # cur_remote.execute(
    #     'replace into uce_trade(data_id,time,price) VALUES '
    #     '(1,"15:28","22"),(2,"15:28","33")'
    # )
    cur_remote.execute(
        ""
        "update uce_trade "
        "set time = CASE data_id "
        "WHEN 1 THEN 'NOW' "
        "WHEN 2 THEN 'NOW' "
        "END " 
        "WHERE data_id IN (1,2) "
        ""
    )
    con_remote.commit()
    pass

if __name__ == '__main__':
    price_get()
    # for i in range(250):
    #     t = threading.Thread(target=price_get)
    #     t.start()
    # p = Pool(1)
    # for i in range(1):
    #     p.apply_async(price_get)
    # p.close()
    # p.join()


