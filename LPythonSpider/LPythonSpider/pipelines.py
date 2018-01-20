# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import leancloud

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

class LpythonspiderPipeline_article_jobbole(object):
    def process_item(self, item, spider):
        #TODO:目前这里是采用的是同步的方式进行的插入，后续需要改成异步的
        ArticJobbleObject = leancloud.Object.extend('ArticJobbleObject')
        jobble_object = ArticJobbleObject()
        jobble_object.set('thumb', item['thumb'])
        jobble_object.set('title', item['title'])
        jobble_object.set('date', item['date'])
        jobble_object.set('type', item['type'])
        jobble_object.set('summary', item['summary'])
        jobble_object.set('link', item['link'])
        jobble_object.set('object_id', item['object_id'])
        jobble_object.save()
        return item