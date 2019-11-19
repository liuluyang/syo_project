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
            os.system('scrapy crawl token_address')
            end_time = time.time()
            used_time = end_time-start_time

            sleep_time = 3600 - used_time%3600
            print('token_address一次爬取完成 用时:{}s, {}s之后再次开始'.
                  format(used_time, sleep_time))
            logger.info('token_address一次爬取完成 用时:{}s, {}s之后再次开始'.
                        format(used_time, sleep_time))
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            data = {'updated_at': updated_at, 'timestamp': end_time,'used_time': used_time}
            redis_5.rpush('spider_token', json.dumps(data))
            time.sleep(sleep_time)
        except Exception as e:
            print('token_address爬取异常：{}'.format(e))
            logger.warn('token_address爬取异常：{}'.format(e))
            if send_times<3:
                #发邮件提醒
                e = EmailSender()
                e.sendEmail('token_address爬虫异常', e)
                send_times+=1
            else:
                break
            redis_5 = LinkRedis(db=5).redis

if __name__ == '__main__':
    run_spider()