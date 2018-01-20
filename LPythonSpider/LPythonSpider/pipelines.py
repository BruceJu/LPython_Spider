# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

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

class LpythonspiderPipeline_leancloud(object):
    def process_item(self, item, spider):
        print('item is %s'%item)
        return item