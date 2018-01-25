# -*- coding: utf-8 -*-

from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute('scrapy crawl LPythonSpider'.split())
    # 测试无效Response的重试与记录机制
    #cmdline.execute('scrapy crawl dmoz'.split())