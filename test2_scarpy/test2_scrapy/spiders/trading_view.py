
import scrapy
#from test2_scrapy.items import Currency_fxh
import time

class CurrencySpider(scrapy.Spider):
    name = 'trading_view'
    allowed_domains = ['cn.tradingview.com']
    url = 'https://cn.tradingview.com/u/{}/'  #用户主页

    def start_requests(self):
        u = 'TouFrancis'
        yield scrapy.Request(self.url.format(u), callback=self.parse)

    def parse(self, response):
        article_list = response.css('div[data-uid]')
        for article in article_list[:2]:
            title = article.css('a')[0]
            href = title.css('::attr(href)').extract_first()
            title_text = title.css('::text').extract_first()    #标题
            img = article.css('img::attr(src)').extract_first() #图片
            desc = article.css('p::text').extract_first()       #描述
            desc = desc.replace('\n', '')
            # created_at = response.xpath(
            #     '//span[@class="tv-card-stats__time js-time-upd"]/@data-timestamp').extract_first()
            #print(response.css('.tv-card-stats__time::attr(data-timestamp)'))
            created_at = article.css('.tv-card-stats__time::attr(data-timestamp)').extract_first()
            created_at = time.strftime('%Y-%m-%d %X',
                                       time.localtime(float(created_at))) #文章创建时间
            updated_at = time.strftime('%Y-%m-%d %X', time.localtime())   #爬取时间
            url = response.urljoin(href)    #正文连接
            #url = 'https://cn.tradingview.com/chart/BTCUSD/Mfqg6ocu/'
            print(title_text, img, created_at, updated_at, url)
            #print(desc)
            #yield scrapy.Request(url, callback=self.content)

    def content(self, response):
        #tv-chart-updates__description tv-chart-view__description selectable--full
        content_update = response.xpath(
            '//div[@class="tv-chart-updates__description tv-chart-view__description selectable--full"]/text()|'
            '//div[@class="tv-chart-updates__description tv-chart-view__description selectable--full"]/*')\
            .extract()
        print(content_update)

        content = response.xpath(
            '//div[@class="tv-chart-view__description selectable--full"]/text()|'
            '//div[@class="tv-chart-view__description selectable--full"]/*')\
            .extract()
        print(content)
        content_new = ''
        # for c in content:
        #     content_new += c.strip()
        # print(content_new)