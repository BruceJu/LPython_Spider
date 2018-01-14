# -*- coding: utf-8 -*-
'''
@author:yangyang.ju
伯乐在线Python模块的Spider
'''
import scrapy
from scrapy import log
from scrapy.http import Request
from items import ArticleItemLoader,LpythonspiderItem


class ArticlejobbolespiderSpider(scrapy.Spider):
    name = 'ArticleJobBoleSpider'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts']

    def parse(self, response):
        if response.status != 200 or len(response.text) == 0:
            log.logger.error('Current response is invalid')
            return

        #解析当前响应数据的标题


        ArticlePage = response.xpath('//div[@class="grid-8"]/div[@class="post floated-thumb"]')
        if ArticlePage is not None:
            log.logger.info('Current artticle list len is {0} and type is {1}'.format(len(ArticlePage),type(ArticlePage)))

        #解析
        for Article in ArticlePage:
            itemloader = ArticleItemLoader(response=response, item=LpythonspiderItem())

            articlethumb = Article.xpath('./div[@class="post-thumb"]/a/img/@src').extract()
            itemloader.add_value('thumb',articlethumb)

            articletitle = Article.xpath('./div[@class="post-meta"]/p/a[@class="archive-title"]/text()').extract()
            itemloader.add_value('title', articletitle)

            articledate = Article.xpath('./div[@class="post-meta"]/p/text()').extract()
            itemloader.add_value('date',articledate)

            articletype = Article.xpath('./div[@class="post-meta"]/p/a[@rel="category tag"]/text()').extract()
            itemloader.add_value('type',articletype)

            articlesummary = Article.xpath('./div[@class="post-meta"]/span[@class="excerpt"]/p/text()').extract()
            itemloader.add_value('summary',articlesummary)

            articlelink = Article.xpath('./div[@class="post-meta"]/p/a[@class="archive-title"]/@href').extract()
            itemloader.add_value('link', articlelink)

            yield itemloader.load_item()

        # 单页面解析完成，开始构建下一页的数据
        next_page_link = response.xpath('//div[@class="grid-8"]/div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract_first()

        if next_page_link is None or len(next_page_link) == 0:
            log.logger.info('completed all page request')

        else:
            log.logger.info('will request next page and request url is %s'%next_page_link)
            yield Request(url=next_page_link)


