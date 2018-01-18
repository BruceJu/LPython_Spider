# -*- coding: utf-8 -*-

import requests
import json
import hashlib
import requests
import json
import random


def get_md5(url):
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    m = hashlib.md5(url)
    m.update(url)
    return m.hexdigest()

def QueryRandomIP():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=20&country=国内')
    ip_ports = json.loads(r.text)
    index = random.randint(0, len(ip_ports) - 1)
    ip = ip_ports[index][0]
    port = ip_ports[index][1]
    proxies = {
        'http': 'http://%s:%s' % (ip, port),
        'https': 'http://%s:%s' % (ip, port)
    }
    return proxies
