# -*- coding: utf-8 -*-

import codecs
import json
import os

class ConfigManager:

    def __init__(self):
        print('*'*10+'ConfigManager init'+'*'*10)
        try:
            self.BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
            self.CONFIG_FILE = os.path.join(self.BASE_DIR, 'config.json')
            self.config_file = codecs.open(self.CONFIG_FILE, 'rb', 'utf-8')
            configjson = json.load(self.config_file,'uft-8')
            self._redis_host = configjson['redis_host']
            self._redis_port = configjson['redis_port']
            self._jobbole_redis_key = configjson['jobbole_redis_key']
            self._jobbole_push_url = configjson['jobbole_push_url']
        finally:
            print('*' * 10 + 'read config success!!! prepare close config file' + '*' * 10)
            self.config_file.close()

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
    def jobbole_push_url(self):
        return self._jobbole_push_url

    @jobbole_push_url.setter
    def change_default_jobbole_push_url(self,value):
        self._jobbole_push_url = value


ConfigManager = ConfigManager()

