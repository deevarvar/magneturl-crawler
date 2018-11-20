# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
from utils import elapsedtime,  query, logger

@elapsedtime
def hello():
    for i in range(10000000):
        pass
    logger.info('hello world')

if __name__ == '__main__':
    #get page category
    cq = query(kw='big bang')

