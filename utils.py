# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
import logging
import yaml

logger = logging.getLogger("crawl")
with open('./config.yml', 'r') as f:
    conf = yaml.safe_load(f)
    print(conf)


def test():
    logger.info('test')
