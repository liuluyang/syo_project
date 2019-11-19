# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Test2ScarpyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#政策
class PolicyItem(scrapy.Item):
    origin_url = scrapy.Field()
    origin_from = scrapy.Field()
    author = scrapy.Field()
    thumb = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()

# 快讯
class NewsletterItem(scrapy.Item):
    group_id = scrapy.Field()     #1 内容分类标识 8
    origin_url = scrapy.Field()   #2 详情页链接
    origin_from = scrapy.Field()  #3 数据来源（币世界）
    thumb = scrapy.Field()        #4 图片
    title = scrapy.Field()         #5 标题
    description = scrapy.Field()   #6 描述
    content = scrapy.Field()       #7 内容
    created_at = scrapy.Field()    #8 发表时间
    updated_at = scrapy.Field()    #9 入库时间（爬取时间）
    is_red = scrapy.Field()        #10 标注为红色
    is_more = scrapy.Field()       #11 是否有查看详情
    to_url = scrapy.Field()        #12 查看详情链接

    data_id = scrapy.Field()       #数据ID 为火球财经外媒添加


#币种信息
class Currency_fxh(scrapy.Item):
    screen_name = Field()  #列表显示名称
    name = Field()         #链接显示名称
    English_name = Field() #英文名称
    chinese_name = Field() #中文名称
    icon = Field()         #币种图标
    introduction = Field() #简介

    quantity = Field()     #流通量
    circulation = Field()  #发行量

    exchange = Field()     #交易所
    published_at = Field() #发行时间（日期）
    white_paper = Field()  #白皮书
    website = Field()      #网站 多个
    block_station = Field() #区块站 多个
    related_concepts = Field() #相关概念 多个
    is_token = Field()      #是否代币
    token_platform = Field() #代币平台
    crowdfunding_price = Field() #众筹价格

    origin_url = Field()    #币种链接
    created_at = Field()    #爬取时间


#币种信息
class Currency_bsj(scrapy.Item):
    screen_name = Field()  #列表显示名称
    name = Field()         #链接显示名称
    English_name = Field() #英文名称 en

    #chinese_name = Field() #中文名称 cn
    short_name = Field()    #简称

    icon = Field()         #币种图标
    introduction = Field() #简介

    quantity = Field()     #流通量
    circulation = Field()  #发行量

    #exchange = Field()     #交易所
    published_at = Field() #发行时间（日期）
    #white_paper = Field()  #白皮书
    website = Field()      #网站 多个
    block_station = Field() #区块站 多个
    #related_concepts = Field() #相关概念 多个
    #is_token = Field()      #是否代币
    #token_platform = Field() #代币平台
    #crowdfunding_price = Field() #众筹价格

    origin_url = Field()    #币种链接
    created_at = Field()    #爬取时间

    #ICO
    ico_cost = Field()      #ICO成本
    ico_amount = Field()    #ICO金额
    crowdfunding_way = Field()  #众筹方式
    crowdfunding_amount = Field() #众筹金额
    opening_price = Field()    #开售价格
    successful_crowdfunding_q = Field() #成功众筹数量
    crowdfunding_goal = Field()  #众筹目标
    successful_crowdfunding_a = Field() #成功众筹金额


class AdressCurrency(scrapy.Item):
    name = Field()
    token = Field()
    balance_url = Field()
    balances = Field()
    num = Field()

class EthToken(scrapy.Item):
    num = Field()
    name = Field()
    en_name = Field()
    desc = Field()
    token = Field()
    addresses = Field()
    decimal_point = Field()





