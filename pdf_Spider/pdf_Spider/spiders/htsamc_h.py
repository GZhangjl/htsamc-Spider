# -*- coding: utf-8 -*-

'''
这一次是为了将获取公告页面（包括翻页）更加人类化，将使用FormRequest进行翻页，而不再使用捷径；
“h”意味着“human”
'''

import scrapy
from scrapy.http import HtmlResponse, Request, FormRequest
from urllib import parse
import datetime
from selenium.webdriver import Chrome


class HtsamcSpider(scrapy.Spider):
    name = 'htsamc_h'
    allowed_domains = ['htsamc.com/']
    start_urls = ['http://www.htsamc.com/servlet/Article?catalogId=2929&keyword=&length=140&rowOfPage=10']

    # 经过试验，西刺代理中的代理ip存在大量不可用现象，当多次请求未果后，爬虫就会退出，所以就不再这块继续好费时间了，控制靠爬取速度即可。
    # custom_settings = {
    #     'DOWNLOADER_MIDDLEWARES' : {
    #        'pdf_Spider.middlewares.ProxyDownloaderMiddleware': 1
    #     }
    # }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    def parse(self, response):
        pass

    # htsamc公告爬取，通过浏览器开发者工具可以观察到有一个POST请求，可以通过提交form表单数据，来确定页码和每页包括的数据，但是总共有几
    # 页需要事先获取，所以在这里使用selenium模拟浏览器进行请求并获得总页面数。
    def start_requests(self):
        # import re
        # web_drvier = Chrome(executable_path=r'C:\Users\zhang\chromedriver_win32\chromedriver.exe')
        # # 这里模拟浏览器登陆是为了在页面上获得公告的总页数，以此来计算总共有几个公告
        # web_drvier.get('http://www.htsamc.com/main/news/productannounce/documentsissued/index.shtml')
        # body = web_drvier.page_source
        # web_drvier.close()
        # p_response = HtmlResponse(url='htsamc.com', body=body, encoding='utf8')
        # page_num = p_response.css('tr#productMelonmdPageNum td:first-child::text').extract_first()
        # # 这里使用正则表达式获取页面数
        # page_num = re.match('\D+(\d+)\D+(\d+)\D+', page_num).group(2)
        # all_num = int(page_num) * 10

        yield FormRequest(url=self.start_urls[0], method='POST', formdata={'pageNumber':'10', 'rowOfPage':'10'}, headers=self.headers, callback=self.parse)