
import scrapy
from test2_scrapy.items import Currency_fxh
import time

class CurrencySpider(scrapy.Spider):
    name = 'fxh_currency'
    allowed_domains = ['feixiaohao.com']
    url = 'https://www.feixiaohao.com/list_{page}.html'  #列表链接
    detail_url = 'https://www.feixiaohao.com/currencies/{name}/'  #详情页链接
    introduction_url = 'https://www.feixiaohao.com/coindetails/{name}/' #简介页面

    def start_requests(self):

        yield scrapy.Request(self.url.format(page=1), callback=self.parse,
                              meta={'page':1})

    def parse(self, response):
        currencies = response.css('#table tbody tr')[:2]
        for currency in currencies:
            tds = currency.css('td')
            name = currency.css("::attr(id)").extract_first() #链接中的币种名称
            screen_name = tds[1].css('a *::attr(alt)').extract_first() #列表页显示名称
            icon = tds[1].css('a *::attr(src)').extract_first()        #币种图标链接
            icon = response.urljoin(icon)
            url = self.detail_url.format(name=name)
            # url = tds[1].css('a::attr(href)').extract_first()          #详情页链接
            # url = response.urljoin(url)
            # market_cap = tds[2].css('::text').extract_first()          #市值str
            # market_cap_data = tds[2].css('::attr(data-cny)').extract_first() #市值num
            # price = tds[3].css('a::text').extract_first()            #价格str
            # price_data = tds[3].css('a::attr(data-cny)').extract_first() #价格num
            # quantity = tds[4].css('::text').extract_first()          #流通量str
            # turnover = tds[5].css('a::text').extract_first()         #成交额str
            # turnover_data = tds[5].css('a::attr(data-cny)').extract_first() #成交额num
            # gain = tds[6].css('span::text').extract_first()    #涨幅百分比
            # print (screen_name, icon, url, market_cap, market_cap_data)
            # print (price, price_data, quantity, turnover, turnover_data, gain)
            #print (icon, screen_name, name)

            item = Currency_fxh()
            item['screen_name'] = screen_name
            item['name'] = name
            item['icon'] = icon
            item['origin_url'] = url
            item['created_at'] = time.strftime('%Y-%m-%d %X', time.localtime())

            yield scrapy.Request(url,
                                 callback=self.content, meta={'item':item})



        # if currencies:
        #     next_page = response.meta['page']+1
        #     yield scrapy.Request(self.url.format(page=next_page), callback=self.parse,
        #                          meta={'page':next_page})

    def content(self, response):
        item = response.meta['item']
        firstPart = response.css('#baseInfo .firstPart .cell')[2].\
            css('.value::text').extract()  #流通量 发行量
        secondPark = response.css('#baseInfo .secondPark ul li')[:-2]

        quantity = firstPart[0]
        circulation = firstPart[1]
        English_name = secondPark[0].css('.value::text').extract_first() #英文名
        chinese_name = secondPark[1].css('.value::text').extract_first() #中文名
        exchange_num = secondPark[2].css('.value a::text').extract_first() #交易所数
        exchange_url = secondPark[2].css('.value a::attr(href)').extract_first() #交易所
        exchange_url = response.urljoin(exchange_url)
        published_at = secondPark[3].css('.value::text').extract_first() #发行时间
        white_paper = secondPark[4].css('.value a::text').extract_first() #白皮书
        website = secondPark[5].css('.value a::attr(href)').extract()    #网站
        website = ' '.join([response.urljoin(w) for w in website])
        block_station = secondPark[6].css('.value a::attr(href)').extract() #区块站
        block_station = ' '.join([response.urljoin(b) for b in block_station])

        other_info = secondPark[7:]
        related_concepts = None  # 相关概念 多个
        is_token = 0  # 是否代币
        token_platform = None  # 代币平台
        crowdfunding_price = None  # 众筹价格
        for obj in other_info:
            tag_text = obj.extract()
            if '相关概念' in tag_text:
                related_concepts = obj.css('.value a::attr(href)').extract()
                related_concepts = ' '.join([response.urljoin(r) for r in
                                             related_concepts])
            if '是否代币' in tag_text:
                is_token = 1
            if '代币平台' in tag_text:
                token_platform = obj.css('.value::text').extract_first()
            if '众筹价格' in tag_text:
                crowdfunding_price = obj.css('.value a::text').extract_first()


        # print (English_name, chinese_name)
        # print (exchange_num, exchange_url, published_at, white_paper)
        # print (website, block_station)
        # print (other_info)
        # print (related_concepts, is_token, token_platform, crowdfunding_price)

        item['quantity'] = quantity
        item['circulation'] = circulation
        item['English_name'] = English_name
        item['chinese_name'] = chinese_name
        item['exchange'] = exchange_num+' '+exchange_url
        item['published_at'] = published_at
        item['white_paper'] = white_paper
        item['website'] = website
        item['block_station'] = block_station
        item['related_concepts'] = related_concepts
        item['is_token'] = is_token
        item['token_platform'] = token_platform
        item['crowdfunding_price'] = crowdfunding_price

        yield scrapy.Request(self.introduction_url.format(name=item['name']),
                             callback=self.introduction, meta={'item':item})

    def introduction(self, response):
        item = response.meta['item']
        introduction = response.xpath('//div[@class="artBox"]/*').extract()
        introduction = ''.join(introduction)

        item['introduction'] = introduction

        #print (introduction)

        yield item


