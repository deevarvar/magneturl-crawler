# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
import yaml
import os
import time
from functools import wraps
import logging

CONFIGYML = './config.yml'

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
        logger.info("{0} runned {1:.7f} seconds".format(func.__name__, end - start))
        return result
    return wrapper


if __name__ == '__main__':
    ret = getlogconf()
    print(ret)
    oneconfig = YamlConfig()
    oneconfig['test'] = 1
