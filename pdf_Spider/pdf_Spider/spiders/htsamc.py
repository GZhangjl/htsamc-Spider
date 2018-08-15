# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse, Request
from urllib import parse
import datetime
from selenium.webdriver import Chrome

from pdf_Spider.items import PdfSpiderItem


# file_name = Field()
# file_url = Field()
# file_path = Field()
# create_date = Field()

class HtsamcSpider(scrapy.Spider):
    name = 'htsamc'
    allowed_domains = ['http://www.htsamc.com/']
    start_urls = ['http://www.htsamc.com/servlet/Article?catalogId=2929&keyword=&length=140&rowOfPage={0}']

    def parse(self, response):
        pdf_item = PdfSpiderItem()
        for file in response.css('dl'):
            pdf_item['file_name'] = file.css('.t_p::text').extract_first().strip()
            pdf_item['file_url'] = [parse.urljoin(response.url,file.css('.a_down::attr(href)').extract_first())]
            create_date = file.css('em::text').extract_first()
            try:
                create_date = datetime.datetime.strptime(create_date, '%Y-%m-%d').date()
                today = datetime.date.today()
                days_delta = (today - create_date).days
                if days_delta <= 14:
                    is_recent = 'Yes'
                else:
                    is_recent = 'No'
            except Exception as e:
                create_date = "Unknown"
                is_recent = 'No'

            pdf_item['create_date'] = create_date
            pdf_item['is_recent'] = is_recent

            yield pdf_item

    # htsamc公告爬取，通过浏览器开发者工具可以观察到有一个POST请求，可以通过提交form表单数据，来确定页码和每页包括的数据，通过该方式提交
    # 请求应该会更加符合人工浏览网页的风格，但是需要重复产生FormRequest提交请求数据进行翻页（由于scrapy是异步的，所以可能会更快，*待定*）
    # 这里使用的是一个更加“机器人”的做法，通过直接修改
    # ’http://www.htsamc.com/servlet/Article?catalogId=2929&keyword=&length=140&rowOfPage=10‘url中的rowOfPage的数据将同一
    # 个catalogId下的所有公告列表都获得到，之后进行PDF文件下载链接的提取与下载。
    def start_requests(self):
        import re
        web_drvier = Chrome(executable_path=r'C:\Users\zhang\chromedriver_win32\chromedriver.exe')
        # 这里模拟浏览器登陆是为了在页面上获得公告的总页数，以此来计算总共有几个公告
        web_drvier.get('http://www.htsamc.com/main/news/productannounce/documentsissued/index.shtml')
        body = web_drvier.page_source
        web_drvier.close()
        p_response = HtmlResponse(url='htsamc.com', body=body, encoding='utf8')
        page_num = p_response.css('tr#productMelonmdPageNum td:first-child::text').extract_first()
        page_num = re.match('\D+(\d+)\D+(\d+)\D+', page_num).group(2)
        all_num = int(page_num) * 10
        aim_url = self.start_urls[0].format(all_num)

        yield Request(url=aim_url, callback=self.parse, method='GET')