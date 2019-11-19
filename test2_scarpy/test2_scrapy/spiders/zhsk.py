import scrapy
import time
import requests

class CurrencySpider(scrapy.Spider):
    name = 'zhsk'
    allowed_domains = ['zhsk.12348.gov.cn']
    url = 'http://zhsk.12348.gov.cn/qa.web/'

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        text = response.text
        print(response, text)
        maintxt = response.css('div.wrapper .maintxt a')
        print(maintxt)
        for a in maintxt[:]:
            href = a.css('::attr(href)').extract_first()
            href = response.urljoin(href)
            title = a.css('::text').extract_first()
            cls = href.split('cls=')[-1]
            print(href, title, cls)

            self.question_get(cls, title)
            time.sleep(0.5)

    def question_get(self, cls, title):
        #cls = 2
        base_url = "http://zhsk.12348.gov.cn/qa.web/query/detail?id="
        data = {
            'rid':'1/{}'.format(cls),
            'pagesize':1000,
            'pageindex':1
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        q_list = requests.post('http://zhsk.12348.gov.cn/qa.web/query/GetLb',
                               data, headers=headers).json()
        print(q_list)
        name = title
        with open(name, 'w+') as f:
            for q in q_list['list']:
                print(q['id'])
                f.write(base_url+ q['id'] + '\n')