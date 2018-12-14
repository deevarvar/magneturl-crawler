# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
from utils import PY3k, elapsedtime, YamlConfig, logger, gethtml
import os
import sys
from pyquery import PyQuery as pq
import re
import argparse

STOREDPATH='./htmlsamples/btyunso'
BTYUNSO_SORT = ['click', 'date', 'size']


@elapsedtime
def hello():
    for i in range(10000000):
        pass
    logger.info('hello world')


def convertsize(size):
    unitlist = [0, 'B', 'KB', 'MB', 'GB', 'TB', 'PB']
    num = size.split(' ')[0]
    unit = size.split(' ')[1]
    multiply = 0
    if unit in unitlist:
        multiply = 1024 ** (unitlist.index(unit))
    return float(num) * multiply


def getresult(pageindex, num):
    pass

def btyunso(**kwargs):
    kw = kwargs['keyword']
    category = BTYUNSO_SORT[kwargs['sort']]
    resultnum = kwargs['number']
    #1. read config
    defaultconf = YamlConfig()
    schema = defaultconf['btyunso']['schema']
    domain = defaultconf['btyunso']['domain']
    pattern = {
        "kw": kw,
        "category": category,
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

    endindex = 1
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
        #kw is just str
        logger.info("{} pages result for {} , user need {}".format(lastindex, kw, resultnum))

        endindex = int(resultnum)/10
        # check page
        if int(resultnum)/10 > int(lastindex):
            # iterate all pages to get links
            endindex = lastindex
    else:
        #only one page or No result
        logger.info("only one page result for {} ".format(kw))
    # 4. get result
    # get all title, seems py2 is unicode, so convert to str
    #uri pattern is span with class media-down, a with attr title
    magnetlist = ["magnet:?xt=urn:btih:" + a.attr('href').split('.')[0]
                   for a in html('span.media-down a[title]').items()]
    # py3 title.text() is str
    # py2.7 title.text() is unicode
    titlelist = [title.text() for title in html('a.title').items()]

    # get date, size ,hot
    datelist = [date.text() for date in html('span.label-success').items()]
    sizelist = [size.text() for size in html('span.label-warning').items()]
    clicklist = [hot.text() for hot in html('span.label-primary').items()]

    results = list()
    for index in range(len(titlelist)):
        if not PY3k:
            #py2.7 logging to file will raise UnicodeEncodeError:
            titlelist[index] = titlelist[index].encode('utf-8')
        one = {
            "title": titlelist[index],
            "magneturi": magnetlist[index],
            "click": clicklist[index],
            "date": datelist[index],
            "size": sizelist[index]
        }
        results.append(one)

    if category in 'date':
        results = sorted(results, key=lambda elem: elem[category], reverse=True)
    elif category == 'click':
        results = sorted(results, key=lambda elem: int(elem[category]), reverse=True)
    elif category == 'size':
        results = sorted(results, key=lambda elem: convertsize(elem[category]), reverse=True)

    # combine
    for info in results:
        logger.info('{0}, {1}, {2}, {3}, {4}'.format(info['title'], info['magneturi'], info['click']
                                                 , info['date'], info['size']))


def outputformat(output):
    try:
        postfix = output.split('.')[1]
        if postfix in ['csv', 'json']:
            return output
        else:
            raise argparse.ArgumentTypeError("{} is not ended with csv or json".format(output))
    except:
        logger.info('type is {0}, error is {1}'.format(sys.exc_info()[0], sys.exc_info()[1]))
        raise argparse.ArgumentTypeError("{} is not ended with csv or json".format(output))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='crawler arguments')
    parser.add_argument('keyword', help="search keyword")
    parser.add_argument('--sort', '-s', type=int, default=0,
                        help="0: sort by click, 1: sort by date, 2: sort by size")
    parser.add_argument('--number', '-n', type=int, default=10,
                        help="search result number ,default is 10")
    parser.add_argument('--output', '-o', type=outputformat,
                        help="output filename with .csv or .json, default will dump to local output dir")
    parser.add_argument('--pretty-oneline', '-p', action='store_true',
                        help='show result in oneline')
    args = vars(parser.parse_args(['毒液', '-s', '0']))
    logger.info(args)
    #get page category
    cq = btyunso(**args)

