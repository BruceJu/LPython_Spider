# -*- coding: utf-8 -*-

import threading
import leancloud

'''
leancloud 后端云操作类
'''

class CloudServerManager:
    def __init__(self):
        print('*' * 10 + 'prepare CloudServerHelper init' + '*' * 10)
        init_sdk_thread = threading.Thread(target=self.init_leancloud_sdk, name='init_leancloud_sdk_thread')
        init_sdk_thread.setDaemon(True)
        init_sdk_thread.start()

    def init_leancloud_sdk(self):
        print('*' * 10 + 'CloudServerHelper init success!!!' + '*' * 10)
        leancloud.init("avjbAbAq3Tjsft3OXhDCHPfC-gzGzoHsz", "jGadrhLEJ3nk9r0lPSQaCdLv")


CloudServerManager = CloudServerManager()