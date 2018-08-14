# -*- coding: utf-8 -*-

'''
这一次是为了将获取公告页面（包括翻页）更加人类化，将使用FormRequest进行翻页，而不再使用捷径
“h”意味着“human”
'''

import scrapy


class HtsamcHSpider(scrapy.Spider):
    name = 'htsamc_h'
    allowed_domains = ['http://www.htsamc.com/']
    start_urls = ['http://http://www.htsamc.com//']

    def parse(self, response):
        pass