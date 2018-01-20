# -*- coding: utf-8 -*-
'''
@author:yangyang.ju
伯乐在线Python模块的Spider
'''
import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from items import ArticleItemLoader,LpythonspiderItem
from Util import common
import threading
import leancloud
import logging
from  scrapy_redis.spiders import RedisSpider



class ArticlejobbolespiderSpider(RedisSpider):
    name = 'ArticleJobBoleSpider'
    allowed_domains = ['jobbole.com']
    redis_key = 'LPythonReids:start_urls'
    # start_urls = ['http://python.jobbole.com/all-posts']

    def __init__(self, callbackUrl=None, **kwargs):
        super(ArticlejobbolespiderSpider, self).__init__()
        dispatcher.connect(self.spider_open_receiver, signals.spider_opened)
        dispatcher.connect(self.spider_error_receiver, signals.spider_error)
        dispatcher.connect(self.spider_closed_receiver, signals.spider_closed)

    def spider_open_receiver(self):
        self.logger.info('Notice!! !!!Spider is start')
        #开启多线程去初始化LeanCloudSDK
        init_sdk_thread = threading.Thread(target=self.init_leancloud_sdk,name='init_leancloud_sdk_thread')
        init_sdk_thread.setDaemon(True)
        init_sdk_thread.start()


    def spider_error_receiver(self):
        # TODO:爬虫发生错误时响应，并以邮件的形式通知,这里补充发送邮件的逻辑
        self.logger.info('!!!!!!!!!!!!!!!!!!!!!!!Error!!!!!!!!!!!!!!!!!!!!!')
        pass

    def spider_closed_receiver(self):
        self.logger.info('Notice!! Spider is closed')

    def  init_leancloud_sdk(self):
        leancloud.init("avjbAbAq3Tjsft3OXhDCHPfC-gzGzoHsz", "jGadrhLEJ3nk9r0lPSQaCdLv")
        logging.basicConfig(level=logging.DEBUG)


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

            articleobjectid = common.get_md5(articlelink)
            itemloader.add_value('object_id',articleobjectid)

            yield itemloader.load_item()

        # 单页面解析完成，开始构建下一页的数据
        next_page_link = response.xpath('//div[@class="grid-8"]/div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract_first()

        if next_page_link is None or len(next_page_link) == 0:
            log.logger.info('completed all page request')

        else:
            log.logger.info('will request next page and request url is %s'%next_page_link)
            yield Request(url=next_page_link)


