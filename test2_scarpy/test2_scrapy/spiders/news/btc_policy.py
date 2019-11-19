#coding:utf8


import scrapy
from test2_scrapy.items import PolicyItem
from test2_scrapy.redis_link import LinkRedis
import time
import re

class PolicySpider(scrapy.Spider):
    name = 'btc_policy'
    allowed_domains = ['8btc.com']
    url = 'http://www.8btc.com/legal-policy'

    def start_requests(self):
        #url = 'http://www.8btc.com/legal-policy'
        self.r = LinkRedis().r
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        articles = response.xpath('//div[@id="list"]/article')
        if articles:
            for article in articles:
                item = PolicyItem()
                origin_from = article.css('.thumb a::attr(href)').extract_first() #详情页链接
                thumb = article.css('.thumb a img::attr(src)').extract_first()    #图片链接
                title = article.css('.article-content .article-title')[0].css('a::attr(title)').extract_first()
                created_at = article.css('.article-info span::text').extract_first()
                author = article.css('.article-info span')[2].css('a::text').extract_first()
                author = author.strip()
                description = article.css('.article-details::text').extract_first()
                description = ''.join(description.split())
                updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
                # print (origin_from, thumb, title, created_at, author)
                # print (description, updated_at)

                item['origin_from'] = origin_from
                item['thumb'] = thumb
                item['title'] = title
                item['created_at'] = created_at
                item['author'] = author
                item['description'] = description
                item['updated_at'] = updated_at

                if self.r.sismember('policy_urls', origin_from):
                    continue

                yield scrapy.Request(origin_from, callback=self.content, meta={'item':item})
        else:
            print ('not get data')
            time.sleep(2)
            #未得到数据 重复请求
            yield scrapy.Request(self.url, callback=self.parse, dont_filter=True)

        pass

    def content(self, response):
        #print (response.css('title').extract())
        content = response.css('.article-content p').extract()
        content = ''.join(content)
        origin_url = response.css('.source-info::text').extract_first()
        origin_url = origin_url.split()[0]
        origin_url = re.search(r'http.*', origin_url).group()
        #print ('origin_url',origin_url)
        #print (content)

        item = response.meta['item']
        item['content'] = content
        item['origin_url'] = origin_url

        yield item


