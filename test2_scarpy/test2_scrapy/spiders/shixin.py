
import scrapy
#from test2_scrapy.items import Currency_fxh
import time

class CurrencySpider(scrapy.Spider):
    name = 'shixin'
    allowed_domains = ['zxgk.court.gov.cn']
    url = 'http://zxgk.court.gov.cn/shixin/'
    need_UserAgent = True

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        for id in ['tb-1', 'tb-2']:
            content = response.css('#{} tr'.format(id))
            for tr in content:
                name = tr.css('td a::text').extract_first()
                num = tr.css('td::text').extract()[-2]
                print(name, num)