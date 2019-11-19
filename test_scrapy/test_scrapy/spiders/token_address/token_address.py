import scrapy
from test_scrapy.items import TokenAddress
from test_scrapy.db import ConnectDB
import time


class TokenAddressSpider(scrapy.Spider):
    name = 'token_address'
    allowed_domains = ['etherscan.io']
    need_UserAgent = True

    def start_requests(self):
        c = ConnectDB()
        for obj in c.token_get()[:]:
            item = TokenAddress()
            item['token'] = obj[0]
            self.url = 'https://etherscan.io/token/tokenholderchart/{}'
            url = self.url.format(obj[0])
            time.sleep(0.5)
            yield scrapy.Request(url, callback=self.parse, meta={'item':item})

    def parse(self, response):
        item = response.meta['item']
        table = response.css('#ContentPlaceHolder1_resultrows .table')
        trs = table.css('tbody tr')
        if trs:
            data_list = []
            percent_list = []
            amount_list = []
            try:
                addresses = response.css('center p::text').extract()[-1]
                addresses = int(addresses.split(':')[-1])
                for tr in trs:
                    tds = tr.css('td')
                    panking = tds[0].css('::text').extract_first()
                    address = tds[1].css('a::text').extract_first()
                    market = None
                    market_tag = tr.xpath('*').extract()[1]
                    if '(' in market_tag:
                        market = market_tag.split('(')[-1]
                        market = market.split(')')[0]
                    amount = tds[2].css('::text').extract_first()
                    amount = float(amount)
                    percent = tds[3].css('::text').extract_first()
                    percent = float(percent.rstrip('%'))
                    #print (panking, address, market, amount, percent)

                    data = {'panking':panking, 'address':address, 'market':market,
                            'amount':amount, 'percent':percent}
                    data_list.append(data)
                    percent_list.append(percent)
                    amount_list.append(amount)
            except Exception as e:
                self.logger.warn('{} 代币地址爬取异常{}'.format(item['token'], e))
                return

            top_list = [sum(percent_list[:index]) for index in [10,20,50,100]]
            top_amount_list = [sum(amount_list[:index]) for index in [10,20,50,100]]
            item['data_list'] = data_list
            item['time_now'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['top_list'] = top_list
            item['addresses'] = addresses
            item['top_amount_list'] = top_amount_list
            yield item