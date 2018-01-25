# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import leancloud
from twisted.internet.threads import deferToThread


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
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
    
    def _process_item(self, item, spider):
        ArticJobbleObject = leancloud.Object.extend('ArticJobbleObject')
        jobble_object = ArticJobbleObject()
        if item['thumb'] is None:
            jobble_object.set('thumb','No cover')
        else:
            jobble_object.set('thumb', item['thumb'])

        jobble_object.set('title', item['title'])
        jobble_object.set('date', item['date'])
        jobble_object.set('type', item['type'])
        jobble_object.set('summary', item['summary'])
        jobble_object.set('link', item['link'])
        jobble_object.set('object_id', item['object_id'])
        jobble_object.save()
        return item