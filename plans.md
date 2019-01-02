# torrent_cli cmd tool used to crawl magnet uri
## Plans
- websites include cloudflare protected like https://torrentkitty.tv/search/ and others like http://www.btyunsou.co 
- compatiable with python 2.7/3+
- unittests
## DONE
* http://www.btyunsou.co/
    * validate the search uri
    * ctime, click, length
        * store in config.yml
    * mirror a site to do unittest
    * store hot search
    * add argparser

## TODO
* http://www.seaomc.com/archives/4168.html
    * http://cnbtkitty.pw/
    * http://www.diaosisou.biz
    * https://www.torrentkitty.tv/search/
    * add compare in excel
    * store old in redis
* http://cnbtkitty.pw/
    * post / with form data and 302 return search html
    * max pages 1000 will be displayed.
* define a search engine class
    * base url
    * search path
    * keyword
    * result uri
* store search result in db, display in web gui.
 