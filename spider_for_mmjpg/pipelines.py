# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import shutil

class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        #文件夹不存在则创建
        if not os.path.exists(item['file_path']):
            os.makedirs(item['file_path'])
        #图片已经保存过了，则直接跳过
        if os.path.exists(os.path.join(item['file_path'],item['file_name'])):
            return item
        #创建图片文件
        with open(os.path.join(item['file_path'],item['file_name']),'wb') as f:
            #根据url获取图片流
            response=requests.get(item['file_url'],stream=True)
            #写入到图片中
            for block in response.iter_content(1024):
                if not block:
                    break
                f.write(block)
        #复制一份到image/allImage中（根据需求，可删除）
        shutil.copy(os.path.join(item['file_path'],item['file_name']), os.path.join('image/allImage', item['file_name']))
        return item
