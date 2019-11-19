#coding:utf8


import scrapy
import json
import time

class WeiboSpider(scrapy.Spider):
    uids = ['1663559265','1713302145']
    url_format = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=107603{uid}&page={page}'

    name = 'weibo'
    allowed_domains = ['m.weibo.cn']

    #微博列表请求api
    #start_urls = ['https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid=107603{uid}&page={page}']

    def start_requests(self):

        for uid in self.uids:
            #time.sleep(0.05)
            yield  scrapy.Request(self.url_format.format(uid=uid,page=1), callback=self.parse,
                                  meta={'uid':uid, 'page':1})


    def parse(self, response):
        #写入json文件
        # with open('t.json', 'wb') as f:
        #     f.write(response.body)

        #<class 'bytes'>
        #print (type(response.body))

        uid = response.meta['uid']
        data_json = json.loads(response.text)

        #先判断数据是否存在
        if data_json['ok']:
            data = data_json['data']

            print ('page: ',response.meta['page'],'date ',data['cards'][-1]['mblog']['created_at'],'uid: ', uid)

            page = response.meta['page']+1
            yield scrapy.Request(self.url_format.format(uid=uid,page=page), callback=self.parse,
                                  meta={'uid':uid, 'page':page})
        pass
