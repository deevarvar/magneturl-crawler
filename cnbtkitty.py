# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com

from utils import PY3k, elapsedtime, YamlConfig, logger, gethtml
import os
import sys
from pyquery import PyQuery as pq
import re

import requests

url='http://cnbtkitty.pw'
formdata={
    "keyword": "big bang theory"
}
rsp = requests.post(url, data=formdata)
with open('./cnbtkitty.html', 'w+', encoding='utf-8') as mainhtml:
    mainhtml.write(rsp.text)
# then need to parse second html to get the real magneturi
secsample = 'http://cnbtkitty.pw/t/BcGHDQAwCAOwlwgjEueU9f8JtSHBVTHZoWmU22N2k3eAt2TSBqwP.html'
rsp = requests.get(secsample)
with open('./second.html', 'w+', encoding='utf-8') as secondhtml:
    secondhtml.write(rsp.text)