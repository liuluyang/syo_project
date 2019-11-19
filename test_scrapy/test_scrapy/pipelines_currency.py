
from test_scrapy.items import Currency


class CurrencyPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if not isinstance(item, Currency):
            return item
        if spider.name in ['bsj_currency', 'bsj_currency_update']:
            self.bsj(item, spider)
        if spider.name == 'fxh_currency':
            self.fxh(item, spider)

        return item

    def bsj(self, item, spider):
        if spider.redis.sismember('currency_name', item['name']):
            if spider.name == 'bsj_currency_update':
                spider.cursor.execute(
                    """update uce_coin set en_name=%s,name=%s,
                        icon=%s, info=%s, circulation=%s, total_supply=%s,
                        published_at=%s, official_site=%s, block_url=%s, 
                        updated_at=%s, ico_cost=%s where full_name=%s""",
                    (
                        #item['name'],  # 对应数据库full_name
                        item['English_name'],
                        item['short_name'],  # 对应数据库name
                        item['icon'],
                        item['introduction'],
                        item['quantity'],
                        item['circulation'],
                        item['published_at'],
                        item['website'],
                        item['block_station'],
                        item['created_at'],
                        item['ico_cost'],
                        item['name'],  # 对应数据库full_name
                    )
                )
                spider.connect.commit()
        else:
            spider.cursor.execute(
                """insert into uce_coin(full_name, en_name, name,
                    icon, info, circulation, total_supply, published_at,
                    official_site, block_url, created_at, ico_cost)
                    value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    item['name'], #对应数据库full_name
                    item['English_name'],
                    item['short_name'],  #对应数据库name
                    item['icon'],
                    item['introduction'],
                    item['quantity'],
                    item['circulation'],
                    item['published_at'],
                    item['website'],
                    item['block_station'],
                    item['created_at'],
                    item['ico_cost'],
                )
            )
            spider.connect.commit()
            spider.redis.sadd('currency_name', item['name'])

    def fxh(self, item, spider):
        if spider.redis.sismember('currency_name', item['name']):
            spider.cursor.execute(
                """update uce_coin set cn_name=%s,
                   white_paper=%s,concepts=%s,is_token=%s,
                   token_platform=%s, updated_at=%s where full_name=%s""",
                (
                    item['chinese_name'],
                    item['white_paper'],
                    item['related_concepts'],
                    item['is_token'],
                    item['token_platform'],
                    item['created_at'],
                    item['name']    # 对应数据库full_name
                )
            )
            spider.connect.commit()