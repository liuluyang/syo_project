#coding:utf8


import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from scrapy.selector import Selector

class PolicySpider(scrapy.Spider):
    name = 'btc_test'
    allowed_domains = ['8btc.com']
    url = 'https://www.8btc.com/news?cat_id=572'
    need_UserAgent = True

    group_id = 6
    origin_from = '巴比特'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome('D:\liuluyang\chromedriver_win32\chromedriver')
        #self.browser.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.driver, 10)

    def start_requests(self):

        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        # 打开页面后，滑动至页面底部
        self.scroll_until_loaded()
        # with open('btc.html', 'wb') as b:
        #     b.write(response.body)
        pass

    def closed(self, spider):
        print("spider closed")
        #self.browser.close()

    def scroll_until_loaded(self):
        check_height = self.driver.execute_script(
            "return document.body.scrollHeight;")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(
                    lambda driver: self.driver.execute_script(
                        "return document.body.scrollHeight;") > check_height)
                check_height = self.driver.execute_script(
                    "return document.body.scrollHeight;")
            except:
                print ('timeout~~~~~~~~~~~~~~~~~')
                break