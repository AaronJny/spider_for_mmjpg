# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderForMmjpgItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #图片名
    file_name=scrapy.Field()
    #图片保存路径
    file_path=scrapy.Field()
    #图片url
    file_url=scrapy.Field()
