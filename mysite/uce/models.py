from django.db import models

# Create your models here.


#新闻
class Spider_news(models.Model):
    """
    新闻政策栏目
    数据来源网站 ：hellochain 巴比特 未来财经 雷鹿财经 核财经
    内容分类标识：6
    """
    group_id = models.SmallIntegerField(verbose_name='内容分类标识')
    origin_url = models.CharField(max_length=255, null=True, verbose_name='内容页链接')
    origin_from = models.CharField(max_length=255, null=True, verbose_name='数据来源网站')
    title = models.CharField(max_length=255, null=True, verbose_name='标题')
    thumb = models.CharField(max_length=255, null=True, verbose_name='缩略图')
    description = models.TextField(null=True, verbose_name='内容概述')
    content = models.TextField(null=True, verbose_name='正文')
    created_at = models.DateTimeField(null=True, verbose_name='发表时间')
    updated_at = models.DateTimeField(null=True, verbose_name='入库时间')

    author = models.CharField(max_length=255, null=True, verbose_name='作者')


#快讯
class Spider_kuaixun(models.Model):
    """
    快讯栏目
    数据来源网站：币世界 非小号
    内容分类标识：8       9
    """
    group_id = models.SmallIntegerField(verbose_name='内容分类标识')
    origin_url = models.CharField(max_length=255, null=True, verbose_name='内容页链接')
    origin_from  = models.CharField(max_length=255, null=True, verbose_name='数据来源网站')
    title = models.CharField(max_length=255, null=True, verbose_name='标题')
    thumb = models.CharField(max_length=255, null=True, verbose_name='缩略图')
    description = models.TextField(null=True, verbose_name='内容概述')
    content = models.TextField(null=True, verbose_name='正文')
    created_at = models.DateTimeField(null=True, verbose_name='发表时间')
    updated_at = models.DateTimeField(null=True, verbose_name='入库时间')

    is_red = models.SmallIntegerField(null=True, default=0, verbose_name='内容标红')
    is_more = models.SmallIntegerField(null=True, default=0, verbose_name='查看详情')
    to_url = models.CharField(max_length=255, null=True, verbose_name='查看详情链接')


#关注
class Spider_guanzhu(models.Model):
    """
    关注栏目
    微博 4
    推特 5
    """
    parent_id = models.SmallIntegerField(verbose_name='上级ID')  #4微博 5推特
    group_id = models.IntegerField(verbose_name='作者ID')
    author = models.CharField(max_length=255, verbose_name='作者')
    author_avatar = models.CharField(max_length=255, verbose_name='头像', null=True)
    content = models.TextField(verbose_name='内容', null=True)
    img_urls = models.TextField(verbose_name='图片', null=True)
    media_url = models.TextField(verbose_name='视频', null=True)
    from_url = models.CharField(max_length=255, verbose_name='内容页链接', null=True)
    forward = models.TextField(verbose_name='转发内容', null=True)
    published_at = models. DateTimeField(verbose_name='发布时间', null=True)
    created_at = models.DateTimeField(verbose_name='入库时间', null=True)

#作者
class Guanzhu_author(models.Model):
    """
    关注栏目作者
    微博作者 4
    推特作者 5
    """
    name = models.CharField(max_length=255, verbose_name='作者')
    uuid = models.UUIDField(verbose_name='uuid', null=True)
    parent_id = models.SmallIntegerField(verbose_name='类型ID')

#币种信息
class Currency_fxh(models.Model):
    """
    非小号网站
    币种信息
    """
    screen_name = models.CharField(max_length=255, null=True)  # 列表显示名称
    name = models.CharField(max_length=255, null=True)  # 链接显示名称
    English_name = models.CharField(max_length=255, null=True)  # 英文名称
    chinese_name = models.CharField(max_length=255, null=True)  # 中文名称
    icon = models.CharField(max_length=255, null=True)  # 币种图标
    introduction = models.TextField(null=True)  # 简介

    quantity = models.CharField(max_length=255, null=True)  # 流通量
    circulation = models.CharField(max_length=255, null=True)  # 发行量

    exchange = models.CharField(max_length=255, null=True)  # 交易所
    published_at = models.DateField(null=True)  # 发行时间（日期）
    white_paper = models.CharField(max_length=255, null=True)  # 白皮书
    website = models.CharField(max_length=255, null=True)  # 网站 多个
    block_station = models.CharField(max_length=255, null=True)  # 区块站 多个
    related_concepts = models.CharField(max_length=255, null=True)  # 相关概念 多个
    is_token = models.SmallIntegerField(null=True)  # 是否代币
    token_platform = models.CharField(max_length=255, null=True)  # 代币平台
    crowdfunding_price = models.CharField(max_length=255, null=True)  # 众筹价格

    origin_url = models.CharField(max_length=255, null=True)  # 币种链接
    created_at = models.DateTimeField(null=True)  # 爬取时间


