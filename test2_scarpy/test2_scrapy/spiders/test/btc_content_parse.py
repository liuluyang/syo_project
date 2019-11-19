


import scrapy
from scrapy.selector import Selector


class BtcSpider(scrapy.Spider):
    name = 'btc_content'
    allowed_domains = ['8btc.com']
    start_urls = ['http://www.8btc.com/indian-crypto-regulation-september-2']

    need_UserAgent = True

    def parse(self, response):
        content = response.xpath('//article[@class="single-article clearfix"]/'
                                 'div[@class="article-content"]/*').extract()

        #content = response.css('.article-content p').extract()

        #print (len(content))
        print (content)
        for num,i in enumerate(content):
            print (self.delete_img_attr(i))
            #print (num,i)

    def delete_img_attr(self, tag):
        check = ['content-bottom','ad akp-adv','content-source-info']

        text = Selector(text=tag)
        if text.css('::attr(class)').extract_first() in check:
            return '~~~~~~~~~~~~~~~~~~~~'

        if text.css('img'):
            print ('replace starting ....')
            class_value = text.css('img::attr(class)').extract()
            width = text.css('img::attr(width)').extract()
            height = text.css('img::attr(height)').extract()
            for c in class_value:
                tag = tag.replace('class="'+c+'"', "")
            for w in width:
                tag = tag.replace('width="'+w+'"', "")
            for h in height:
                tag = tag.replace('height="'+h+'"', "")

        return tag


# s = '<h2><a href="http://cdn.8btc.com/wp-content/uploads/2018/07/201807240318267820.png">' \
#     '<img class="size-full wp-image-240193 aligncenter" ' \
#     'alt="indian-bull-1068x1068" ' \
#     'src="http://cdn.8btc.com/wp-content/uploads/2018/07/201807240318267820.png" ' \
#     'width="534" height="534"></a></h2>'
#
# print (s.replace('class="size-full wp-image-240193 aligncenter"', '|'))
