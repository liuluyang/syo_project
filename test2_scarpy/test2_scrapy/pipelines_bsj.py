# -*- coding: utf-8 -*-

from test2_scrapy.items import NewsletterItem

class NewsletterPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        # 关闭数据库连接
        spider.connect.close()
        spider.logger.info('{name}关闭mysql数据库连接'.format(name=spider.name))

    def process_item(self, item, spider):
        if not isinstance(item, NewsletterItem):
            return item
        spider.cursor.execute(
            """insert into information_newsletter(group_id, origin_url, origin_from, is_red, title, thumb,
                            description, content, created_at, updated_at, is_more, to_url)
                        value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                item['group_id'],
                item['origin_url'],
                item['origin_from'],
                item['is_red'],
                item['title'],
                item['thumb'],
                item['description'],
                item['content'],
                item['created_at'],
                item['updated_at'],
                item['is_more'],
                item['to_url']
            )
        )
        spider.connect.commit()
        # 把已抓取的数据链接添加到redis去重队列
        spider.redis.sadd('newsletter_urls', item['origin_url'])

        return item
