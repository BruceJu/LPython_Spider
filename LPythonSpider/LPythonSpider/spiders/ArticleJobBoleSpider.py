# -*- coding: utf-8 -*-
import scrapy


class ArticlejobbolespiderSpider(scrapy.Spider):
    name = 'ArticleJobBoleSpider'
    allowed_domains = ['http://python.jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        pass
