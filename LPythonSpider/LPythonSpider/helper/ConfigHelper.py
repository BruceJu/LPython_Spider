# -*- coding: utf-8 -*-

'''
配置文件操作类，用于读取更新配置文件信息
TODO:这里的跟新是在进程中暂时更新，后续应该将更改记录在文件中
TODO:每添加一个新的配置项。都要手动去添加一组方法，或许可以换个方式来实现
'''
import codecs
import json
import os


class ConfigManager:

    def __init__(self):
        print('*'*10+'ConfigManager init'+'*'*10)
        try:
            self._BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
            self._CONFIG_FILE = os.path.join(self._BASE_DIR, 'config.json')
            self._config_file = codecs.open(self._CONFIG_FILE, 'rb', 'utf-8')
            self._configjson = json.load(self._config_file,'uft-8')
            self._redis_host = self._configjson['redis_host']
            self._redis_port = self._configjson['redis_port']
            self._jobbole_redis_key = self._configjson['jobbole_redis_key']
            self._jobbole_push_url = self._configjson['jobbole_push_url']
            self._leancloud_key = self._configjson['leancloud_key']
            self._leancloud_secret = self._configjson['leancloud_secret']
        finally:
            print('*' * 10 + 'read config success!!! prepare close config file' + '*' * 10)
            self._config_file.close()

    @property
    def redis_host(self):
        return self._redis_host

    @redis_host.setter
    def change_default_redis_host(self,value):
        self._redis_host = value

    @property
    def redis_port(self):
        return self._redis_port

    @redis_port.setter
    def change_defaule_redis_port(self,value):
        self._redis_port = value

    @property
    def jobbole_redis_key(self):
        return self._jobbole_redis_key

    @jobbole_redis_key.setter
    def change_default_jobbole_redis_key(self,value):
        self._jobbole_redis_key = value

    @property
    def leancloud_secret(self):
       return self._leancloud_secret

    @leancloud_secret.setter
    def change_defaule_leancloud_key(self,value):
        self._leancloud_secret = value

    @property
    def leancloud_key(self):
        return self._leancloud_key

    @leancloud_key.setter
    def change_defaule_leancloud_key(self, value):
        self._leancloud_key = value

    @property
    def jobbole_push_url(self):
        return self._jobbole_push_url

    @jobbole_push_url.setter
    def change_default_jobbole_push_url(self,value):
        self._jobbole_push_url = value



ConfigManager = ConfigManager()

