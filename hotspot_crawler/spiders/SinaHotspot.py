# -*- coding: utf-8 -*-
import datetime
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import HotspotCrawlerItem, HotspotCrawlerItemLoader


class SinaHotspotSpider(CrawlSpider):
    name = 'SinaHotspot'
    allowed_domains = ['sina.com.cn', 'sina.com']
    start_urls = ['https://news.sina.com.cn/', ]
    reg = r"http(s)?://(\w+\.)?news.sina.com.cn/\w+/time/\w+-\w+\.(s)?html"
    t = time.localtime()
    now_time = time.strftime("%Y-%m-%d", t)
    reg = reg.replace("time", now_time)
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_time = yesterday.strftime("%Y-%m-%d")
    reg2 = reg.replace("time", yesterday_time)
    rules = (
        Rule(LinkExtractor(
            allow=reg),
            callback='parse_sina_news', follow=True),
        Rule(LinkExtractor(
            allow=reg2),
            callback='parse_sina_news', follow=True),
    )
    custom_settings = {
        'ITEM_PIPELINES': {'hotspot_crawler.pipelines.SinaHotspotPipeline': 300}
    }


    def parse_sina_news(self, response):
        self.logger.info("parsing url %s" % response.url)
        # URL示例：https://news.sina.com.cn/s/2019-07-05/doc-ihytcerm1571229.shtml
        # start parsing #
        item_loader = HotspotCrawlerItemLoader(item=HotspotCrawlerItem(), response=response)
        try:
            item_loader.add_css("title", '.main-title::text') or ""
            item_loader.add_css("publish_time", '.date-source>span::text') or ""
            keywords = response.css('meta[name="keywords"]::attr(content)').extract_first().split(',')
            item_loader.add_value("keywords", list(set(keywords)))
            item_loader.add_css("content_url", 'meta[property="og:url"]::attr(content)') or response.url
            content_list = response.css('.article>p::text').extract()
            content = self.remove_spaces_and_comments('\n'.join(content_list))
            item_loader.add_value("content", content)
            item_loader.add_css("abstract", 'meta[name="description"]::attr(content)')
            if not item_loader.get_collected_values("abstract"):
                # print("no abstract available")
                item_loader.add_value("abstract", content[:100] if len(content) > 100 else content)
            yield item_loader.load_item()
        except Exception as e:
            self.logger.critical(msg=e)
            return None


    def remove_spaces_and_comments(self, repl_text):
        import re
        repl_text = re.sub(r'\s+', repl="", string=repl_text)
        repl_text = re.sub(r'\u3000', repl="", string=repl_text)
        return re.sub(r'<!--\S+-->', repl="", string=repl_text)
