import sys
sys.path.append('/root/test_scrapy/test_scrapy')
import os
import time
import json
from test_scrapy._logger import Logger as logger
from test_scrapy.redis_link import LinkRedis
from test_scrapy.send_mail import EmailSender

def run_spider():
    redis_5 = LinkRedis(db=5).redis
    send_times = 0
    while True:
        try:
            print('正在爬取。。。')
            start_time = time.time()
            os.system('scrapy crawlall')
            end_time = time.time()
            used_time = end_time-start_time

            print('一次爬取完成 用时:{}s'.format(used_time))
            logger.info('一次爬取完成 用时:{}s'.format(used_time))
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            data = {'updated_at': updated_at, 'timestamp': end_time,'used_time': used_time}
            redis_5.rpush('spider_time', json.dumps(data))

            if used_time <= 60:
                time.sleep(60 - used_time)
            else:
                time.sleep(60)
        except Exception as e:
            print('爬取异常：{}'.format(e))
            logger.warn('爬取异常：{}'.format(e))
            if send_times<3:
                #发邮件提醒
                e = EmailSender()
                e.sendEmail('爬虫异常', e)
                send_times+=1
            else:
                break
            redis_5 = LinkRedis(db=5).redis

if __name__ == '__main__':
    run_spider()