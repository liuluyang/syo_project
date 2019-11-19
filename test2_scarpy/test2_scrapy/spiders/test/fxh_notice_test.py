
import scrapy


class ContentSpider(scrapy.Spider):

    name = 'fxh_content'
    allowed_domains = ['feixiaohao.com']

    start_urls = ['https://www.feixiaohao.com/notice/3600022.html']

    def parse(self, response):
        #正常情况 当前节点下不含<br>标签
        content = response.xpath('//div[@class="artBox article"]/*').extract()[2:]

        content = response.xpath('//div[@class="artBox article"]/node()').extract()[5:]
        s = ''
        for n,i in enumerate(content):
            #print ('<br>' in i)
            # if i:
            print (n,i)
            #s+=i.strip()

        #print (''.join(content))
        #print (s)
