# -*- coding: utf-8 -*-
import copy
import time
import urllib

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import HotspotCrawlerItem, HotspotCrawlerItemLoader


class XinhuaHotspotSpider(CrawlSpider):
    name = 'XinhuaHotspot'
    allowed_domains = ['xinhuanet.com']
    start_urls = ['http://www.xinhuanet.com/', "https://www.xinhuanet.com/", ]

    now_yearmonth = time.strftime("%Y-%m", time.localtime())
    now_day = time.strftime("%d", time.localtime())
    reg = r"https?://www\.xinhuanet\.com/\w+/{ym}/{day}/c_\d+"
    reg = reg.replace("{ym}", now_yearmonth).replace("{day}", now_day)
    rules = (
        Rule(LinkExtractor(allow=reg, deny=(
            r"https?://www\.xinhuanet\.com/english/\S+",
            r"https?://www\.xinhuanet\.com/photo/\S+",
            r"https?://www\.xinhuanet\.com/video/\S+")),
             follow=True, callback='parse_items_xinhua'),
    )
    custom_settings = {
        'ITEM_PIPELINES': {'hotspot_crawler.pipelines.XinhuaHotspotPipeline': 301}
    }

    def parse_items_xinhua(self, response):
        self.logger.info("parsing url %s" % response.url)
        global request_more
        if response.meta.get('item') is None:
            item_loader = HotspotCrawlerItemLoader(item=HotspotCrawlerItem(), response=response)
            request_more = True
        else:
            item_loader = response.meta['item']
            self.logger.info(item_loader.get_collected_values)
            request_more = False
        try:
            import re
            if not item_loader.get_collected_values("title"):
                item_loader.add_css("title", ".share-title::text")
            keywords = list(
                set(response.css('meta[name="keywords"]::attr(content)').extract_first().strip().split(','))) or []
            item_loader.add_value("keywords", keywords)
            item_loader.add_css("publish_time", '.h-time::text')
            item_loader.add_value("content_url", response.url)
            item_loader.add_css("abstract", 'meta[name="description"]::attr(content)')
            content = response.css('#p-detail>p').extract() or response.css(
                '#content>p::text, #content>p>span::text').extract()
            item_loader.add_value("content", self.deal_with_content(''.join(content)))
            more_pages = response.css('#div_currpage>a::attr(href)').extract()
            if more_pages and not request_more:
                # 先去重
                temp = list(set(more_pages))
                temp.sort(key=more_pages.index)
                for url in temp:
                    print("more pages,continue parsing")
                    yield scrapy.Request(
                        url=url, callback=self.parse_items_xinhua,
                        meta=copy.deepcopy({'item': item_loader.load_item()})
                    )
            yield item_loader.load_item()
        except Exception as e:
            self.logger.critical(msg=e)
            return None

    def deal_with_content(self, repl_text):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(repl_text, "lxml")
        contents = soup.find_all('p')
        return ''.join(i.string for i in contents if i.string) or ""
