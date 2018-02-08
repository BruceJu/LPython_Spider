# -*- coding: utf-8 -*-
'''
@author:yangyang.ju
伯乐在线Python模块的Spider
'''
import logging

from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider

from Util import common
# 这里不要删除，否则leancloud无法初始化
from helper.CloudServerHelper import ConfigManager
from helper.ConfigHelper import ConfigManager
from items import ArticleItemLoader, LpythonspiderItem

logger = logging.getLogger(__name__)


class ArticlejobbolespiderSpider(RedisSpider):
    name = 'LPythonSpider'
    already_push_all_request = False
    redis_key = ConfigManager.jobbole_redis_key

    # Fix:问题1.路径应用方式和编码不同导致的，在不同平台上无法运行的bug

    # Fix:问题2.爬取过程中，由于代理IP的无效导致的404爬取页面的收集

    # Fix:问题3.由于有些页面没有封面封会导致，进入管道时，数据无法正常使用入库的问题

    # Fix:问题4.爬取完成后，如何关闭爬虫

    # Fix:问题5 爬虫发生错误时响应，并以邮件的形式通知,这里补充发送邮件的逻辑

    # TODO:问题6 如何避免每次启动重复爬取

    # TODO:问题7 服务化

    def __init__(self, callbackUrl=None, **kwargs):
        super(ArticlejobbolespiderSpider, self).__init__()

    def parse(self, response):
        if response.status != 200 or len(response.text) == 0:
            logger.error('Current response is invalid')
            return
        # 解析当前响应数据的标题
        ArticlePage = response.xpath('//div[@class="grid-8"]/div[@class="post floated-thumb"]')

        if ArticlePage is not None:
            logger.info('Current artticle list len is {0} and type is {1}'.format(len(ArticlePage), type(ArticlePage)))

        # 解析
        for Article in ArticlePage:
            itemloader = ArticleItemLoader(response=response, item=LpythonspiderItem())

            articlethumb = Article.xpath('./div[@class="post-thumb"]/a/img/@src').extract()
            if articlethumb is None:
                logger.info('cur article no cover')
                itemloader.add_value('thumb', 'No cover')
            else:
                itemloader.add_value('thumb', articlethumb)
            articletitle = Article.xpath('./div[@class="post-meta"]/p/a[@class="archive-title"]/text()').extract()
            itemloader.add_value('title', articletitle)

            articledate = Article.xpath('./div[@class="post-meta"]/p/text()').extract()
            itemloader.add_value('date', articledate)

            articletype = Article.xpath('./div[@class="post-meta"]/p/a[@rel="category tag"]/text()').extract()
            itemloader.add_value('type', articletype)

            articlesummary = Article.xpath('./div[@class="post-meta"]/span[@class="excerpt"]/p/text()').extract()
            itemloader.add_value('summary', articlesummary)

            articlelink = Article.xpath('./div[@class="post-meta"]/p/a[@class="archive-title"]/@href').extract()
            itemloader.add_value('link', articlelink)

            articleobjectid = common.get_md5(articlelink)
            itemloader.add_value('object_id', articleobjectid)
            yield itemloader.load_item()

        if self.already_push_all_request is not True:
            page_list_html_a = response.xpath(
                '//div[@class="grid-8"]/div[@class="navigation margin-20"]/a[@class="page-numbers"]')
            last_page_list_html_a = page_list_html_a[-1]
            last_page_index = last_page_list_html_a.xpath('text()').extract_first()
            print(type(last_page_index))
            last_index_number = int(last_page_index)
            print last_index_number
            format_url = 'http://python.jobbole.com/all-posts/page/{0}/'
            next_page_index = 2
            while next_page_index <= last_index_number:
                next_page_request_url = format_url.format(next_page_index)
                print(' will lpush to redis and url is %s' % next_page_request_url)
                yield Request(url=next_page_request_url)
                next_page_index += 1
            self.already_push_all_request = True
