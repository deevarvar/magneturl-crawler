# torrent_cli cmd tool used to crawl magnet uri
## Plans
- websites include cloudflare protected like https://torrentkitty.tv/search/ and others like http://www.btyunsou.co 
- compatiable with python 2.7/3+
- unittests
## DONE
- use yaml as config file
- pyquery to get entry url


## TODO
* http://www.btyunsou.co/
    * validate the search uri
    * ctime, click, length
        * store in config.yml
    * mirror a site to do unittest
    * store hot search
    * add argparser
* define a search engine class
    * base url
    * search path
    * keyword
    * result uri
* store search result in db, display in web gui.
 