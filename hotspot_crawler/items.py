# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity


class HotspotCrawlerItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    @classmethod
    def remove_spaces_and_comments(cls, repl_text):
        import re
        repl_text = re.sub(r'\s+', repl="", string=repl_text)
        repl_text = re.sub(r'\u3000', repl="", string=repl_text)
        return re.sub(r'<!--\S+-->', repl="", string=repl_text)


class HotspotCrawlerItem(Item):
    # 新闻标题
    title = Field(input_processor=MapCompose(HotspotCrawlerItemLoader.remove_spaces_and_comments))
    # 发布日期
    publish_time = Field()
    # 关键词
    keywords = Field(output_processor=Identity(), )
    # 新闻内容详情网址
    content_url = Field()
    # 新闻内容详情
    content = Field(serializer=str, input_processor=MapCompose(HotspotCrawlerItemLoader.remove_spaces_and_comments))
    # 新闻摘要
    abstract = Field(serializer=str, input_processor=MapCompose(HotspotCrawlerItemLoader.remove_spaces_and_comments))
