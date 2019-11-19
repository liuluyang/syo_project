from scrapy.commands import ScrapyCommand
from test_scrapy.settings import SPIDER_NAME_LIST


class Command(ScrapyCommand):
    requires_project = True
    spider_name_list = SPIDER_NAME_LIST

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        spider_list = self.crawler_process.spider_loader.list()
        for name in spider_list:
            if name in self.spider_name_list:
                self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()