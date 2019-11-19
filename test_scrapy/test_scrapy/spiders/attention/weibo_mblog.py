# -*- coding: utf-8 -*-
import scrapy
import json
from test_scrapy.items import AttentionItem
from test_scrapy.db import ConnectDB
import time
from scrapy.selector import Selector

class WeiboSpider(scrapy.Spider):
    name = 'weibo_mblog'
    allowed_domains = ['m.weibo.cn']
    detail_url = 'https://m.weibo.cn/status/'

    parent_id = 4    #类型ID

    def start_requests(self):
        """
        微博用户主页数据请求
        :return: 
        """
        users_request = ConnectDB().authors_get(4)
        self.url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&' \
                   'containerid=107603{uid}&page={page}'
        for user in users_request:
            user_id = user[0]
            uid = user[2]
            url = self.url.format(uid=uid, page=1)
            yield scrapy.Request(url, callback=self.parse,
                                 meta={'page':1, 'user_id':user_id})

    def parse(self, response):
        """
        用户最新微博数据列表处理
        :param response: 
        :return: 
        """
        data_json = json.loads(response.text)
        user_id = response.meta['user_id']
        if data_json['ok']:
            cards = data_json['data']['cards']
            for card in cards:
                if card['card_type']!=9 or card['mblog'].get('isTop', None):
                    continue
                mblog = card['mblog']
                request_url = self.detail_url+mblog['id']

                if self.redis.sismember('mblog_urls', request_url):
                     continue

                yield scrapy.Request(request_url, callback=self.content,
                                     meta={'user_id':user_id})

        else:
            return False

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

        parent_id = self.parent_id
        group_id = response.meta['user_id']
        author = data_dict['status']['user']['screen_name']
        author_avatar = data_dict['status']['user']['profile_image_url']
        published_at = data_dict['status']['created_at']
        content = data_dict['status']['text']
        img_urls = data_dict['status']['pic_ids']
        media_url = data_dict['status'].get('page_info',{}).get('media_info',{})\
                             .get('stream_url',None)
        media_background = data_dict['status'].get('page_info',{}).get('page_pic',{})\
                             .get('url',None)
        forward = data_dict['status'].get('retweeted_status', None)
        created_at = time.strftime('%Y-%m-%d %X', time.localtime())

        #print (name, created_at, text, mblog_id, pic_ids, media_url)
        item = AttentionItem()
        item['parent_id'] = parent_id
        item['group_id'] = group_id
        item['author'] = author
        item['author_avatar'] = author_avatar
        item['content'] = content
        item['img_urls'] = None
        item['media_url'] = None
        item['from_url'] = response.url
        item['published_at'] = published_at
        item['created_at'] = created_at
        item['forward'] = None

        #数据处理
        item['published_at'] = self.make_time(item['published_at'])
        if img_urls:
            item['img_urls'] = self.make_img_urls(img_urls)
        if media_url:
            item['media_url'] = self.make_media(media_url, media_background)
        if content:
            item['content'] = self.content_parse(content)
        #print (item['content'])

        if forward:
            request_url = self.detail_url+forward['id']
            yield scrapy.Request(request_url, callback=self.retweet,
                                     meta={'item':item})
        else:
            yield item

    def retweet(self, response):
        """
        微博转发内容的数据解析处理
        :param response: 
        :return: 
        """
        data = response.css('body script::text').extract_first()
        data = data.split('var $render_data = [')[-1]
        data = data.split('][0] || {}')[0]
        data_dict = json.loads(data)

        author = data_dict['status']['user']['screen_name']
        published_at = data_dict['status']['created_at']
        published_at = self.make_time(published_at)
        content = data_dict['status']['text']
        img_urls = data_dict['status']['pic_ids']
        img_urls = self.make_img_urls_retweet(img_urls)
        media_url = data_dict['status'].get('page_info', {}).get('media_info', {}).get('stream_url', None)
        from_url = response.url

        if content:
            content = self.content_parse(content)

        item = response.meta['item']
        item['forward'] = {
            'author':author, 'published_at':published_at, 'content':content,
            'img_urls':img_urls, 'media_url':media_url, 'from_url':from_url
        }

        #转成str
        item['forward'] = json.dumps(item['forward'])

        yield item

    def make_img_urls(self, data):
        """
        图片路径拼接
        :param data: list
        :return: json
        """
        domain = 'https://wx1.sinaimg.cn/large/{id}.jpg'
        new_data = {"pic_ids":[]}
        for id in data:
            new_data['pic_ids'].append(domain.format(id=id))
        new_data = json.dumps(new_data)

        return new_data

    def make_time(self, data):
        """
        转换时间格式
        :param data: Fri Jul 13 08:31:08 +0800 2018
        :return: 2018-7-13 08:31:08
        """
        created_at = data
        clean_time = ''.join(created_at.split('+0800'))
        created_time = time.strftime('%Y-%m-%d %X', time.strptime(clean_time, "%a %b %d %H:%M:%S  %Y"))

        return created_time

    def make_img_urls_retweet(self, data):
        """
        转发内容的图片路径拼接
        :param data: list
        :return: list
        """
        domain = 'https://wx1.sinaimg.cn/large/{id}.jpg'
        new_data = []
        for id in data:
            new_data.append(domain.format(id=id))

        return new_data

    def make_media(self, media, background):
        data = {'media_url':media, 'media_background':background}
        data = json.dumps(data)

        return data

    def content_parse(self, text):
        t1 = Selector(text="<div class='demon'>" + text + "​</div>")
        t1 = t1.xpath('//div[@class="demon"]/node()')
        text_new = []
        other_text = ''
        for t in t1:
            text = t.extract()
            alt = t.css('img::attr(alt)').extract_first()
            a = t.css('a::attr(href)').extract_first()
            if alt:
                text_new.append(alt)
            elif a:
                a_text = t.css('::text').extract_first()
                if '@' in a_text:
                    text_new.append(a_text)
                else:
                    other_text = a
            else:
                if '<br>' not in text:
                    text_new.append(text)

        # print ('解析后的内容列表：')
        # print (text_new)
        # print (other_text)

        new_text = ''
        for t in text_new:
            new_text += t.replace('\n', '')

        if len(text_new) == 1 and text_new[-1].strip().startswith('\u200b'):
            return other_text

        return new_text


