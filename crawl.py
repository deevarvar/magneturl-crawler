# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
from utils import PY3k, elapsedtime, YamlConfig, logger, gethtml
import os
from pyquery import PyQuery as pq


@elapsedtime
def hello():
    for i in range(10000000):
        pass
    logger.info('hello world')


def btyunso(kw="big bang"):
    defaultconf = YamlConfig()
    schema = defaultconf['btyunso']['schema']
    domain = defaultconf['btyunso']['domain']
    pattern = {
        "kw": kw,
        "category": "ctime",
        "index": 1
    }
    kwpage = "{kw}_{category}_{index}.html".format(**pattern)
    qurl = ''.join([schema, domain, '/search/', kwpage])
    logger.info('qurl is {}'.format(qurl))
    # btyunso is not that good, always return 100 pages and 10 per page
    rsp = gethtml(url=qurl, outhtml=os.path.join('./', kwpage))
    html = pq(rsp)
    # get all title, seems py2 is unicode, so convert to str
    # py3 get bytes
    titlelist = [title.text().encode('utf-8') for title in html('a.title').items()]

    # get date, size ,hot
    datelist = [date.text() for date in html('span.label-success').items()]
    sizelist = [size.text() for size in html('span.label-warning').items()]
    hotlist = [hot.text() for hot in html('span.label-primary').items()]
    infolist = list(zip(titlelist,datelist, sizelist, hotlist))
    # combine
    for info in infolist:
        logger.info(u'{} {} {} {}'.format(info[0].decode('utf-8'), info[1], info[2], info[3]))

if __name__ == '__main__':
    #get page category
    cq = btyunso()

