#coding:utf8
import requests
import time
from test_scrapy.settings import IS_PUSH, PUST_SPIDER_SET, PUSH_TIME, KEY_WORDS
from test_scrapy.items import NewsItem, NewsletterItem, AttentionItem
import re
from test_scrapy.utils.message_push import MessagePush
from test_scrapy.db import ConnectDB
import threading

class CloseDB(object):

    def close_spider(self, spider):
        # 关闭数据库连接
        spider.connect.close()
        spider.logger.info('{name}关闭mysql数据库连接'.format(name=spider.name))


class PushMessage(object):
    def __init__(self):
        #print ('消息推送初始化。。。')
        self.push_time = PUSH_TIME
        self.now = int(time.strftime('%H', time.localtime()))
        self.key_words = KEY_WORDS
        self.has_push = False

    def process_item(self, item, spider):
        #print ('进入消息推送。。。')
        if not IS_PUSH or not item:
            return item
        if spider.name not in PUST_SPIDER_SET:
            return item

        #print ('开启推送而且该爬虫在推送列表。。。')
        spider.logger.info('开启推送而且{name}爬虫在推送列表。。。'
                           .format(name=spider.name))

        if self.check_time():
            #print ('时间段检查通过。。。')
            spider.logger.info('时间段检查通过。。。')
            if isinstance(item, NewsItem):
                self.push_message(item['title'], item['description'], spider)
            elif isinstance(item, NewsletterItem):
                self.push_message(item['title'], item['description'], spider)
            elif isinstance(item, AttentionItem):
                self.push_message(item['author'], item['content'], spider)

        if not self.has_push:
            #print ('关键字检查。。。')
            for word in self.key_words:
                if not self.has_push:
                    if isinstance(item, NewsItem):
                        if word in item['title']:
                            self.push_message(item['title'], item['description'], spider)
                    elif isinstance(item, NewsletterItem):
                        if item['title'] and word in item['title']:
                            self.push_message(item['title'], item['description'], spider)
                        if not item['title'] and word in item['description']:
                            self.push_message(item['title'], item['description'], spider)
                    elif isinstance(item, AttentionItem):
                        if word in item['content']:
                            self.push_message(item['author'], item['content'], spider)

        if not self.has_push:
            #print ('标红字段检查。。。')
            if isinstance(item, NewsletterItem) and item['is_red']:
                self.push_message(item['title'], item['description'], spider)

        return item

    def check_time(self):
        for t in self.push_time:
            if t[0]<=self.now<t[1]:
                return True
        return False

    def push_message(self, title, content, spider):
            #print ('正在推送消息。。。',title, content)
            spider.logger.info('{name}正在推送消息。。。{title}'.format(
                        name=spider.name,title=title)
            )
            is_old_api = False
            if is_old_api:
                data = {
                    'sign': '4fecd52c593658a8a9c7656da62b7ae9',
                    'title': title,
                    'body': content,
                }
                requests.post('http://api.bitbcs.com/api/v1/sys-po-push',data=data)
            else:
                alert = {"title": title, "body": content}
                message_info = {"message_type": 2}
                device_tokens = ConnectDB().device_token_get()
                device_list = [d[0] for d in device_tokens]
                listcast_num = 400
                start_index = 0
                for i in range(len(device_tokens) // listcast_num + 1):
                    device_token = ','.join(
                        device_list[start_index:start_index + listcast_num])
                    start_index += listcast_num
                    self.push_message_thread(message_info, alert, device_token,
                                             spider.logger)

            spider.logger.info('{name}推送完毕。。。{title}'.format(
                name=spider.name, title=title)
            )
            self.has_push = True

    def push_message_thread(self, message_info, alert, device_token_s, logger):
        """
        
        :param message_info: 
        :param alert: 
        :param device_token_s: 
        :return: 
        """
        m = MessagePush()
        try:
            status_code = m.ios_listcast(device_token=device_token_s,
                                        message_info=message_info,
                                        alert=alert)
            if status_code != 200:
                logger.warning('快讯推送失败 {}'.format(status_code))
            else:
                logger.warning('快讯推送成功 {}'.format(status_code))
        except Exception as e:
            logger.warning('快讯推送异常 {}'.format(e))


class DropTag_a(object):

    def process_item(self, item, spider):
        #print ('进入a标签filter。。。')
        if isinstance(item, NewsItem) or isinstance(item, NewsletterItem):
            text = item['content']
            a_list = re.findall(r'<a.*?>', text)
            for i in a_list + ['</a>']:
                text = text.replace(i, '')

            item['content'] = text
            if a_list:
                spider.logger.info('{name}{title}内容已过滤a标签。。。'.format(
                    name=spider.name, title=item['title'])
                )

        return item