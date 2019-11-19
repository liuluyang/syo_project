
import scrapy
from test_scrapy.items import TradingViewItem
from test_scrapy.db import ConnectDB
import time

class CurrencySpider(scrapy.Spider):
    name = 'trading_view'
    allowed_domains = ['cn.tradingview.com']
    url = 'https://cn.tradingview.com/u/{}/'  #用户主页

    group_id = 14
    origin_from = 'TradingView'

    def start_requests(self):
        users_request = ConnectDB().authors_get(14)
        for user in users_request:
            u = user[2]
            yield scrapy.Request(self.url.format(u), callback=self.parse,
                                 meta={'author': u})

    def parse(self, response):
        author = response.meta['author']
        article_list = response.css('div[data-uid]')
        for article in article_list:
            title = article.css('a')[0]
            href = title.css('::attr(href)').extract_first()
            url = response.urljoin(href)  # 正文连接
            if self.redis.sismember('TradingView_idea', url):
                continue

            title_text = title.css('::text').extract_first()    #标题
            img = article.css('img::attr(src)').extract_first() #图片
            desc = article.css('p::text').extract_first()       #描述
            desc = desc.replace('\n', '')
            created_at = article.css(
                '.tv-card-stats__time::attr(data-timestamp)').extract_first()
            created_at = time.strftime('%Y-%m-%d %X',
                                       time.localtime(float(created_at))) #文章创建时间
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())   #爬取时间
            symbol = article.css('.tv-widget-idea__symbol::text').extract_first()
            symbol = symbol.strip() if isinstance(symbol, str) else ''    #交易对
            label = article.css('.tv-card-label *::text').extract()        #标签
            label = label[-1].strip() if label else ''
            # print(title_text, img, created_at, updated_at, url)
            # print(desc)
            # print(symbol, label)
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

            item = TradingViewItem()
            item['origin_url'] = url
            item['thumb'] = img
            item['title'] = title_text
            item['author'] = author
            item['description'] = desc
            item['updated_at'] = updated_at
            item['group_id'] = self.group_id
            item['origin_from'] = self.origin_from
            item['created_at'] = created_at
            item['symbol'] = symbol
            item['label'] = label

            yield scrapy.Request(url, callback=self.content, meta={'item':item})

    def content(self, response):
        item = response.meta['item']
        content_update = response.xpath(
            '//div[@class="tv-chart-updates__description tv-chart-view__description selectable--full"]/text()|'
            '//div[@class="tv-chart-updates__description tv-chart-view__description selectable--full"]/*') \
            .extract()
        content = response.xpath(
            '//div[@class="tv-chart-view__description selectable--full"]/text()|'
            '//div[@class="tv-chart-view__description selectable--full"]/*')\
            .extract()
        content_new = ''
        content = content_update if content_update else content
        for c in content:
            content_new += c.strip()

        item['content'] = content_new

        yield item