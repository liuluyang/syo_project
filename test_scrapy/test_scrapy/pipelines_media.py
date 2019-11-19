from test_scrapy.items import Media_weibo


class MediaPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        if spider.name=='media_update':
            spider.logger.info('共{update_num}条微博视频链接，成功更新'
                               '{success_num}条。。。'.format(update_num=spider.
                                update_num, success_num=spider.success_num))

    def process_item(self, item, spider):
        if not isinstance(item, Media_weibo):
            return item
        spider.cursor.execute(
            """
            update uce_spider_guanzhu set media_url=%s where id=%s
            """,
            (
                item['media_url'],
                item['id'],
            )
        )
        spider.connect.commit()
        spider.success_num += 1

        return item
