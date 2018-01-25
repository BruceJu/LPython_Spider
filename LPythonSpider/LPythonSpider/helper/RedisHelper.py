# -*- coding: utf-8 -*-

import redis
import threading
import time
from ConfigHelper import ConfigManager
import logging
logger = logging.getLogger(__name__)

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

class RedisManager(Singleton):
    def __init__(self):
        print('*'*30+'Redis Helper init'+'*'*30)
        self.config = ConfigManager
        self.redis_server = redis.Redis(host=self.config.redis_host, port=self.config.redis_port)
        if self.redis_server.ping():
            logger.info('connect redis-server successful!!!')
        else:
            logger.info('connect redis-server fail!!!')

            raise Exception

    def doGetServer(self):
        if self.redis_server is not None and self.redis_server.ping():
            return self.redis_server
        else:
            return None

    def doInitPush(self):
        try:
            self.redis_server.lpush(self.config.jobbole_redis_key, self.config.jobbole_push_url)
            print "写入url成功!"
            thread = threading.Thread(target=self.doQuery, args=(), name='thread-redis')
            thread.start()
            thread.join(120)
            print "completed Bye "
        except Exception:
            print "写入失败"

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


    def doRequestPush(self,key,value):
           if self.redis_server is None:
               logger.info('redis-server valid!!!!!')
               return
           list_len = self.redis_server.lpush(key,value)
           logger.info(list_len)

redisManager = RedisManager()

if __name__ == '__main__':
    RedisManager = RedisManager()
    RedisManager.doInitPush()