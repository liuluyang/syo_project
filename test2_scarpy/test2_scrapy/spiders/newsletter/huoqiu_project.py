

import scrapy
import json
import time
from test2_scrapy.items import NewsletterItem

class ProjectSpider(scrapy.Spider):
    name = 'huoqiu_project'
    allowed_domains = ['ihuoqiu.com']
    group_id = 11
    origin_from = '火球财经'

    def start_requests(self):
        url_post = 'https://www.ihuoqiu.com/Home/newsflash'
        formdata = {'data': 'GSw__2BNreotKJB2cXvF11nHQ__2C__2C',
                    'pageIndex': '1'
                    }

        yield scrapy.FormRequest(url_post, callback=self.parse,
                                 formdata=formdata)

    def parse(self, response):
        data_json = json.loads(response.text)
        #is_success = data_json.get('success')
        data_list = json.loads(data_json.get('msg', []))

        for data in data_list:
            # for k,v in data.items():
            #     print (k,v)
            # print ('~~~~~~~~~')
            data_id = data['ID']
            description = data['ShortDescription']
            created_at = data['UpdateTime']
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
            is_more = 0
            to_url = data.get('ArticleHref', None)
            if to_url:
                is_more = 1
            is_red = 0
            if data.get('Tag'):
                is_red = 1

            item = NewsletterItem()
            item['group_id'] = self.group_id
            item['origin_url'] = None
            item['origin_from'] = self.origin_from
            item['thumb'] = None
            item['title'] = None
            item['description'] = description
            item['content'] = description
            item['created_at'] = created_at
            item['updated_at'] = updated_at
            item['is_red'] = is_red
            item['is_more'] = is_more
            item['to_url'] = to_url

            item['data_id'] = data_id

            if self.redis.sismember('newsletter_urls', data_id):
                continue

            yield item

