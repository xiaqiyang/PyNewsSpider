# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import HotspotCrawlerItem, HotspotCrawlerItemLoader


class FengHuangHotspotSpider(CrawlSpider):
    name = 'FengHuangHotspot'
    allowed_domains = ['ifeng.com']
    start_urls = ['http://news.ifeng.com/', 'https://news.ifeng.com/']

    rules = (
        Rule(LinkExtractor(allow=r"^https?://news\.ifeng\.com/c/\w+$",
                           restrict_css=(".content-14uJp0dk", ".aside-2XIR61CP")), follow=False,
             callback='parse_items_fenghuang'),
    )
    custom_settings = {
        'ITEM_PIPELINES': {'hotspot_crawler.pipelines.FengHuangHotspotPipeline': 302}
    }

    def parse_items_fenghuang(self, response):
        self.logger.info("parsing url %s" % response.url)
        item_loader = HotspotCrawlerItemLoader(item=HotspotCrawlerItem(), response=response)
        try:
            keywords = list(
                set(response.css('meta[name="keywords"]::attr(content)').extract_first().split(' ')))
            item_loader.add_value("keywords", keywords)
            metadatas = self.get_metadatas(response)
            item_loader.add_css("publish_time", 'meta[name="og:ti me "]::attr(content)')
            if not item_loader.get_collected_values("publish_time"):
                item_loader.add_value("publish_time", metadatas.get('publish_time'))
            item_loader.add_value("title", metadatas.get("title") or "")
            item_loader.add_value("content_url", metadatas.get("content_url") or response.url)
            item_loader.add_value("content", metadatas.get("content") or "")
            item_loader.add_value("abstract",
                                  metadatas.get("content") if len(metadatas.get("content")) < 100 else metadatas.get(
                                      "content")[:100] or "")
            yield item_loader.load_item()
        except Exception as e:
            self.logger.critical(msg=e)
            return None

    def get_metadatas(self, response):
        import re, json
        data_from = ""
        for each in response.css('head>script').extract():
            if "var allData" and "\"nav\"" in each:
                data_from = each
                break
        match = re.search(r"var\sadData\s=\s.+", data_from)
        if match:
            data_from = data_from[:match.start()]
            c = json.loads(data_from.lstrip("<script>").strip().lstrip("var allData = ").rstrip(";"), encoding='utf-8')
            base_data = c.get('docData')
            slide_data = c.get('slideData')
            if base_data or slide_data:
                content = ""
                publish_time = base_data.get('newsTime')
                title = base_data.get('title') or ""
                content_url = base_data.get('pcUrl') or response.url
                if "contentData" in base_data and base_data.get('contentData'):
                    for each in base_data['contentData']['contentList']:
                        if each.get('type') == 'text':
                            content = each['data'] or ""
                        else:
                            self.logger.info(each.get('type'))
                    content = self.deal_with_content(content)
                else:
                    content_list = []
                    content_list = list(set(content_list))
                    content = '\n'.join(content_list) or ""
                return {
                    "title": title or "",
                    "content_url": content_url or "",
                    "publish_time": publish_time or "",
                    "content": content or ""
                }
        return {}


    def deal_with_content(self, repl_text):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(repl_text, "lxml")
        return '\n'.join(string for string in soup.stripped_strings) or ""
