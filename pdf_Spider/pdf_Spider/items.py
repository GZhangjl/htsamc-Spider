# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
import datetime

class PdfSpiderItem(scrapy.Item):

    file_name = Field()
    file_url = Field()
    file_path = Field()
    create_date = Field()
    files = Field()
    is_recent = Field()

    pass
