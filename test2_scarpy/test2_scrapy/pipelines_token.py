
from test2_scrapy.items import EthToken

class EthTokenPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not isinstance(item, EthToken):
            return item
        spider.cursor.execute(
            """insert into uce_token(name, en_name, description, token, 
                      addresses, decimal_point, num)
                      value (%s, %s, %s, %s, %s, %s, %s)""",
            (
                item['name'],
                item['en_name'],
                item['desc'],
                item['token'],
                item['addresses'],
                item['decimal_point'],
                item['num']
            )
        )
        spider.connect.commit()

        return item