#币种信息
class Currency_bsj(models.Model):
    """
    币世界网站
    币种信息
    """
    screen_name = models.CharField(max_length=255, null=True)  # 列表显示名称
    name = models.CharField(max_length=255, null=True)  # 链接显示名称
    English_name = models.CharField(max_length=255, null=True)  # 英文名称

    # chinese_name = Field() #中文名称
    short_name = models.CharField(max_length=255, null=True)  # 简称

    icon = models.CharField(max_length=255, null=True)  # 币种图标
    introduction = models.TextField(null=True)  # 简介

    quantity = models.CharField(max_length=255, null=True)  # 流通量
    circulation = models.CharField(max_length=255, null=True)  # 发行量

    # exchange = Field()     #交易所
    published_at = models.DateField(null=True)  # 发行时间（日期）
    # white_paper = Field()  #白皮书
    website = models.CharField(max_length=255, null=True)  # 网站 1个
    block_station = models.CharField(max_length=255, null=True)  # 区块站 多个
    # related_concepts = Field() #相关概念 多个
    # is_token = Field()      #是否代币
    # token_platform = Field() #代币平台
    # crowdfunding_price = Field() #众筹价格

    origin_url = models.CharField(max_length=255, null=True)  # 币种链接
    created_at = models.DateTimeField(null=True)  # 爬取时间

    # ICO
    ico_cost = models.CharField(max_length=255, null=True)  # ICO成本
    ico_amount = models.CharField(max_length=255, null=True)  # ICO金额
    crowdfunding_way = models.CharField(max_length=255, null=True)  # 众筹方式
    crowdfunding_amount = models.CharField(max_length=255, null=True)  # 众筹金额
    opening_price = models.CharField(max_length=255, null=True)  # 开售价格
    successful_crowdfunding_q = models.CharField(max_length=255, null=True)  # 成功众筹数量
    crowdfunding_goal = models.CharField(max_length=255, null=True)  # 众筹目标
    successful_crowdfunding_a = models.CharField(max_length=255, null=True)  # 成功众筹金额

#币种合并信息
class Currency(models.Model):
    """
    币世界 非小号
    币种信息合并表
    """
    name = models.CharField(max_length=255, null=True)    # 全称
    en_name = models.CharField(max_length=255, null=True)  # 英文名称
    cn_name = models.CharField(max_length=255, null=True)  #中文名称
    short_name = models.CharField(max_length=255, null=True)  # 简称
    icon = models.CharField(max_length=255, null=True)  # 币种图标
    introduction = models.TextField(null=True)  # 简介

    quantity = models.CharField(max_length=255, null=True)  # 流通量
    circulation = models.CharField(max_length=255, null=True)  # 发行量

    exchange = models.CharField(max_length=255, null=True)     #交易所
    published_at = models.DateField(null=True)  # 发行时间（日期）
    white_paper = models.CharField(max_length=255, null=True)  #白皮书
    website = models.CharField(max_length=255, null=True)  # 网站 1个
    block_station = models.CharField(max_length=255, null=True)  # 区块站 多个
    related_concepts = models.CharField(max_length=255, null=True)  # 相关概念 多个
    is_token = models.SmallIntegerField(null=True)  # 是否代币
    token_platform = models.CharField(max_length=255, null=True)  # 代币平台
    ico_cost = models.CharField(max_length=255, null=True)  # 众筹价格/ICO成本

    origin_url = models.CharField(max_length=255, null=True)  # 币种链接
    created_at = models.DateTimeField(null=True)  # 爬取时间


class Trade(models.Model):
    data_id = models.IntegerField()
    time = models.CharField(max_length=255, null=True)
    price = models.CharField(max_length=255, null=True)
    amount = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)

class Exchange(models.Model):
    market = models.CharField(max_length=25, null=True)
    symbol = models.CharField(max_length=25, null=True)
    currency = models.CharField(max_length=25, null=True)
    period = models.CharField(max_length=25, null=True)
    open = models.CharField(max_length=25, null=True)
    close = models.CharField(max_length=25, null=True)
    high = models.CharField(max_length=25, null=True)
    low = models.CharField(max_length=25, null=True)
    last = models.CharField(max_length=25, null=True)
    p_change = models.CharField(max_length=25, null=True)
    quoteVolume = models.CharField(max_length=25, null=True)
    baseVolume = models.CharField(max_length=25, null=True)
    updated_at = models.DateTimeField(null=True)



