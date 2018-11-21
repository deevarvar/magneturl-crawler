#  -*- encoding =  utf-8 -*-
# author: zhihuaye@gmail.com

import unittest
import os
import sys
from pyquery import PyQuery as pq
curpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curpath, '../'))
from utils import YamlConfig, gethtml, mkdirp
from collections import Counter

class TestBtyunso(unittest.TestCase):
    def setUp(self):
        defaultconf = YamlConfig()
        schema = defaultconf['btyunso']['schema']
        domain = defaultconf['btyunso']['domain']
        # "http://www.btyunsou.co"
        self.url = ''.join([schema, domain])
        self.outpath = os.path.join(curpath, 'testdata')
        mkdirp(self.outpath)

    def test_entryurl(self):
        html = gethtml(url=self.url,outhtml=os.path.join(self.outpath, 'btmain.html'))
        page = pq(html)
        form = page('form')
        # should have the form element
        self.assertIsNotNone(form.text())
        method = form.attr('method')
        action = form.attr('action')
        # method should be 'get'
        self.assertEqual(method, 'get')
        # action should be '/search'
        self.assertEqual(action, '/search')

    def test_category(self):
        kw = "big bang"
        queryurl = "http://www.btyunsou.co/search?kw=" + kw
        html = gethtml(url=queryurl, outhtml=os.path.join(self.outpath, kw + '.html'))
        page = pq(html)
        clist = [ a.attr('href').split('_')[1] for a in page('div.sort li a').items()]
        # btyunsou is quite simple, three categories
        self.assertEqual(Counter(clist), Counter(['ctime', 'length', 'click']))


if __name__ == '__main__':
    unittest.main()