# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com

import logging
import time
from functools import wraps
import os
from utils import test

logger = logging.getLogger("crawl")
path = './'
logprefix = "crun_"
timestamp = time.strftime('%Y_%m_%d_%H_%M_%S', time.gmtime())
logpostfix = '.log'


def initlogger():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '
                                  '- %(funcName)s - %(lineno)d - %(message)s')

    # console handler, set to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # file handler, set to debug
    fh = logging.FileHandler(os.path.join('./',
                                          ''.join([logprefix, timestamp, logpostfix])))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


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

initlogger()
hello()
test()
logger.debug('end')