# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
import yaml
import os

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



if __name__ == '__main__':
    ret = getlogconf()
    print(ret)
    oneconfig = YamlConfig()
    oneconfig['test'] = 1
