# -*- coding: utf-8 -*-

import requests
import json

class ProxiesHelper():
    @classmethod
    def queryIP(cls):
        r = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=国内')
        ip_ports = json.loads(r.text)
        print ip_ports
        ip = ip_ports[0][0]
        port = ip_ports[0][1]
        proxies = {
            'http': 'http://%s:%s' % (ip, port),
            'https': 'http://%s:%s' % (ip, port)
        }
        return proxies