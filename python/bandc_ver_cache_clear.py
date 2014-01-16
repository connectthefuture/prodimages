#!/usr/bin/env python

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
    return set(linklist)


def return_versioned_urls(text):
    regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')
    listurls = []
    for line in text:
        testfind =  regex.findall(line)
        if testfind:
            listurls.append(testfind)
            #print testfind
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
    if len(eventid) == 4:
        import sqlalchemy
        orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
        connection = orcl_engine.connect()
        eventid = str(eventid)
        eventid_tocatid_query = "SELECT DISTINCT POMGR.EVENT.CATEGORY FROM POMGR.EVENT WHERE POMGR.EVENT.ID = '" + eventid + "'"
    #print eventid_tocatid_query
        for row in connection.execute(eventid_tocatid_query):
            catid = row['category']
    else:
        catid = eventid
    if catid:
        return catid
    else:
        print "Event {0} has not been pushed to ATG yet".format(eventid)


def send_purge_request_edgecast(mediaPath):
    import pycurl,json,sys,os
    ## Setup variables
    token = "9af6d09a-1250-4766-85bd-29cebf1c984f"
    account = "4936"
    mediaType = "8"

    purgeURL = "https://api.edgecast.com/v2/mcc/customers/{0}/edge/purge".format(account)

    if token != "" and account != "" and mediaPath != "" and mediaType != "":
        ## Create send data
        data = json.dumps({
        'MediaPath' : mediaPath,
        'MediaType' : mediaType 
        })
        #data = json_encode(request_params)
        head_authtoken = "Authorization: tok:{0}".format(token)
        head_content_len= "Content-length: {0}".format(str(len(data)))
        head_accept = 'Accept: application/json'
        head_contenttype = 'Content-Type: application/json'
        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.setopt(pycurl.URL, purgeURL)
        c.setopt(pycurl.PORT , 443)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.HEADER, 0)
        #c.setopt(pycurl.INFOTYPE_HEADER_OUT, 1)
        #c.setopt(pycurl.RETURNTRANSFER, 1)
        c.setopt(pycurl.FORBID_REUSE, 1)
        c.setopt(pycurl.FRESH_CONNECT, 1)
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")
        c.setopt(pycurl.POSTFIELDS,data)
        c.setopt(pycurl.HTTPHEADER, [head_authtoken, head_contenttype, head_accept, head_content_len])
        try:
            c.perform()
            c.close()
            print "Successfully Sent Purge Request for --> {0}".format(mediaPath)
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr


############ RUN ###########

import sys,re,os
eventid = sys.argv[1]

catid = get_catid_from_eventid(eventid)
## Join Catid to BC Url
url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid

#url_colorstyle_pdp = 'http://www.belleandclive.com/browse/product.jsp?id=' + colorstyle

## Get all Img links on List page
listpage_urllist = url_get_links(url_catid)

## Parse urllist returning only versioned List page images
versioned_links = return_versioned_urls(listpage_urllist)
#count = 0
if len(versioned_links) <= 100:

    regex = re.compile(r'(.+?=)([0-9]{9})(.+?)(ver=[0-9]+?)')
#    for url_purge_local in versioned_links:
#        url = url_purge_local.split('=')
#        colorstyle = re.findall(regex, url)
#        #colorstyle = colorstyle.group[1]
#        #version = re.match(regex, url_purge_local)
#        #version = version.group[-1]
#        #colorstyle = url_purge_local.split()
#        version  = re.findall(regex, url)
#        print "{0} and version num {1}".format(colorstyle,version) 
    for url_purge in versioned_links:
        send_purge_request_edgecast(url_purge[0])
        csv_write_datedOutfile(url_purge)

else:
    print "Failed -- Over 100 URLs Submitted"    
