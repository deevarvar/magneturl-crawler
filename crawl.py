# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com

import logging
import time
from functools import wraps
import os
from utils import getlogconf, elapsedtime, logger
from pyquery import PyQuery as pq
import requests
import sys
import re
#python 2.x do not support encoding in open
from io import open

PY3k = sys.version_info >= (3,)
if not PY3k:
    from urllib import quote
else:
    from urllib.parse import quote



BTDOMAIN='www.btyunsou.co'
NORMALURL=''.join(['http://', BTDOMAIN]) #"http://www.btyunsou.co"
MAINHTML="./btmain.html"
HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
QUERYURL=''

def initlogger():
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S', time.gmtime())
    logname, logpath, loglevel, logprefix, logpostfix = getlogconf()
    logger = logging.getLogger(logname)
    logger.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '
                                  '- %(funcName)s - %(lineno)d - %(message)s')

    # console handler, set to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # file handler, set to debug
    fh = logging.FileHandler(os.path.join(logpath,
                                          ''.join([logprefix, timestamp, logpostfix])))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

@elapsedtime
def hello():
    for i in range(10000000):
        pass
    logger.info('hello world')


@elapsedtime
def gethtml(url, outhtml=MAINHTML):
    try:
        rsp = requests.get(url, headers=HEADERS)
        logger.info('encoding is {}'.format(rsp.encoding))
        with open(outhtml, encoding='utf-8', mode='w+') as mainhtml:
            mainhtml.write(rsp.text)
        return rsp.text

    except requests.exceptions.HTTPError as errh:
        logger.error("Http Error: {}".format(errh))
        sys.exit(-1)
    except requests.exceptions.ConnectionError as errc:
        logger.error("Connection Error: {}".format(errc))
        sys.exit(-1)
    except requests.exceptions.Timeout as errt:
        logger.error("TimeOut: {}".format(errt))
        sys.exit(-1)
    except requests.exceptions.RequestException as errr:
        logger.error("RequestExeptions: {}".format(errr))
        sys.exit(-1)
    except:
        etype = sys.exc_info()[0]
        estr = sys.exc_info()[1]
        logger.error("Exceptions: {} {}".format(etype, estr))
        sys.exit(-1)


@elapsedtime
def getqueryurl():
    html = gethtml(url=NORMALURL)
    page = pq(html)
    form = page('form')
    if form is None:
        raise Exception("no form in url")
    # get action, method in form
    method = form.attr('method')
    if method != 'get':
        raise Exception("query method is {}".format(method))
    action = form.attr('action')
    logger.info('form method is {0}, action is {1}'.format(method, action))

    # get input name, input id is 'search'
    keyword = form('#search').attr('name')
    logger.info('input keyword is {}'.format(keyword))
    return ''.join([NORMALURL, action, '?' + keyword + '='])


def query(kw):
    """
    from one result page to
    :param kw:
    :return:
    """
    qurl = QUERYURL + kw
    logger.info('search url is {}'.format(qurl))
    rsp = gethtml(url=qurl,outhtml=''.join(['./', kw, '.html']))

    # get category dict list
    # in case admin will change it.
    # current pattern is field2 delemitered by _ like'/search/big%20bang_length_1.html'
    page = pq(rsp)
    try:
        categorylist = [{'kw': a.attr('href').split('_')[1], 'text' : a.text()}
                        for a in page('div .sort li a').items()]
        #[{'text': '收录时间', 'kw': 'ctime'}, {'text': '活跃热度', 'kw': 'click'}, {'text': '文件大小', 'kw': 'length'}]
        logger.info("page category is {}".format(categorylist))

    except:
        etype = sys.exc_info()[0]
        estr = sys.exc_info()[1]
        logger.error("Exceptions: {} {}".format(etype, estr))
        sys.exit(-1)
    return categorylist


if __name__ == '__main__':
    QUERYURL = getqueryurl()
    logger.info('query url is {}'.format(QUERYURL))
    cq = query(kw='big bang')

