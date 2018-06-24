# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from pdf_Spider.items import PdfSpiderItem
import datetime

# file_name = Field()
# file_url = Field()
# file_path = Field()
# create_date = Field()

class HtsamcSpider(scrapy.Spider):
    name = 'htsamc'
    allowed_domains = ['http://www.htsamc.com/']
    start_urls = ['http://www.htsamc.com/servlet/Article?catalogId=2930&keyword=&length=140&rowOfPage=2779']

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