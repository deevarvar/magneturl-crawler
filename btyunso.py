# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com
from utils import PY3k, elapsedtime, YamlConfig, logger, gethtml, mkdirp
import os
import sys
from pyquery import PyQuery as pq
import re
import argparse
import math
import unicodecsv as csv
import json
from io import open

STOREDPATH='./htmlsamples/btyunso'
mkdirp(STOREDPATH)
BTYUNSO_SORT = ['click', 'date', 'size']
CONF = YamlConfig()
SCHEMA = CONF['btyunso']['schema']
DOMAIN = CONF['btyunso']['domain']

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


def getvalidpage(kw, category, index):
    # return html
    pattern = {
        "kw": kw,
        "category": category,
        "index": index
    }
    kwpage = "{kw}_{category}_{index}.html".format(**pattern)
    qurl = ''.join([SCHEMA, DOMAIN, '/search/', kwpage])
    logger.info('qurl is {}'.format(qurl))
    rsp = gethtml(url=qurl, outhtml=os.path.join(STOREDPATH, kwpage))
    html = pq(rsp)
    if html('div.media-body').html() is None:
        logger.error('No result for {}'.format(kw))
        return None
    else:
        return html


def getmaxindex(html, resultnum):
    # get pagination
    if html('.pagination').html():
        alinks = [a.attr("href") for a in html('ul.pagination a').items() if a.attr('href') ]
        #last page index from href, text may be "末页" in more than 10 pages.
        lastlink = alinks[-1]
        indexpattern = r'.*_.*_(\d+).html'
        cpattern = re.compile(indexpattern)
        imatch = cpattern.search(lastlink)
        lastindex = imatch.group(1)
        #kw is just str
        logger.info("{} pages result ".format(lastindex))
        # check page
        if math.ceil(resultnum/10) > int(lastindex):
            # iterate all pages to get links
            return int(lastindex)
        else:
            return math.ceil(resultnum/10)
    else:
        #only one page or No result
        logger.info("only one page result")
        return 1


def output(results, output, pprint):
    # combine
    if pprint:
        for result in results:
            logger.info('{magneturi} {size} {date}'.format(**result))
    else:
        for i, result in enumerate(results):
            logger.info('\n{0:-^50} '.format(i+1))
            logger.info('{0: <10}: {1}'.format("magneturi", result['magneturi']))
            logger.info('{0: <10}: {1}'.format("title", result['title']))
            logger.info('{0: <10}: {1}'.format("date", result['date']))
            logger.info('{0: <10}: {1}'.format("size", result['size']))
            logger.info('{0: <10}: {1}'.format("click", result['click']))

    if output:
        postfix = output.split('.')[1]
        if postfix == 'csv':
            #open unicodecsv with binary mode, so newline is not used.
            #https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
            with open(output, mode='wb+') as csvfile:
                fieldnames = ['magneturi', 'title', 'date', 'size', 'click']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
        elif postfix == 'json':
            with open(output, mode='w+', encoding='utf-8') as jsonfile:
                # ensure_ascii=False, so output is not unicode
                if PY3k:
                    json.dump(results, jsonfile, indent=4, ensure_ascii=False)
                else:
                    # special handling for py2, io.open with utf-8, write need utf-8
                    # use json.dump will fail with TypeError: must be unicode, not str
                    resultsjson = json.dumps(results, indent=4, ensure_ascii=False)
                    jsonfile.write(resultsjson.decode('utf-8'))

@elapsedtime
def btyunso(**kwargs):
    resultnum = kwargs['number']
    kw = kwargs['keyword']
    category = BTYUNSO_SORT[kwargs['sort']]
    results = list()

    # 1. get 1st page
    # btyunso is not that good, always return 100 pages and 10 per page
    html = getvalidpage(kw, category, 1)

    # 2. check if no result
    if html is None:
        return -1
    # 3. get first page result
    # get all title, seems py2 is unicode, so convert to str
    # uri pattern is span with class media-down, a with attr title
    #<a href="/533382DBD8F54410E2F55C1057D48D958C2F09AC.html" title="bturl">
    magnetlist = ["magnet:?xt=urn:btih:" + a.attr('href')[1:].split('.')[0]
                  for a in html('span.media-down a[title]').items()]
    # py3 title.text() is str class, py2.7 title.text() is unicode
    titlelist = [title.text() for title in html('a.title').items()]
    # get date, size ,hot
    datelist = [date.text() for date in html('span.label-success').items()]
    sizelist = [size.text() for size in html('span.label-warning').items()]
    clicklist = [hot.text() for hot in html('span.label-primary').items()]

    endindex = getmaxindex(html, resultnum)
    # 3. run loop to get all results
    if endindex > 1:
        for pindex in range(2, endindex + 1):
            html = getvalidpage(kw, category, pindex)
            if html:
                # merge list
                magnetlist += ["magnet:?xt=urn:btih:" + a.attr('href').split('.')[0]
                              for a in html('span.media-down a[title]').items()]
                titlelist += [title.text() for title in html('a.title').items()]
                datelist += [date.text() for date in html('span.label-success').items()]
                sizelist += [size.text() for size in html('span.label-warning').items()]
                clicklist += [hot.text() for hot in html('span.label-primary').items()]

    # results
    for index in range(min(resultnum, len(titlelist))):
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

    if category == 'date':
        results = sorted(results, key=lambda elem: elem[category], reverse=True)
    elif category == 'click':
        results = sorted(results, key=lambda elem: int(elem[category]), reverse=True)
    elif category == 'size':
        results = sorted(results, key=lambda elem: convertsize(elem[category]), reverse=True)

    output(results, kwargs['output'], kwargs['pretty_oneline'])


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
    parser.add_argument('--number', '-n', type=int, default=5,
                        help="search result number ,default is 5")
    parser.add_argument('--output', '-o', type=outputformat,
                        help="output filename with .csv or .json, default will dump to local output dir")
    parser.add_argument('--pretty-oneline', '-p', action='store_true',
                        help='show result in oneline')
    #args = vars(parser.parse_args(['毒液', '-s', '0', '-n', '10', '-o', 'huo.json']))
    args = vars(parser.parse_args())
    logger.info(args)
    #get page category
    cq = btyunso(**args)

