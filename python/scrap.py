import os
import sys
import pdb

var1 = pdb
print(var1)



LoadModule wsgi_module modules/mod_wsgi.so


WSGIScriptAlias /appname /var/www/webpy-app/code.py/

Alias /appname/static /var/www/webpy-app/static/

AddType text/html .py

<Directory /var/www/webpy-app/>
    Order deny,allow
    Allow from all
</Directory>

fileslink = 'https://www.yousendit.com/directDownload?phi_action=app/directDownload&fl=SWhZekZtSyt5UkhLd05OU01JMXhkak9ycmd5and0SUoxejIzQTdDU0tWVi9EYXJLTVl4UVV1S2FEaFlMcmo0ckFGTEFGTDkzQndJakt5TEJJTDNwWTA0bnFzcHZDbFlaMFlDWmNBPT0&experience=bas'
s = requests.Session()
#s.auth = ('user', 'pass')
s.headers.update({'User-Agent': 'Mozilla/5.0')})

# both 'x-test' and 'x-test2' are sent
s.get(fileslink)


def url2_download_read_http(targeturl):
    try:
        from time import time
        import urllib2, subprocess
        import requests
        import urllib2
#        request = urllib2.Request("http://www.google.com", headers={"User Agent" : "text/html"})
#        contents = urllib2.urlopen(request).read()
#        url_start = time()
        #targetreq = urllib2.Request(targeturl)
        #downloadfile = urllib2.urlopen(targetreq).read()
#        req = urllib2.Request(targeturl)
        req = targeturl
#        req.add_unredirected_header('User-Agent', 'Mozilla/5.0')
#        req.add_unredirected_header('Content-Type', 'text/html;charset=utf-8')
#        urllib2.urlopen(req)
        headers = {'User-agent': 'Mozilla/5.0', 'Content-Type': 'text/html;charset=utf-8'}
        req = requests.get(targeturl, headers=headers)
        response = req.text
        return respo	
#        headers = {'User-agent': 'Mozilla/5.0', 'Content-Type': 'text/html;charset=utf-8'}
#        eq = requests.get(targeturl, headers=headers)
#        req = requests.get(link_testreq, headers=headers)
#        response = req.text
#        
#        s = requests.Session()
#        s.auth = ('user', 'pass')
#        s.headers.update({'User-Agent': 'Mozilla/5.0')})
#        s.get(fileslink)
        url_end = time()
        print "Download Time -> %s"  % (url_end - url_start)
#        l = []
#        for f in response:
#            l.append(f)
#        print len(l)
        return response
    except TypeError:
        print "Unicode Obj Error"



def html_parse_yousend_images_https(htmlpage):
    domain = 'www.yousendit.com'
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmlpage)
    links = []
    for link in soup.find_all('a'):
        try:
            domain = str('https://' + domain)
            hrefstr = link.get('href')
            filenm = link.get('title')
            if not hrefstr:
                print "No Href Found"
            if not filenm:
                        print "No title attribute Found"
            lastp = str(hrefstr)
            dload = str(domain + "/" + lastp + "/" + filenm)
            import re
            regex = re.compile(r'http.+?')
            found = re.findall(regex, dload)
            linksret = links.append(found)
            print list(linksret)
        except TypeError:
            print "Tags Missing"
    return list(linksret)

        
# This scripts shows how to crawl a site without settings up a complete project.
# 
# Note: the `crawler.start()` can't be called more than once due twisted's reactor limitation.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Rolando Espinoza La fuente
#
# Changelog:
#     24/07/2011 - updated to work with scrapy 13.0dev
#     25/08/2010 - initial version. works with scrapy 0.9

from scrapy.contrib.loader import XPathItemLoader
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider


class QuestionItem(Item):
    """Our SO Question Item"""
    title = Field()
    summary = Field()
    tags = Field()

    user = Field()
    posted = Field()

    votes = Field()
    answers = Field()
    views = Field()


class MySpider(BaseSpider):
    """Our ad-hoc spider"""
    name = "myspider"
    start_urls = ["http://stackoverflow.com/"]

    question_list_xpath = '//div[@id="content"]//div[contains(@class, "question-summary")]'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        for qxs in hxs.select(self.question_list_xpath):
            loader = XPathItemLoader(QuestionItem(), selector=qxs)
            loader.add_xpath('title', './/h3/a/text()')
            loader.add_xpath('summary', './/h3/a/@title')
            loader.add_xpath('tags', './/a[@rel="tag"]/text()')
            loader.add_xpath('user', './/div[@class="started"]/a[2]/text()')
            loader.add_xpath('posted', './/div[@class="started"]/a[1]/span/@title')
            loader.add_xpath('votes', './/div[@class="votes"]/div[1]/text()')
            loader.add_xpath('answers', './/div[contains(@class, "answered")]/div[1]/text()')
            loader.add_xpath('views', './/div[@class="views"]/div[1]/text()')

            yield loader.load_item()


def main():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    def catch_item(sender, item, **kwargs):
        print "Got:", item

    dispatcher.connect(catch_item, signal=signals.item_passed)

    # shut off log
    from scrapy.conf import settings
    settings.overrides['LOG_ENABLED'] = False

    # set up crawler
    from scrapy.crawler import CrawlerProcess

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(MySpider())

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print "ENGINE STOPPED"


if __name__ == '__main__':
    main()


for link in soup.find_all('a'):
    print(link.get('href'))
soup.find_all("title")
import codecs
f = codecs.open(soup, encoding='utf8')


response  = requests.get(url, headers = user_agent, config=debug)