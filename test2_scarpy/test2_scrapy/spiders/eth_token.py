import scrapy
from test2_scrapy.items import EthToken
import time


class EthTokenSpider(scrapy.Spider):
    name = 'eth_token'
    allowed_domains = ['etherscan.io']
    need_UserAgent = True

    def start_requests(self):
        self.url = 'https://etherscan.io/tokens?p={}'
        url = self.url.format(1)
        yield scrapy.Request(url, callback=self.parse, meta={'page':1})

    def parse(self, response):
        table = response.css('table tbody tr')[:]
        for num, tr in enumerate(table):
            num_text = tr.css('td')[0].css('span::text').extract_first()
            num_text = ''.join(num_text.split())
            a = tr.css('.hidden-xs a')
            desc = tr.css('.hidden-xs font::text').extract_first()
            desc = desc.replace('\n', '') if desc else None
            name_text = a.css('::text').extract_first()
            try:
                en_name, name = name_text.split('(')
            except:
                continue
            name = name[:-1].strip()
            en_name = en_name.strip()
            token = a.css('::attr(href)').extract_first()
            url_token = response.urljoin(token)
            token = token.split('/')[-1]
            #print(num, name, token, response.urljoin(token))

            item = EthToken()
            item['num'] = num_text
            item['name'] = name
            item['en_name'] = en_name
            item['desc'] = desc
            item['token'] = token

            yield scrapy.Request(url_token, callback=self.detail, meta={'item': item})

        page = response.meta['page']
        if page < 14:
            next_page = page+1
            next_url = self.url.format(next_page)
            yield scrapy.Request(next_url, callback=self.parse, meta={'page': next_page})

    def detail(self, response):
        item = response.meta['item']
        td = response.css('.table tr')
        if not td:
            yield scrapy.Request(response.url, callback=self.detail,meta={'item': item}, dont_filter=True)
            return
        td = td[3].css('td')[1]
        addresses = td.css('::text').extract_first()
        addresses = addresses.strip().split(' ')[0]
        table2 = response.css('.table')[1]
        decimal_point = table2.css('#ContentPlaceHolder1_trDecimals td::text').extract()[1].strip()

        item['addresses'] = addresses
        item['decimal_point'] = decimal_point

        #print(item)
        yield item
