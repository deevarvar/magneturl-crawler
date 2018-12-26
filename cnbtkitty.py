# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com

from utils import PY3k, elapsedtime, YamlConfig, logger, gethtml
import os
import sys
from pyquery import PyQuery as pq
import re

import requests

url='http://cnbtkitty.pw'

#no result page: abcdefghijg
formdata={
    "keyword": "big bang theory"
}
rsp = requests.post(url, data=formdata)
with open('./cnbtkitty.html', 'w+', encoding='utf-8') as mainhtml:
    mainhtml.write(rsp.text)
html = pq(rsp.text)
if html('div.list-box').html() is None:
    print("no result")
    exit(-1)
else:
    alinks = [ a.attr('href') for a in html('div.list-box dl.list-con dt a').items()]
    print(alinks)
# then need to parse second html to get the real magneturi
secsample = 'http://cnbtkitty.pw/t/BcGHDQAwCAOwlwgjEueU9f8JtSHBVTHZoWmU22N2k3eAt2TSBqwP.html'
rsp = requests.get(secsample)
with open('./second.html', 'w+', encoding='utf-8') as secondhtml:
    secondhtml.write(rsp.text)
html = pq(rsp.text)
dlink = html('dd.magnet a').text()
print(dlink)