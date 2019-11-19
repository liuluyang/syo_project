import pymysql
import time

MYSQL_TES = {'host':'47.75.223.85', 'port':3306, 'db':'lvjian', 'user':'root',
         'passwd':'lvjian', 'use_unicode':True}

connect = pymysql.connect(**MYSQL_TES)
cursor = connect.cursor()
#print (connect.ping())

while True:
    try:
        p = connect.ping()
        print (p)
        break
    except Exception as e:
        print (e)
    time.sleep(5)


