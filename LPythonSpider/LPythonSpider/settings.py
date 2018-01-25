# -*- coding: utf-8 -*-
import sys
import os
from helper.ConfigHelper import ConfigManager

BOT_NAME = 'LPythonSpider'

SPIDER_MODULES = ['LPythonSpider.spiders']
NEWSPIDER_MODULE = 'LPythonSpider.spiders'

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'LPythonSpider'))
RANDOM_UA_TYPE = "random"
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
   #'LPythonSpider.middlewares.RandomUserAgentMiddlware': 543,
   'LPythonSpider.middlewares.InvalidResponseHandlerMiddleware':400

}
ITEM_PIPELINES = {
   #是否将item刷新至redis
   'scrapy_redis.pipelines.RedisPipeline': 400,
   #'LPythonSpider.pipelines.Lpythonspider_article_jobbole':300
}

EXTENSIONS = {
    'scrapy.exceptions.CloseSpider':500
}
CLOSESPIDER_TIMEOUT = 600

#无效Response重试和收集中间件的配置项
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [404,403,502]
#分布式配置项目
REDIS_HOST = ConfigManager.redis_host
REDIS_PORT = ConfigManager.redis_port
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DUPEFILTER_DEBUG = False
SCHEDULER_FLUSH_ON_START = True
SCHEDULER_IDLE_BEFORE_CLOSE = 30


#自动优化加载速度的优化项
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_DEBUG = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_MAX_DELAY = 60

#日志文件输出配置项目
# local = arrow.now()
# LOG_FILE_NAME = 'Run-log-{0}.log'.format(local.format('YYYY-MM-DD'))
# LOG_FILE = LOG_FILE_NAME
# #为 True，进程所有的标准输出(及错误)将会被重定向到log中(包括Print的输出)
# LOG_STDOUT =True



