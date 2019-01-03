# -*- encoding=utf-8 -*-
# author: zhihuaye@gmail.com

# just a simple draft
# flow is get __cfduid via calculate the challenge
#         get cf_clearance in 302
#
# two ways:
# 1.0  https://github.com/Anorov/cloudflare-scrape, extra node js should be installed , use node js
# 1.1  use execute_script to replace the node
# 2.  https://stackoverflow.com/questions/5799228/how-to-get-status-code-by-using-selenium-py-python-code/39991889#39991889
# use selenium to emulate the js and use get_log to retrive the cookies,
# but cf need cf_clearance indeed, no way to get cf_clearance.
# some ideas: https://github.com/webdriverio/webdriverio/issues/1003
#   or use https://github.com/cryzed/Selenium-Requests to get detailed rsp including redirect
#


# TODO:
# 1. add logic to store cookies and validate logic

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1024x1400")
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'performance':'ALL', 'browser':'ALL' }

# download Chrome Webdriver
# https://sites.google.com/a/chromium.org/chromedriver/download
# put driver executable file in the script directory
chrome_driver = os.path.join(os.getcwd(), "chromedriver")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver, desired_capabilities=d)


'''
#can also borrow idea from https://github.com/Anorov/cloudflare-scrape
reuse the code to gen the challange answer.
val=driver.execute_script("return 5")
print(val)
'''

#
#
driver.get("https://torrentkitty.tv/search/")
print(driver.page_source)

def noform(d):
    form = d.find_elements_by_id('challenge-form')
    if(len(form)):
        print(form)
        return False
    else:
        return True

def getHttpResponseHeader(browser):
    for responseReceived in browser.get_log('performance'):
        #dig into this response to get cookies
        #{'level': 'INFO', 'message':
        # {'level': 'INFO',
        # 'message': '{"message":{"method":"Network.responseReceived","params":{"frameId":"CB24C8783AA18D102A6D031A579FF153","loaderId":"ED3F2B21CA82C258370CBB2ED2341E06","requestId":"ED3F2B21CA82C258370CBB2ED2341E06","response":{"connectionId":15,"connectionReused":true,"encodedDataLength":211,"fromDiskCache":false,"fromServiceWorker":false,"headers":{"cache-control":"public, max-age=3600","cf-cache-status":"HIT","cf-ray":"4933b579c91745c0-TPE","content-encoding":"br","content-type":"text/html","date":"Thu, 03 Jan 2019 07:21:29 GMT","expect-ct":"max-age=604800, report-uri=\\"https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct\\"","expires":"Thu, 03 Jan 2019 08:21:29 GMT","pragma":"no-cache","server":"cloudflare",
        # "set-cookie":"__cfduid=db92ba758128859a510ce7c26ebe9b07a1546500089; expires=Fri, 03-Jan-20 07:21:29 GMT; path=/; domain=.torrentkitty.tv; HttpOnly","status":"200","vary":"Accept-Encoding","x-powered-by":"PHP/5.4.45"},"mimeType":"text/html","protocol":"h2","remoteIPAddress":"104.28.0.185","remotePort":443,"requestHeaders":{":authority":"www.torrentkitty.tv",":method":"GET",":path":"/search/",":scheme":"https","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-encoding":"gzip, deflate, br","upgrade-insecure-requests":"1","user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/71.0.3578.98 Safari/537.36"},"securityDetails":{"certificateId":0,"certificateTransparencyCompliance":"unknown","cipher":"AES_128_GCM","issuer":"COMODO ECC Domain Validation Secure Server CA 2","keyExchange":"ECDHE_ECDSA","keyExchangeGroup":"X25519","protocol":"TLS 1.2","sanList":["sni66758.cloudflaressl.com","*.1250foxsports.com","*.13n.com","*.141592653.com","*.141592653.net","*.141av.com","*.141jav.com","*.141tube.com","*.1428elm.com","*.1431am.gr","*.144l.com","*.avbye.com","*.basskubtole.tk","*.dramabox.se","*.erolivedoor.com","*.eromaka.com","*.horecaconnect.com","*.hostviconra.tk","*.jav28.com","*.javbed.com","*.javbye.com","*.javcab.com","*.javpal.com","*.javpoo.com","*.javsss.com","*.javtiger.com","*.javyes.com","*.javzen.com","*.mycountry961.com","*.ouibeauty.com","*.quebuena106.com","*.schusrecttibxi.cf","*.sosomagnet.com","*.stewpidvideos.ga","*.takykeduxeqamu.tk","*.torrent28.com","*.torrentkitty.com","*.torrentkitty.me","*.torrentkitty.net","*.torrentkitty.org","*.torrentkitty.tv","*.tristateswolf.com","*.venturemail.nz","*.wajr.com","*.wjmsam.com","*.wkkwfm.com","*.womecimi.tk","*.wvaq.com","*.ybideresefofy.tk","*.ypdroolmidpho.tk","1250foxsports.com","13n.com","141592653.com","141592653.net","141av.com","141jav.com","141tube.com","1428elm.com","1431am.gr","144l.com","avbye.com","basskubtole.tk","dramabox.se","erolivedoor.com","eromaka.com","horecaconnect.com","hostviconra.tk","jav28.com","javbed.com","javbye.com","javcab.com","javpal.com","javpoo.com","javsss.com","javtiger.com","javyes.com","javzen.com","mycountry961.com","ouibeauty.com","quebuena106.com","schusrecttibxi.cf","sosomagnet.com","stewpidvideos.ga","takykeduxeqamu.tk","torrent28.com","torrentkitty.com","torrentkitty.me","torrentkitty.net","torrentkitty.org","torrentkitty.tv","tristateswolf.com","venturemail.nz","wajr.com","wjmsam.com","wkkwfm.com","womecimi.tk","wvaq.com","ybideresefofy.tk","ypdroolmidpho.tk"],"signedCertificateTimestampList":[],"subjectName":"sni66758.cloudflaressl.com","validFrom":1536192000,"validTo":1552694399},"securityState":"secure","status":200,"statusText":"","timing":{"connectEnd":-1,"connectStart":-1,"dnsEnd":-1,"dnsStart":-1,"proxyEnd":-1,"proxyStart":-1,"pushEnd":0,"pushStart":0,"receiveHeadersEnd":230.099,"requestTime":432178.002945,"sendEnd":7.915,"sendStart":7.707,"sslEnd":-1,"sslStart":-1,"workerReady":-1,"workerStart":-1},"url":"https://www.torrentkitty.tv/search/"},"timestamp":432178.233544,"type":"Document"}},"webview":"CB24C8783AA18D102A6D031A579FF153"}',
        # 'timestamp': 1546500090074}
        print(responseReceived)

        try:
            response = json.loads(responseReceived['message'])['message']['params']['response']
            return response
        except:
            pass
    return None
try:
    WebDriverWait(driver, 6, 0.5).until(noform)
    print(driver.page_source)
    rsp = getHttpResponseHeader(driver)
    print(rsp['headers']['set-cookie'])
finally:
    driver.close() # close the driver

if __name__ == '__main__':
    pass