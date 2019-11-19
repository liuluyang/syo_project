import scrapy
from test2_scrapy.items import AdressCurrency
import time

class CurrencySpider(scrapy.Spider):
    """
    /token/generic-tokenholders2?a=0xB8c77482e45F1F44dE1745F52C74426C631bDD52&
    s=192443301000000000000000000
    /token/generic-tokenholders2?a=0xB8c77482e45F1F44dE1745F52C74426C631bDD52&
    s=192443301 000000000000000000
    https://etherscan.io
    /token/generic-tokenholders2?a=0xB8c77482e45F1F44dE1745F52C74426C631bDD52&
    s=1.92443301E%2b26&p=2
    
    /token/generic-tokenholders2?a=0xd850942ef8811f2a866692a623011bde52a462c1&
    s=1000 000 000 000000000000000000
    /token/generic-tokenholders2?a=0xd26114cd6EE289AccF82350c8d8487fedB8A0C07&
    s=140245398 245132780789239631
    
    /token/generic-tokenholders2?a=0xe41d2489571d322189246dafa5ebde1f4699f498&
    s=1000 000 000 000000000000000000
    140245398000000000000000000
    """
    name = 'address_cur'
    allowed_domains = ['etherscan.io']
    #url = 'https://etherscan.io/'
    #url = 'https://etherscan.io/token/0xB8c77482e45F1F44dE1745F52C74426C631bDD52#balances'
    #url = 'https://etherscan.io/token/0xd26114cd6EE289AccF82350c8d8487fedB8A0C07#balances'
    #url = 'https://etherscan.io/token/0xa74476443119A942dE498590Fe1f2454d7D4aC0d#balances'

    url = 'https://etherscan.io/tokens'
    balance_url = 'https://etherscan.io/token/generic-tokenholders2?a={token}&s={s}&p={page}'
    nums = []

    need_UserAgent = True

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        table = response.css('table tbody tr')[:2]
        #print(table)
        for num, tr in enumerate(table):
            a = tr.css('.hidden-xs a')
            name = a.css('::text').extract_first()
            token = a.css('::attr(href)').extract_first()
            print (num, name, token, response.urljoin(token))

            url_token = response.urljoin(token)
            item = AdressCurrency()
            item['name'] = name
            item['token'] = token.split('/')[-1]
            item['num'] = num

            yield scrapy.Request(url_token, callback=self.detail, meta={'item': item})

    def detail(self, response):
        item = response.meta['item']
        tditem = response.css('.table .tditem')[0]
        num_text = tditem.css('::text').extract_first()
        num_text = num_text.split(' ')[0]
        print (num_text)
        total_supply = num_text.replace('\n', '')
        total_supply = total_supply.replace(',', '')
        balance_url = self.balance_url.format(token=item['token'],
                                              s=total_supply+'0'*18, page=1)


        item['balance_url'] = balance_url

        print (item, item['num'])
        self.nums.append(item['num'])
        print (len(self.nums), sorted(self.nums))

        yield scrapy.Request(balance_url, callback=self.balance, meta={'item': item})

    def balance(self, response):
        item = response.meta['item']

        trs = response.css('.table tr')[1:]
        for num, tr in enumerate(trs):
            #print (num, tr)
            tds = tr.css('td')
            panking = tds[0].css('::text').extract_first()
            address = tds[1].css('a::attr(href)').extract_first()
            amount = tds[2].css('::text').extract_first()
            percent = tds[3].css('::text').extract_first()
            print (panking, address, amount, percent)

        if trs and item['balance_url'].split('p=')[-1]=='1':
                next_url = item['balance_url'][:-1]+'2'
                yield scrapy.Request(next_url, callback=self.balance,
                                     meta={'item': item})
        pass



