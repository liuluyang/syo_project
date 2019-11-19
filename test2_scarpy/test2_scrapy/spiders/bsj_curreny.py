

import scrapy
from test2_scrapy.items import Currency_bsj
import time

class CurrencySpider(scrapy.Spider):
    name = 'bsj_currency'
    allowed_domains = ['bishijie.com']
    url = 'http://www.bishijie.com/hangqing/coins/all'  #列表链接
    #url = 'http://www.bishijie.com/hangqing'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        currencies = response.css('#table_body tr')[:100]
        #print (len(currencies))
        for currency in currencies:
            origin_url = currency.css('.coinname a::attr(href)').extract_first()
            origin_url = response.urljoin(origin_url)
            icon = currency.css('.coinname a img::attr(src)').extract_first()
            screen_name = currency.css('.coinname a::attr(title)').extract_first()[:-10]
            name = origin_url.split('/')[-1]

            # print (origin_url, icon, screen_name, name, len(name))

            item = Currency_bsj()
            item['screen_name'] = screen_name      #列表显示名
            item['name'] = name                    #链接显示名
            item['icon'] = icon                    #图标
            item['origin_url'] = origin_url        #链接
            item['created_at'] = time.strftime('%Y-%m-%d %X', time.localtime())

            yield scrapy.Request(origin_url, callback=self.content, meta={'item':item})

        pass

    def content(self, response):
        cur_info = response.css('.cur_info_list p::text').extract()
        main_info = response.css('.main_info div.left')[0]
        tr_info = main_info.css('table tbody tr')
        other_info = tr_info[4:]

        quantity = cur_info[1]              #流通量
        circulation = cur_info[2]           #发行量
        introduction = main_info.css('p::text').extract_first()  #简介
        English_name = tr_info[1].css('th::text').extract()[1]   #英文名
        website = tr_info[1].css('a::attr(href)').extract_first() #网站
        short_name = tr_info[2].css('th::text').extract()[1]      #简称
        block_station = tr_info[2].css('a::attr(href)').extract()  #区块站
        block_station = ' '.join([response.urljoin(b) for b in block_station])
        published_at = tr_info[3].css('th::text').extract()[1]    #发行时间

        # print (introduction, English_name, website, short_name, block_station)
        # print (published_at, quantity, circulation)

        #ICO
        ico_cost = None  # ICO成本
        ico_amount = None  # ICO金额
        crowdfunding_way = None  # 众筹方式
        crowdfunding_amount = None  # 众筹金额
        opening_price = None  # 开售价格
        successful_crowdfunding_q = None  # 成功众筹数量
        crowdfunding_goal = None  # 众筹目标
        successful_crowdfunding_a = None  # 成功众筹金额

        if other_info:
            for tr in other_info:
                th_info_list = [th.css('::text').extract_first() for th in tr.css('th')]
                #print (th_info_list)
                if 'ICO成本' in th_info_list:
                    ico_cost = th_info_list[1]
                elif 'ICO金额' in th_info_list:
                    ico_amount = th_info_list[1]
                elif '众筹方式' in th_info_list:
                    crowdfunding_way = th_info_list[1]
                    crowdfunding_amount = th_info_list[3]
                elif '开售价格' in th_info_list:
                    opening_price = th_info_list[1]
                    successful_crowdfunding_q = th_info_list[3]
                elif '众筹目标' in th_info_list:
                    crowdfunding_goal = th_info_list[1]
                    successful_crowdfunding_a = th_info_list[3]

        item = response.meta['item']
        item['quantity'] = quantity
        item['circulation'] = circulation
        item['introduction'] = introduction
        item['English_name'] = English_name
        item['website'] = website
        item['short_name'] = short_name
        item['block_station'] = block_station
        item['published_at'] = published_at

        item['ico_cost'] = ico_cost
        item['ico_amount'] = ico_amount
        item['crowdfunding_way'] = crowdfunding_way
        item['crowdfunding_amount'] = crowdfunding_amount
        item['opening_price'] = opening_price
        item['successful_crowdfunding_q'] = successful_crowdfunding_q
        item['crowdfunding_goal'] = crowdfunding_goal
        item['successful_crowdfunding_a'] = successful_crowdfunding_a

        yield item
