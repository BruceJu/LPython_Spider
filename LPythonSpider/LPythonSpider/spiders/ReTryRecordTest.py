# -*- coding: utf-8 -*-

"""
用于测试请求无效重试机制和记录机制的有效性。
http://www.dmoz.org/网站目前会返回 403
"""
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class ReTryRecordTestSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    allowed_domains = ['dmoz.org']
    start_urls = ['http://www.dmoz.org/']

    rules = [
        Rule(LinkExtractor(
            restrict_css=('.top-cat', '.sub-cat', '.cat-item')
        ), callback='parse_directory', follow=True),
    ]

    def __init__(self, callbackUrl=None, **kwargs):
        super(ReTryRecordTestSpider, self).__init__()
        dispatcher.connect(self.spider_open_receiver, signals.spider_opened)


    def spider_open_receiver(self):
        self.logger.info('Notice!! !!!Spider is start')
        settings = self.settings

    def parse_directory(self, response):
        settings = self.settings
        for div in response.css('.title-and-desc'):
            yield {
                'name': div.css('.site-title::text').extract_first(),
                'description': div.css('.site-descr::text').extract_first().strip(),
                'link': div.css('a::attr(href)').extract_first(),
            }
