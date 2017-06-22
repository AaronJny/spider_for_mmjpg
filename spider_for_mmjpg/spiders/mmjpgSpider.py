#coding=utf-8
import scrapy
from scrapy.http import Request
import os
from spider_for_mmjpg.items import SpiderForMmjpgItem

class MMjpgSpider(scrapy.spiders.Spider):
    name='mmjpg'
    allowed_domians=['mmjpg.com']
    start_urls=['http://www.mmjpg.com/']
    for i in range(2,70):
        start_urls.append('http://www.mmjpg.com/home/'+str(i))
    base_url=u'http://www.mmjpg.com'

    #创建存放图片的文件夹
    if not os.path.exists('image'):
        os.makedirs('image')
    #再创建一个子文件夹，用来存放所有图片。（根据我的需求，我将每个文件都存了两份，
    # 一份放在对应的标题文件夹下，一份放在image/allImage下）
    if not os.path.exists('image/allImage'):
        os.makedirs('image/allImage')

    #解析一个图片集的图片页面
    def parseArticle(self,response):
        #先获取当前页面的图片列表
        src_links=response.xpath('//img[re:test(@src,"^http://img.mmjpg.com/20\d{2}/\d+/\d+.jpg$")]/@src').extract()
        #获取该图片集的其他图片页面链接
        page_links=response.xpath('//a[re:test(@href,"^/mm/\d+/\d+$")]/@href').extract()
        #加上基地址
        for i in range(len(page_links)):
            page_links[i]=self.base_url+page_links[i]
        #获取该页面可以到达的其他图片集链接（无基地址形式）
        links=response.xpath('//a[re:test(@href,"^/mm/\d+$")]/@href').extract()
        #加上基地址
        for i in range(len(links)):
            links[i]=self.base_url+links[i]
        # 获取该页面可以到达的其他图片集链接（有基地址形式）
        links+=response.xpath('//a[re:test(@href,"^http://www.mmjpg.com/mm/\d+$")]/@href').extract()
        # 根据图片链接等信息，生成item，交由管道处理
        for url in src_links:
            #获取图片集名，即所属文件夹名
            dir_name = response.xpath('//title/text()').re(ur'([\u4e00-\u9fa5]+)')[0]
            #创建item
            item=SpiderForMmjpgItem()
            #图片保存路径
            item['file_path']=os.path.join('image',dir_name)
            #图片名
            item['file_name']=url[21:].replace('/', '-')
            #图片url
            item['file_url']=url
            #提交item
            yield item
        #使用此函数解析该图片集的其他图片页面
        for url in page_links:
            yield Request(url,callback=self.parseArticle)
        #使用此函数解析该页面可以到达的其他图片集
        for url in links:
            yield Request(url,callback=self.parseArticle)



    def parse(self,response):
        #获取所有图片集链接
        links=response.xpath('//a[re:test(@href,"^http://www.mmjpg.com/mm/\d+$")]/@href').extract()
        print len(links)
        #请求所有的图片集
        for url in links:
            yield Request(url,callback=self.parseArticle)