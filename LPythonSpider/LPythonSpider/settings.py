# -*- coding: utf-8 -*-

# Scrapy settings for LPythonSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import sys
import os
from config import spiderConfig
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
   #'LPythonSpider.middlewares.LpythonspiderDownloaderMiddleware': 543,
   'LPythonSpider.middlewares.RandomUserAgentMiddlware': 543,

}
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DUPEFILTER_DEBUG = False
ITEM_PIPELINES = {
   #是否将item刷新至redis
   'scrapy_redis.pipelines.RedisPipeline': 400,
   'LPythonSpider.pipelines.Lpythonspider_article_jobbole':300
}

REDIS_HOST = spiderConfig.redis_host
REDIS_PORT = spiderConfig.redis_port
AUTOTHROTTLE_START_DELAY = 5
SCHEDULER_FLUSH_ON_START = True
AUTOTHROTTLE_DEBUG = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_MAX_DELAY = 60
SCHEDULER_IDLE_BEFORE_CLOSE = 30
LOG_FILE='Spiderun.log'

