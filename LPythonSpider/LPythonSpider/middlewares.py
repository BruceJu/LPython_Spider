# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


import codecs
import os
import json
from scrapy import signals
import logging
from fake_useragent import UserAgent
from Util.common import QueryRandomIP
from config import spiderConfig
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed

from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.utils.python import global_object_name


logger = logging.getLogger(__name__)


class RandomUserAgentMiddlware(object):
    #随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.host = 'http://{0}:8000/?types=0&count=20&country=国内'
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        randomua = get_ua()
        request.headers.setdefault('User-Agent', randomua)
        proxy_host = spiderConfig.redis_host
        request_proxy_url = self.host.format(proxy_host)
        proxy = QueryRandomIP(request_proxy_url)
        print 'random ip is %s' % proxy['http']
        print 'random ua is %s' % randomua
        request.meta['proxy'] = proxy['http']


class InvalidResponseHandlerMiddleware(object):

    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)

    def __init__(self, settings):
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        self.record_file = codecs.open(spiderConfig.InvalidResponseMessageFileName, 'w', encoding="utf-8")
        logger.debug('create a json file to record  Invalid Response Message ')

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider,response)
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)


    def spider_closed(self, spider):
        spider.logger.info('Spider close: %s' % spider.name)
        content = self.record_file.read()
        try:
            if len(content) == 0:
                logger.debug('All Response are valid and will remove InvalidResponseMessageFile')
                self.record_file.close()
                os.remove(spiderConfig.InvalidResponseMessageFileName)
            self.record_file.close()
        finally:
            self.record_file.close()
            logger.debug('an error when remove InvalidResponseMessageFile.json ')

    def _retry(self, request, reason, spider,response):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            reason = response_status_message(response.status)
            dict_response = {'url': request.url, 'reason': reason, 'retries': retries}
            lines = json.dumps(dict_response, ensure_ascii=False) + "\n"
            self.record_file.write(lines)
            return response

