import scrapy
from test2_scrapy.items import EthToken
import time


class EthTokenSpider(scrapy.Spider):
    name = 'token_address'
    allowed_domains = ['etherscan.io']
    need_UserAgent = True

    def start_requests(self):
        self.url = 'https://etherscan.io/token/tokenholderchart/{}'
        token = None
        url = self.url.format(token)
        yield scrapy.Request(url, callback=self.parse, meta={'page':1})

    def parse(self, response):
        pass