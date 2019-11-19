# -*- coding: utf-8 -*-
import scrapy
import json
from test_scrapy.items import Media_weibo
from test_scrapy.db import ConnectDB

class WeiboSpider(scrapy.Spider):
    name = 'media_update'
    allowed_domains = ['m.weibo.cn']
    detail_url = 'https://m.weibo.cn/status/'

    update_num = 0
    success_num = 0

    def start_requests(self):
        """
        微博主页数据请求
        :return: 
        """
        obj_list = ConnectDB().media_get()
        self.update_num = len(obj_list)

        for obj in obj_list:
            id = obj[0]
            request_url = obj[2]

            yield scrapy.Request(request_url, callback=self.content,
                                 meta = {'id':id})

    def content(self, response):
        """
        微博正文的数据解析处理
        :param response: 
        :return: 
        """
        data = response.css('body script::text').extract_first()
        data = data.split('var $render_data = [')[-1]
        data = data.split('][0] || {}')[0]
        data_dict = json.loads(data)

        media_url = data_dict['status'].get('page_info',{}).get('media_info',{})\
                             .get('stream_url',None)
        media_background = data_dict['status'].get('page_info',{}).get('page_pic',{})\
                             .get('url',None)

        item = Media_weibo()
        item['media_url'] = None
        item['id'] = response.meta['id']

        #print(item['id'], media_url, created_at)

        if media_url:
            item['media_url'] = self.make_media(media_url, media_background)
            yield item
        else:
            pass

    def make_media(self, media, background):
        data = {'media_url':media, 'media_background':background}
        data = json.dumps(data)

        return data


