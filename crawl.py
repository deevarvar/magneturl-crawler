# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
from utils import PY3k, elapsedtime, YamlConfig, logger, gethtml
import os
from pyquery import PyQuery as pq
import re

STOREDPATH='./htmlsamples/btyunso'

@elapsedtime
def hello():
    for i in range(10000000):
        pass
    logger.info('hello world')


def btyunso(kw="asdfasdfasdfasdf"):
    #1. read config
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

    # 2. get page
    # btyunso is not that good, always return 100 pages and 10 per page
    rsp = gethtml(url=qurl, outhtml=os.path.join(STOREDPATH, kwpage))
    html = pq(rsp)

    # 3. check if no result
    if html('div.media-body').html() is None:
        logger.error('No result for {}'.format(kw))
        return -1

    # 4. get pagination
    #
    if html('.pagination').html():
        alinks = [a.attr("href") for a in html('ul.pagination a').items() if a.attr('href') ]
        #last page index from href, text may be "末页" in more than 10 pages.
        lastlink = alinks[-1]
        indexpattern = r'.*_.*_(\d+).html'
        cpattern = re.compile(indexpattern)
        imatch = cpattern.search(lastlink)
        lastindex = imatch.group(1)
        logger.info("{} pages result for {} ".format(lastindex, kw))
    else:
        #only one page or No result
        logger.info("only one page result for {} ".format(kw))
    # 4. get result
    # get all title, seems py2 is unicode, so convert to str
    # py3 get bytes
    titlelist = [{"title": title.text().encode('utf-8').decode('utf-8')} for title in html('a.title').items()]

    # get date, size ,hot
    datelist = [{"date": date.text()} for date in html('span.label-success').items()]
    sizelist = [{"size": size.text()} for size in html('span.label-warning').items()]
    hotlist = [{"hot": hot.text()} for hot in html('span.label-primary').items()]
    infolist = list(zip(titlelist,datelist, sizelist, hotlist))
    # combine
    for info in infolist:
        logger.info(u'{} {} {} {}'.format(info[0],info[1], info[2], info[3]))

if __name__ == '__main__':
    #get page category
    cq = btyunso()

