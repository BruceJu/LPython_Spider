# -*- coding: utf-8 -*-

from celery import Celery
from scrapy import cmdline
from RedisHelper import redisManager

app = Celery('start_spider')

app.config_from_object('task_config')

@app.task
def start_spider(arg,args):
    print 'start_spider %d'%arg
    cmdline.execute('scrapy crawl LPythonSpider'.split())
    pass

@app.task
def push_url_to_redis(arg,args):
    print 'push_url_to_redis %d'%arg
    redisManager.doInitPush()
    pass