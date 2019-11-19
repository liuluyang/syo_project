# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


# 新闻
class NewsItem(scrapy.Item):
    group_id = scrapy.Field()     #1 内容分类标识
    origin_url = scrapy.Field()   #2 详情页链接
    origin_from = scrapy.Field()  #3 数据来源
    author = scrapy.Field()       #4 作者
    thumb = scrapy.Field()        #5 缩略图
    title = scrapy.Field()        #6 标题
    description = scrapy.Field()  #7 描述
    content = scrapy.Field()      #8 内容
    created_at = scrapy.Field()   #9 发表时间
    updated_at = scrapy.Field()   #10 入库时间


# 快讯
class NewsletterItem(scrapy.Item):
    group_id = scrapy.Field()     #1 内容分类标识 快讯8 公告9
    origin_url = scrapy.Field()   #2 详情页链接
    origin_from = scrapy.Field()  #3 数据来源（币世界 非小号）
    thumb = scrapy.Field()        #4 缩略图
    title = scrapy.Field()         #5 标题
    description = scrapy.Field()   #6 描述
    content = scrapy.Field()       #7 内容
    created_at = scrapy.Field()    #8 发表时间
    updated_at = scrapy.Field()    #9 入库时间（爬取时间）
    is_red = scrapy.Field()        #10 标注为红色
    is_more = scrapy.Field()       #11 是否有查看详情
    to_url = scrapy.Field()        #12 查看详情链接

    data_id = scrapy.Field()       #数据ID 为火球财经外媒添加


# 关注
class AttentionItem(scrapy.Item):
    parent_id = scrapy.Field()     #1 内容类型ID
    group_id = scrapy.Field()      #2 作者ID
    author = scrapy.Field()        #3 作者
    author_avatar = scrapy.Field() #4 作者头像
    content = scrapy.Field()       #5 内容
    img_urls = scrapy.Field()      #6 图片链接
    media_url = scrapy.Field()     #7 视频链接
    from_url = scrapy.Field()      #8 内容页链接
    forward = scrapy.Field()       #9 转发
    published_at = scrapy.Field()  #10 发表时间
    created_at = scrapy.Field()    #11 入库时间


#币种信息 非小号
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
    created_at = Field()  # 爬取时间


#币种信息 币世界
class Currency_bsj(scrapy.Item):
    screen_name = Field()  #列表显示名称
    name = Field()         #链接显示名称
    English_name = Field() #英文名称

    #chinese_name = Field() #中文名称              非小号
    short_name = Field()    #简称                  #币世界

    icon = Field()         #币种图标
    introduction = Field() #简介

    quantity = Field()     #流通量
    circulation = Field()  #发行量

    #exchange = Field()     #交易所                 非小号
    published_at = Field() #发行时间（日期）
    #white_paper = Field()  #白皮书                  非小号
    website = Field()      #网站 多个
    block_station = Field() #区块站 多个
    #related_concepts = Field() #相关概念 多个        非小号
    #is_token = Field()      #是否代币                非小号
    #token_platform = Field() #代币平台               非小号
    #crowdfunding_price = Field() #众筹价格           非小号

    origin_url = Field()    #币种链接
    created_at = Field()    #爬取时间

    #ICO 币世界的字段
    ico_cost = Field()      #ICO成本
    ico_amount = Field()    #ICO金额
    crowdfunding_way = Field()  #众筹方式
    crowdfunding_amount = Field() #众筹金额
    opening_price = Field()    #开售价格
    successful_crowdfunding_q = Field() #成功众筹数量
    crowdfunding_goal = Field()  #众筹目标
    successful_crowdfunding_a = Field() #成功众筹金额

#币种信息
class Currency(scrapy.Item):
    screen_name = Field()  # 列表显示名称
    name = Field()  # 链接显示名称
    English_name = Field()  # 英文名称

    chinese_name = Field() #中文名称              非小号
    short_name = Field()  # 简称                  #币世界

    icon = Field()  # 币种图标
    introduction = Field()  # 简介

    quantity = Field()  # 流通量
    circulation = Field()  # 发行量

    exchange = Field()     #交易所                 非小号
    published_at = Field()  # 发行时间（日期）
    white_paper = Field()  #白皮书                  非小号
    website = Field()  # 网站 多个
    block_station = Field()  # 区块站 多个
    related_concepts = Field() #相关概念 多个        非小号
    is_token = Field()      #是否代币                非小号
    token_platform = Field() #代币平台               非小号
    crowdfunding_price = Field() #众筹价格           非小号

    origin_url = Field()  # 币种链接
    created_at = Field()  # 爬取时间

    # ICO 币世界的字段
    ico_cost = Field()  # ICO成本
    ico_amount = Field()  # ICO金额
    crowdfunding_way = Field()  # 众筹方式
    crowdfunding_amount = Field()  # 众筹金额
    opening_price = Field()  # 开售价格
    successful_crowdfunding_q = Field()  # 成功众筹数量
    crowdfunding_goal = Field()  # 众筹目标
    successful_crowdfunding_a = Field()  # 成功众筹金额

#微博视频链接
class Media_weibo(scrapy.Item):
    id = Field()          #爬虫数据库数据id
    media_url = Field()   #微博视频链接

#代币信息
class EthToken(scrapy.Item):
    num = Field()
    name = Field()
    en_name = Field()
    desc = Field()
    token = Field()
    addresses = Field()
    decimal_point = Field()
    created_at = Field()

#代币 账户信息
class TokenAddress(scrapy.Item):
    # panking = Field()
    # address = Field()
    # market = Field()
    # amount = Field()
    # percent = Field()
    token = Field()
    data_list = Field()
    time_now = Field()
    addresses = Field()
    top_list = Field()   #[top_10, top_20, top_50, top_100]
    top_amount_list = Field() #持币数量统计

#代币 钱包转账信息
class TokenTransaction(scrapy.Item):
    address = Field()  #钱包地址
    token = Field()    #代币
    is_enter = Field() #转入转出
    amount = Field()   #总价值
    market = Field()   #交易所
    time_now = Field()

# TradingView
class TradingViewItem(scrapy.Item):
    group_id = scrapy.Field()     #1 内容分类标识
    origin_url = scrapy.Field()   #2 详情页链接
    origin_from = scrapy.Field()  #3 数据来源
    author = scrapy.Field()       #4 作者
    thumb = scrapy.Field()        #5 缩略图
    title = scrapy.Field()        #6 标题
    description = scrapy.Field()  #7 描述
    content = scrapy.Field()      #8 内容
    created_at = scrapy.Field()   #9 发表时间
    updated_at = scrapy.Field()   #10 入库时间

    symbol = scrapy.Field()       #11 交易对
    label = scrapy.Field()        #12 标签