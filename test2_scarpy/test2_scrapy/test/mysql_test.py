
import pymysql

MYSQL_REMOTE = {'host':'47.75.223.85', 'port':3306, 'db':'lvjian', 'user':'root',
         'passwd':'lvjian', 'use_unicode':True}
con_remote = pymysql.connect(**MYSQL_REMOTE)
cur_remote =  con_remote.cursor()
print (cur_remote)