# -*- coding: utf-8 -*-

'''
本模块用Requests包对西刺代理网站的高匿ip进行爬取，然后通过接口为爬虫主体提交请求提供代理ip
这部分代理ip希望通过middleware加入request请求中。
'''

import requests
from scrapy.selector import Selector
import json

headers = {
    'Host':'www.xicidaili.com',
    'Referer':'http://www.xicidaili.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

url = 'http://www.xicidaili.com/nn/{0}'

count = 0
proxy_dict = {
    'total':count,
    'proxy_dict':{}
}

for i in range(10):
    page = i + 1
    response = requests.get(url=url.format(page), headers=headers)
    ip_list = Selector(response=response).css('table tr')[1:]
    for ip_info in ip_list:
        if ip_info.css('td:nth-child(7)>div>div.slow'):
            continue
        proxy_ip = ip_info.css('td:nth-child(2)::text').extract_first()
        proxy_port = ip_info.css('td:nth-child(3)::text').extract_first()
        proxy_http = ip_info.css('td:nth-child(6)::text').extract_first()

        proxy = '{0}://{1}:{2}'.format(proxy_http, proxy_ip, proxy_port)
        proxy_dict['proxy_dict'][count] = proxy
        count += 1

proxy_dict['total'] = count

with open('./proxy.json', 'w') as f:
    json.dump(proxy_dict, f)