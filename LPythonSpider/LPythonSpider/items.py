# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def remove_date_spot(value):
    if " ·" in value:
        return value.replace(" ·",'')

    else:
        return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class LpythonspiderItem(scrapy.Item):

    #文章封面
    thumb = scrapy.Field()

    #文章标题
    title = scrapy.Field()

    #文章发布日期
    date = scrapy.Field(
        input_processor=MapCompose(unicode.strip,remove_date_spot),
    )

    #文章的类型
    type = scrapy.Field()

    #文章简介
    summary = scrapy.Field()

    #文章链接
    link = scrapy.Field()

    #索引为分布式做准备
    object_id = scrapy.Field()

    pass
