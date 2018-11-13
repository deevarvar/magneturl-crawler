# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
import yaml


class dotdict(dict):
    """
        dot.notation access to dict attr
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def defaultlogconf(logconf):
    logconf.setdefault('name', 'crawl')
    logconf.setdefault('path', './')
    logconf.setdefault('level', 'DEBUG')
    logconf.setdefault('prefix', 'crun')
    logconf.setdefault('postfix', '.log')


def readconf(cfile='./config.yml'):
    with open(cfile, 'r') as f:
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


if __name__ == '__main__':
    ret = getlogconf()
    print(ret)