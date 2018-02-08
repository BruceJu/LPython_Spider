# -*- coding: utf-8 -*-
from flask_script import Manager, prompt_bool
from scrapy import cmdline

from WebServer.WebService import app
from helper.RedisHelper import redisManager

manager = Manager(app)


@manager.option('-h', '--host', dest='host', default='127.0.0.1')
@manager.option('-p', '--port', dest='port', default=5000)
def runserver(host, port):
    '''
    启动web服务
    :param host:主机
    :param port: 端口
    :return:
    '''
    app.run(host, port)


@manager.command
def spider_list():
    '''
    输出可用爬虫列表
    :return:
    '''
    cmdline.execute('scrapy list'.split())


@manager.option('-n', '--name', dest='name', default='default')
def start_spider(name):
    '''
    启动爬虫
    :param name:爬虫名字，可通过 spider_list获取所有爬虫的名字
    :return:
    '''
    if prompt_bool("Are you sure you want to start spider %s" % name):
        crawl_script = 'scrapy crawl {0}'.format(name)
        cmdline.execute(crawl_script.split())
        # runner = CrawlerRunner()
        # d = runner.crawl(ArticleJobBoleSpider)
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()  # the script will block here until the crawling is finished
    else:
        print 'bye!!'


@manager.command
def redis_push_init():
    '''
    初始化redis并push第一个url
    :return:
    '''
    redisManager.doInitPush()


if __name__ == '__main__':
    manager.run()
    # cmdline.execute('scrapy crawl LPythonSpider'.split())
    # 测试无效Response的重试与记录机制
    # cmdline.execute('scrapy crawl dmoz'.split())
