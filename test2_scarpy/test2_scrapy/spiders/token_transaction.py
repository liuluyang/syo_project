import scrapy
#from test2_scrapy.items import EthToken
import time


class EthTokenSpider(scrapy.Spider):
    name = 'token_transaction'
    allowed_domains = ['etherscan.io']
    url = 'https://etherscan.io/tokentxns'
    need_UserAgent = True

    def start_requests(self):
        self.check_dict = {'token':{'address':(), 'address_2':()}}
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        print (response)
        trs = response.css('.table tr')[1:]

        for num, tr in enumerate(trs):
            #print (num, tr)
            tds = tr.css('td')
            hash_transfer = tds[0].css('a::attr(href)').extract_first()
            hash_transfer = hash_transfer.split('/')[-1]
            send_address = tds[2].css('a::attr(href)').extract_first()
            send_address = send_address.split('/')[-1].split('#')[0]
            send_name = tds[2].css('a::text').extract_first()
            recv_address = tds[4].css('a::attr(href)').extract_first()
            recv_address = recv_address.split('/')[-1].split('#')[0]
            recv_name = tds[4].css('a::text').extract_first()
            amount = tds[5].css('::text').extract_first()
            amount = float(amount.replace(',', ''))
            token = tds[6].css('a::attr(href)').extract_first()
            token = token.split('/')[-1]
            token_name = tds[6].css('a::text').extract_first()

            print (hash_transfer, send_address, send_name, recv_address, recv_name,
                   amount, token, token_name)

            transfer = self.check_dict.get(token, None)
            if transfer:
                if send_address in transfer:
                    """
                    转出
                    """
                    usd_price = 1
                elif recv_address in transfer:
                    """
                    转入
                    """
                    usd_price = 1