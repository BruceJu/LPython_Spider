# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging

import itchat
from fake_useragent import UserAgent
from scrapy import signals
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.exceptions import NotConfigured
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.internet.threads import deferToThread
from twisted.web.client import ResponseFailed

from Util.common import QueryRandomIP
from Util.common import sendmail
from helper.ConfigHelper import ConfigManager
from helper.RedisHelper import redisManager

logger = logging.getLogger(__name__)


class RandomUserAgentMiddlware(object):
    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.host = 'http://{0}:8000/?types=0&count=60&country=国内'
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        randomua = get_ua()
        request.headers.setdefault('User-Agent', randomua)
        proxy_host = ConfigManager.redis_host
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
        self.default_serialize = ScrapyJSONEncoder().encode
        self.server = redisManager.doGetServer()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider, response)
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider, response):
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
        elif self.server is not None:
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            reason = response_status_message(response.status)
            dict_response = {'url': request.url, 'reason': reason, 'retries': retries}
            data = self.default_serialize(dict_response)
            print '*' * 10 + 'record invaild request and url is %s' % request.url + '*' * 10
            RETRYT_KEY = '%(spider)s:invailrequest'
            self.server.rpush(RETRYT_KEY, data)
        return response


class StatsAndErrorMailerMiddlware(object):

    def __init__(self, stats, recipients):
        self.stats = stats
        self.recipients = recipients

    @classmethod
    def from_crawler(cls, crawler):
        recipients = crawler.settings.getlist("STATSMAILER_RCPTS")
        if not recipients:
            raise NotConfigured
        o = cls(crawler.stats, recipients)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)

        crawler.signals.connect(o.spider_error, signal=signals.spider_error)
        return o

    def spider_closed(self, spider):
        spider_stats = self.stats.get_stats(spider)
        body = "Global stats\n\n"
        body += "\n".join("%-50s : %s" % i for i in self.stats.get_stats().items())
        body += "\n\n%s stats\n\n" % spider.name
        body += "\n".join("%-50s : %s" % i for i in spider_stats.items())
        return sendmail(body, self.recipients, "Scrapy stats for: %s" % spider.name)

    def spider_error(self, failure, response, spider):
        body = "Meet Error\n\n"
        body += "\n\n%s error\n\n" % spider.name + "\n"
        body += " ".join("error message is  : %s" % failure.getErrorMessage)
        body += " ".join("error response url is  : %s" % response.url)
        return sendmail(body, self.recipients, "Scrapy meet a error for: %s" % spider.name)


class WeChatNoticeMiddlware(object):

    def __init__(self, crawler):
        if not crawler.settings.getbool('WECHAT_NOTICE_ENABLED'):
            raise NotConfigured
        self.wechat_notice_enabled = crawler.settings.getbool('WECHAT_NOTICE_ENABLED')
        self.stats = crawler.stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.spider_error, signal=signals.spider_error)
        return o

    def spider_opened(self, spider):
        if self.wechat_notice_enabled:
            deferToThread(self._wechat_notice, u"%s spider start" % spider.name)

    def spider_closed(self, spider):
        spider_stats = self.stats.get_stats(spider)
        body = "Global stats\n\n"
        body += "\n".join("%-50s : %s" % i for i in self.stats.get_stats().items())
        body += "\n\n%s stats\n\n" % spider.name
        body += "\n".join("%-50s : %s" % i for i in spider_stats.items())
        if self.wechat_notice_enabled:
            deferToThread(self._wechat_notice, body)

    def spider_error(self, failure, response, spider):
        body = "Meet Error\n\n"
        body += "\n\n%s error\n\n" % spider.name + "\n"
        body += " ".join("error message is  : %s" % failure.getErrorMessage)
        body += " ".join("error response url is  : %s" % response.url)
        if self.wechat_notice_enabled:
            deferToThread(self._wechat_notice, body)

    def _wechat_notice(self, message):
        if itchat.check_login == 200:
            itchat.send_msg(message)
        else:
            itchat.auto_login(hotReload=True)
            itchat.send_msg(message)
        itchat.logout
