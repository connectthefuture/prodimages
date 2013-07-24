#!/usr/bin/env python
import sys,re,os

def url_get_links(targeturl):
    import os,re,sys,requests
    from bs4 import BeautifulSoup
    r = requests.get(targeturl)
    soup = BeautifulSoup(r.text,"html.parser")
    ###  soup is now Full HTML of target -- Below creates/returns list of unique links
    linklist = []
    for link in soup.find_all('img'):
        linklist.append(link.get('src'))
        sorted(linklist)
    ## Return list of unique links
    return list(set(linklist))



def return_versioned_url(text):
    regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')
    listurls = []
    for line in text:
        testfind =  regex.findall(line)
        if testfind:
            listurls.append(testfind)
            print testfind
        else:
            pass
    return listurls


def csv_write_datedOutfile(lines):
    import csv,datetime,os
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_belleclive_urls.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter='\n')
            writer.writerows([lines])


def get_catid_from_eventid(eventid):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@192.168.30.165:1531/bfyprd12')
    connection = orcl_engine.connect()
    eventid = str(eventid)
    eventid_tocatid_query = "SELECT DISTINCT POMGR.EVENT.CATEGORY FROM POMGR.EVENT WHERE POMGR.EVENT.ID = '" + eventid + "'"
    #print eventid_tocatid_query
    for row in connection.execute(eventid_tocatid_query):
        catid = row['category']
    if catid:
        return catid
    else:
        print "Event {0} has not been pushed to ATG yet".format(eventid)

#urls = bandc_return_versioned_url_listpage(htmlfile)


#print len(urls)

#'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=cat1670052'

#htmlfile = sys.argv[1]
eventid = sys.argv[1]

catid = get_catid_from_eventid(eventid)
## Join Catid to BC Url
url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid

#url_colorstyle_pdp = 'http://www.belleandclive.com/browse/product.jsp?id=' + colorstyle

## Get all Img links on List page
listpage_urllist = url_get_links(url_catid)

## Parse urllist returning only versioned List page images
versioned_links = return_versioned_url(listpage_urllist)
#count = 0
if len(versioned_links) <= 50:

    for line in versioned_links:
        print "Formatted {0}".format(str(line))
    #csv_write_datedOutfile(line)


