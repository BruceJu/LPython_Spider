# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import leancloud
from twisted.internet.threads import deferToThread
from scrapy.utils.serialize import ScrapyJSONEncoder


class JsonWithEncodingPipeline(object):

    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

class LpythonspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class Lpythonspider_article_jobbole(object):

    def __init__(self):
        self.default_serialize = ScrapyJSONEncoder().encode

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
    
    def _process_item(self, item, spider):
        ArticJobbleObject = leancloud.Object.extend('ArticJobbleObject')
        jobble_object = ArticJobbleObject()
        data =self.default_serialize(item)
        for key, value in item.items():
            jobble_object.set(key=str(key),value=value)

        return item