# -*- coding: utf-8 -*-

import redis
import threading
import time
from scrapy import log

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

class RedisManager(Singleton):
    def __init__(self):
        self.redis_server = redis.Redis(host='172.30.116.191', port=6379)
        if self.redis_server.ping():
            log.logger.info('connect redis-server successful!!!')
        else:
            log.logger.info('connect redis-server fail!!!')

            raise Exception

    def doQuery(self):
        while True:
            keylist = self.redis_server.keys('*')
            for key in keylist:
                print('now redis key is %s'%key)
            time.sleep(10)
    def doPop(self):
        i=0
        while i<1:
           print (self.redis_server.lpop("LPythonSpider:items"))
           i += 1


    def doClear(self):
        self.redis_server.flushall()

        print 'clear all commpleted Bye'

    def doInitPush(self):
        try:
            self.redis_server.lpush('jobbole:starturl', 'http://python.jobbole.com/all-posts')
            print "写入url成功!"
            thread = threading.Thread(target=self.doQuery, args=(), name='thread-redis')
            thread.start()
            thread.join(120)
            print "completed Bye "
        except Exception:
            print "写入失败"

    def doRequestPush(self,key,value):
           if self.redis_server is None:
               log.logger.info('redis-server valid!!!!!')
               return
           list_len = self.redis_server.lpush(key,value)
           log.logger.info(list_len)

if __name__ == '__main__':
    redisManager = RedisManager()
    redisManager.doInitPush()