# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com

from utils import PY3k, elapsedtime, YamlConfig, logger, gethtml,mkdirp, outputformat
import os
import sys
from pyquery import PyQuery as pq
import re
import argparse
import requests
import concurrent.futures
import time
from random import randint

STOREDPATH='./htmlsamples/cnbtkitty'
mkdirp(STOREDPATH)
CONF = YamlConfig()
SCHEMA = CONF['cnbtkitty']['schema']
DOMAIN = CONF['cnbtkitty']['domain']

BTURL=''.join([SCHEMA, DOMAIN])
BTKITTY_SORT = ['Relevance', 'AddedDate', 'Size', 'Files', 'Popularity']

#no result page: abcdefghijg

proxies = {
}
def getentrypage(kw):
    formdata = {
        "keyword": kw
    }
    kwpage = "{0}_Relevance_1.html".format(kw)
    rsp = gethtml(url=BTURL, outhtml=os.path.join(STOREDPATH, kwpage), method='POST', data=formdata, proxies=proxies)
    html = pq(rsp)
    if html('dl.list-con').html() is None:
        logger.error('No result for {}'.format(kw))
        return None
    else:
        return html


def genresulturl(preurl=None, category=0,index=1):
    return '/'.join([preurl, str(index), str(category)])


def fetchresult(url):
    target = BTURL + url
    rsp = gethtml(url=target, outhtml=os.path.join(STOREDPATH, url.split('/')[2]), proxies=proxies)
    html = pq(rsp)
    dlink = html('dd.magnet a').text()
    #FIXME: ever url is valid, the magnet uri may be none... WTF~!
    if dlink:
        logger.info(dlink)
    else:
        logger.info("no result for {}.".format(target))

    time.sleep(randint(1, 5))

@elapsedtime
def cnbtkitty(**kwargs):
    resultnum = kwargs['number']
    kw = kwargs['keyword']
    category = kwargs['sort']
    results = list()
    # 0. get entry html, default is Relevance page
    html = getentrypage(kw=kw)
    if html is None:
        return -1

    # 1. parse the page and get result pattern
    # /search/S8pMV0hKzEtXKMlIzS-qBAA/1/1/0.html
    # 1.1 result page pattern  /pageindex/category/0.html
    # 1.2 resutl pattern 'div.list-box dl.list-con dt a'
    apattern = html('div.list-box div.category a.select')
    preurl = '/'.join(apattern.attr('href').split('/')[:3])

    # 2. change sort and check num

    # 3. get result page
    alinks = [a.attr('href') for a in html('div.list-box dl.list-con dt a').items()]
    logger.info(alinks)

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        #map will return in iterate order
        # submit and as_completed will return in completed order
        executor.map(fetchresult, alinks)

    #fetchresult(alinks[0])



if __name__ == "__main__":
    # 0. add argparser
    parser = argparse.ArgumentParser(prog="cnbtkitty crawler")
    parser.add_argument('keyword', help="search keyword")
    parser.add_argument('--sort', '-s', type=int, default=0,
                        help="0: sort by Relevance, 1: sort by AddedDate, 2: sort by Size, 3: sort by Files, 4: sort by Popularity")
    parser.add_argument('--number', '-n', type=int, default=5,
                        help="search result number ,default is 5")
    parser.add_argument('--output', '-o', type=outputformat,
                        help="output filename with .csv or .json, default will dump to local output dir")
    parser.add_argument('--pretty-oneline', '-p', action='store_true',
                        help='show result in oneline')
    args = vars(parser.parse_args())
    logger.info(args)
    cq = cnbtkitty(**args)
    # 1. get entry page and entry url

    # 2. get all magnet uri info using future

    # 3. print

    pass