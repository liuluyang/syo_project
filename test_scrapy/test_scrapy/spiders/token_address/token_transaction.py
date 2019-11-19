import scrapy
from test_scrapy.settings import transaction_value
from test_scrapy.items import TokenTransaction
from test_scrapy.db import ConnectDB
import time
import json


class EthTokenSpider(scrapy.Spider):
    name = 'token_transaction'
    allowed_domains = ['etherscan.io']
    url = 'https://etherscan.io/tokentxns'
    need_UserAgent = True

    def start_requests(self):
        self.transaction_check = {'token':{'address':(), 'address_2':()}}
        token_market = self.redis.get('token_market')
        if token_market:
            transaction_check = json.loads(token_market.decode())
        else:
            transaction_check = {}
            address_markets = ConnectDB().address_market_get()
            for obj in address_markets:
                token = obj[-1]
                if token not in transaction_check:
                    transaction_check[token] = {}
                    transaction_check[token][obj[1]] = obj
            self.redis.set('token_market', json.dumps(transaction_check))
        self.transaction_check = transaction_check

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        trs = response.css('.table tr')[1:]
        if not trs:
            print ('未获取到数据！')
            return
        for num, tr in enumerate(trs):
            tds = tr.css('td')
            transfer_hash = tds[0].css('a::attr(href)').extract_first()
            transfer_hash = transfer_hash.split('/')[-1]
            if self.redis.sismember('token_transfer_hash', transfer_hash):
                continue

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

            # print (transfer_hash, send_address, send_name, recv_address, recv_name,
            #        amount, token, token_name)

            transfer = self.transaction_check.get(token, None)
            if transfer:
                item = TokenTransaction()
                item['token'] = token
                item['time_now'] = time.strftime('%Y-%m-%d %X', time.localtime())
                is_enter = 0
                if send_address in transfer: #转出
                    is_enter = -1
                    item['address'] = send_address
                    item['is_enter'] = is_enter
                    item['market'] = transfer[send_address][-2]
                    print (token, token_name, '转出', send_address, amount, send_name)
                elif recv_address in transfer: #转入
                    is_enter = 1
                    item['address'] = recv_address
                    item['is_enter'] = is_enter
                    item['market'] = transfer[recv_address][-2]
                    print(token, token_name, '转入', recv_address, amount, recv_name)
                if is_enter:
                    timestamp = time.time()
                    token_price = self.redis.hget('token_price', token)
                    if token_price:
                        token_price = json.loads(token_price.decode())
                        if timestamp - token_price['timestamp'] < 3600:
                            self.redis.sadd('token_transfer_hash', transfer_hash)
                            usd_price = token_price['usd_price']
                            trading_volume = usd_price * amount
                            if trading_volume > transaction_value:
                                item['amount'] = trading_volume
                                yield item
                        else:
                            url = 'https://etherscan.io/token/{}'.format(token)
                            yield scrapy.Request(url, callback=self.token_price,
                                                 meta={'item':item, 'amount':amount,
                                                       'transfer_hash':transfer_hash})
                    else:
                        url = 'https://etherscan.io/token/{}'.format(token)
                        yield scrapy.Request(url, callback=self.token_price,
                                             meta={'item': item, 'amount': amount,
                                                   'transfer_hash': transfer_hash})

    def token_price(self, response):
        """
        获取代币美元价格
        :param response: 
        :return: 
        """
        print (response)
        tr = response.css('.table tr')
        td = tr[2].css('td')[1]
        price = td.css('::text').extract_first()
        usd_price = float(price.split('@')[0].strip()[1:])
        print('价格：', price, usd_price)

        item = response.meta['item']
        amount = response.meta['amount']
        transfer_hash = response.meta['transfer_hash']
        self.redis.sadd('token_transfer_hash', transfer_hash)
        trading_volume = usd_price * amount
        if trading_volume > transaction_value:
            item['amount'] = trading_volume
            yield item

        timestamp = time.time()
        updated_at = time.strftime('%Y-%m-%d %X', time.localtime())
        token_price = {'usd_price':usd_price, 'timestamp':timestamp,
                       'updated_at':updated_at}
        self.redis.hset('token_price', item['token'], json.dumps(token_price))
