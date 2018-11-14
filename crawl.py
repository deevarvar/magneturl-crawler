# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com

import logging
import time
from functools import wraps
import os
from utils import getlogconf
from pyquery import PyQuery as pq
import requests
import sys
#python 2.x do not support encoding in open
from io import open
PY3k = sys.version_info >= (3,)

NORMALURL="http://www.btyunsou.co/"
MAINHTML="./btmain.html"
HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

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


logger = initlogger()


def elapsedtime(func):
    """
    Decorrator that caculate the exe time
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{0} runned {1:.7f} seconds".format(func.__name__, end - start))
        return result
    return wrapper


@elapsedtime
def hello():
    for i in range(10000000):
        pass
    logger.info('hello world')

@elapsedtime
def findquery():
    try:
        rsp = requests.get(NORMALURL,headers=HEADERS)
        with open(MAINHTML, encoding='utf-8', mode='w+') as mainhtml:
            mainhtml.write(rsp.text)
        page = pq(rsp.text)
        form = page('form')
        if form is None:
            raise Exception("no form in url")
        # get action, method in form
        logger.info('form method is {0}, action is {1}'.format(form.attr('method'), form.attr('action')))
        # get input name, input id is 'search'
        logger.info('input keyword is {}'.format(form('#search').attr('name')))

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

def getresult():
    pass



if __name__ == '__main__':
    hello()
    findquery()

