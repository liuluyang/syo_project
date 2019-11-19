#coding:utf8


import scrapy
from test_scrapy.items import NewsletterItem
import time

class NoticeSpider(scrapy.Spider):
    name = 'fxh_notice'
    allowed_domains = ['feixiaohao.com']

    group_id = 9
    origin_from = '非小号'

    def start_requests(self):
        url = 'https://www.feixiaohao.com/notice/'

        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        notice_list = response.css('.noticeList li')

        for notice in notice_list:
            #real_name = notice.css('.web::attr(href)').extract_first().split('/')[-2]
            #screen_name = notice.css('.web::text').extract_first()
            group_id = self.group_id
            origin_from = self.origin_from
            title = notice.css('.tit::attr(title)').extract_first()
            if len(title)>255:
                title = title[:120]+'...'
            origin_url = notice.css('.tit::attr(href)').extract_first()
            created_at = notice.css('.time::text').extract_first()
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())

            description = None
            content = None
            thumb = None
            is_red = 0
            is_more = 0
            to_url = 0

            item = NewsletterItem()
            item['group_id'] = group_id
            item['origin_url'] = origin_url
            item['origin_from'] = origin_from
            item['title'] = title
            item['description'] = description
            item['content'] = content
            item['created_at'] = created_at
            item['updated_at'] = updated_at
            item['is_red'] = is_red
            item['is_more'] = is_more
            item['to_url'] = to_url
            item['thumb'] = thumb


            if origin_url.startswith('/notice'):
                item['origin_url'] = response.urljoin(origin_url)
                if self.redis.sismember('newsletter_urls', item['origin_url']):
                    continue
                else:
                    yield  scrapy.Request(item['origin_url'], callback=self.content, meta={'item':item})
            else:
                item['is_more'] = 1
                item['to_url'] = item['origin_url']
                item['origin_url'] = None
                if item['to_url'].startswith('//'):
                    item['to_url'] = item['to_url'][2:]
                item['content'] = '原文链接：' + item['to_url']
                if self.redis.sismember('newsletter_urls', item['to_url']):
                    continue

                yield item

    def content(self, response):
        item = response.meta['item']
        #原文链接
        to_url = response.css('.artBox .art-head span a::attr(href)').extract_first()
        if to_url:
            item['is_more'] = 1
            item['to_url'] = to_url
        article = response.xpath('//div[@class="article-body"]/*').extract()
        article = ''.join(article)
        content = response.xpath('//div[@class="artBox article"]/node()').extract()[5:]
        content = ''.join(content)

        if article:
            item['content'] = content
        else:
            item['content'] = content
        yield item






