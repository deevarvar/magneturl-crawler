# -*- encoding: utf-8 -*-
# author: zhihuaye@gmail.com
import yaml
import os
import time
from functools import wraps
import logging
from pyquery import PyQuery as pq
import requests
import sys
import errno
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


CONFIGYML = os.path.join(os.path.dirname(os.path.realpath(__file__)),'./config.yml')

class DotDict(dict):
    """
        dot.notation access to dict attr
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class YamlConfig(dict):
    def __init__(self, filename=CONFIGYML):
        self.filename = filename
        super(YamlConfig, self).__init__()
        if os.path.isfile(CONFIGYML):
            with open(filename, 'r') as f:
                super(YamlConfig, self).update(yaml.safe_load(f) or {})
        else:
            raise Exception('{} not exists!'.format(CONFIGYML))

    def __setitem__(self, key, value):
        super(YamlConfig, self).__setitem__(key, value)
        with open(self.filename, 'w') as f:
            #note dump seems only support dict
            yaml.dump(dict(self), f, default_flow_style=False)

    def __delitem__(self, key):
        super(YamlConfig, self).__delitem__(key)
        with open(self.filename, 'w') as f:
            yaml.dump(dict(self), f, default_flow_style=False)

    def update(self, **kwargs):
        super(YamlConfig, self).update(kwargs)
        with open(self.filename, 'w') as f:
            yaml.dump(dict(self), f, default_flow_style=False)


def defaultlogconf(logconf):
    logconf.setdefault('name', 'crawl')
    logconf.setdefault('path', './')
    logconf.setdefault('level', 'DEBUG')
    logconf.setdefault('prefix', 'crun')
    logconf.setdefault('postfix', '.log')


def readconf(cfile=CONFIGYML):
    with open(cfile) as f:
        conf = yaml.safe_load(f)
        # init keyword
        conf.setdefault('logconf', {})
        return conf


def getlogconf():
    config = readconf()
    defaultlogconf(config['logconf'])
    #TODO: add logconf validator for level, path, etc...
    return config['logconf']['name'], config['logconf']['path'], \
           config['logconf']['level'], config['logconf']['prefix'], config['logconf']['postfix']


def initlogger():
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S', time.gmtime())
    logname, logpath, loglevel, logprefix, logpostfix = getlogconf()
    logger = logging.getLogger(logname)
    logger.setLevel(loglevel)
    consoleformatter = logging.Formatter('%(message)s')
    fileformatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s '
                                  '- %(funcName)s - %(lineno)d - %(message)s')

    # console handler, set to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(consoleformatter)
    logger.addHandler(ch)

    # file handler, set to debug
    if PY3k:
        fh = logging.FileHandler(os.path.join(logpath,
                                              ''.join([logprefix, timestamp, logpostfix])),encoding='utf-8')
    else:
        #seems python2.7 logging can not do utf-8
        fh = logging.FileHandler(os.path.join(logpath,
                                              ''.join([logprefix, timestamp, logpostfix])))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fileformatter)
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
        logger.info("{0} runned {1:.7f} seconds".format(func.__name__, end - start))
        return result
    return wrapper


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

def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

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
    qurl = getqueryurl() + kw
    logger.info('search url is {}'.format(qurl))
    rsp = gethtml(url=qurl, outhtml=''.join(['./', kw, '.html']))

    # get category dict list
    # in case admin will change it.
    # current pattern is field2 delemitered by _ like'/search/big%20bang_length_1.html'
    page = pq(rsp)
    try:
        categorylist = [{'kw': a.attr('href').split('_')[1], 'text': a.text()}
                        for a in page('div .sort li a').items()]
        #[{'text': '收录时间', 'kw': 'ctime'}, {'text': '活跃热度', 'kw': 'click'}, {'text': '文件大小', 'kw': 'length'}]
        logger.info("page category is {}".format(categorylist))

    except:
        etype = sys.exc_info()[0]
        estr = sys.exc_info()[1]
        logger.error("Exceptions: {} {}".format(etype, estr))
        sys.exit(-1)


if __name__ == '__main__':
    ret = getlogconf()
    print(ret)
    oneconfig = YamlConfig()
    oneconfig['test'] = 1
