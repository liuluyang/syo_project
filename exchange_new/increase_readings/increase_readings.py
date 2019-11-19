import sys
sys.path.append('/root/exchange_new')
import time
import random
import pymysql
from utils._logger import Logger as logger
from settings import MYSQL_TES, MYSQL_PRO, IS_TEST

#IS_TEST = True
class IncreaseReadings(object):
    def __init__(self):
        self.hot_time = [0,1,2,3,4]
        self.cold_time = [0,1]
        self.update_num = [1,2,1,1,2,1,2]

    def mysql_obj_get(self):
        """
        连接数据库 并返回对象
        :return: 
        """
        MYSQL = MYSQL_TES if IS_TEST else MYSQL_PRO
        connect = pymysql.connect(**MYSQL, cursorclass=pymysql.cursors.DictCursor)
        cursor = connect.cursor()

        return cursor, connect

    def news_hits_increase(self):
        NOW = int(time.strftime('%H', time.localtime()))
        is_update = random.choice(self.hot_time) if 10<=NOW<=12 else random.choice(self.cold_time)
        if not is_update:
            #print('news_hits不进行更新')
            return False
        try:
            cursor, connect = self.mysql_obj_get()
        except Exception as e:
            logger.warning('news_hits自增阅读量mysql连接异常{}'.format(e))
            return False

        sql_one = 'select * from uce_spider_news_hits'
        cursor.execute(sql_one)
        news_hits = cursor.fetchall()
        news_hits_id = {new['article_id']:new['views'] for new in news_hits}

        sql_two = 'select id from uce_spider_news order by id desc limit 50'
        cursor.execute(sql_two)
        news = cursor.fetchall()

        for new in news:
            is_update = random.choice(
                self.hot_time) if 10 <= NOW <= 12 else random.choice(
                self.cold_time)
            if not is_update:
                #print('news_hits不进行更新')
                continue
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            views = news_hits_id.get(new['id'])
            if views:
                #change
                views += 1
                sql = 'update uce_spider_news_hits set views=%s, updated_at=%s ' \
                      'where article_id=%s'
                cursor.execute(sql, (views, time_now, new['id']))
            else:
                #add
                views = 1
                sql = 'insert into uce_spider_news_hits(article_id, views, created_at)' \
                        ' value (%s, %s, %s)'
                cursor.execute(sql, (new['id'], views, time_now))
        connect.commit()
        connect.close()

        return True

    def look_total_increase(self):
        NOW = int(time.strftime('%H', time.localtime()))
        # is_update = random.choice(self.hot_time) if 10<=NOW<=22 else random.choice(self.cold_time)
        # if not is_update:
        #     #print('look_total不进行更新')
        #     return False
        try:
            cursor, connect = self.mysql_obj_get()
        except Exception as e:
            logger.warning('look_total自增阅读量mysql连接异常{}'.format(e))
            return False

        sql_one = 'select * from uce_spider_look_total'
        cursor.execute(sql_one)
        look_total = cursor.fetchall()
        look_total_id = {new['article_id']:[new['lookup'],new['lookdown']]
                        for new in look_total}

        sql_two = 'select id from uce_spider_kuaixun order by id desc limit 50'
        cursor.execute(sql_two)
        news = cursor.fetchall()

        for new in news:
            is_update = random.choice(
                self.hot_time) if 10 <= NOW <= 22 else random.choice(
                self.cold_time)
            if not is_update:
                #print('news_hits不进行更新')
                continue
            time_now = time.strftime('%Y-%m-%d %X', time.localtime())
            nums = look_total_id.get(new['id'])
            if nums:
                #change
                up, down = nums[0], nums[-1]
                up += random.choice(self.update_num)
                down += random.choice(self.update_num)
                sql = 'update uce_spider_look_total set lookup=%s, lookdown=%s, ' \
                      'updated_at=%s where article_id=%s'
                cursor.execute(sql, (up, down, time_now, new['id']))
            else:
                #add
                up = random.choice(self.update_num)
                down = random.choice(self.update_num)
                views = random.choice(self.update_num)
                sql = 'insert into uce_spider_look_total(category_id, ' \
                      'article_id, lookup, lookdown, created_at) value ' \
                      '(%s, %s, %s, %s, %s)'
                cursor.execute(sql, (8, new['id'], up, down, time_now))
        connect.commit()
        connect.close()

        return True


if __name__ == '__main__':
    c = IncreaseReadings()
    c.news_hits_increase()
    c.look_total_increase()