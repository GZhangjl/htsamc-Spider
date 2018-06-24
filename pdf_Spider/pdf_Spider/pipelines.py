# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from os.path import basename,join
from urllib.parse import urlparse
import codecs
from scrapy.exporters import CsvItemExporter


class DateProcessorPipeline(object):
    def process_item(self, item, spider):
        if item['is_recent'] == 'Yes':
            return item
        else:
            return {}


class MyFilesPipeline(FilesPipeline):
    def item_completed(self, results, item, info):
        for ok,v in results:
            item['file_path'] = v['path']
        return item

    def file_path(self, request, response=None, info=None):
        path = basename(urlparse(request.url).path)
        return 'full_pdf/%s' % path


class CsvWritePipeline(object):
    def __init__(self):
        self.file = open('htsamc_pdf.csv','wb')
        self.exporter = CsvItemExporter(self.file,include_headers_line=True,\
                                        encoding='utf8',fields_to_export=['file_name','create_date','file_url','is_recent'])
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def end_write(self,spider):
        self.file.close()
