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

def alt_send_POST_localis(colorstyle, version, POSTURL):
    import httplib, urllib

    POSTDATA = "'style={colorstyle}&version={version}'".format(colorstyle=colorstyle, version=version)
    params = urllib.urlencode({'style': colorstyle, 'version': version})
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    conn = httplib.HTTPConnection(POSTURL.split('/')[:-1])
    conn.request("POST", "/BnCClear2.php", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    if response.status == 200:
        
    #200 OK
         data = response.read()
         print data
    
    conn.close()


def send_purge_request_localis(colorstyle, version, POSTURL):
    import re
    if colorstyle != "" and version != "":
        import pycurl,json
        #BNCPHP = "http://clearcache.bluefly.corp/BnCClear2.php"
        #POSTDATA = "'style={colorstyle}&version={version}'".format(colorstyle=colorstyle, version=version)
        #POSTDATA = "'{colorstyle} {version}'".format(colorstyle=colorstyle, version=version)
        ## Create send data
        #data = json.dumps({
        #'style' : colorstyle,
        #'version' : version
        #})
#       
        POSTURL_Referer = POSTURL.replace('Clear2.php', 'Clear1.php')
        
        regex = re.compile(r'.+?Mobile.+?')
        if re.findall(regex, POSTURL):
            data = "style={0}".format(colorstyle)
            # Replace Previous Line with uncommenting next line when versioning is added to mobile
            # Currently only need to POST Colorstyle to PHP script       
            ## data = "style={0}&version={1}".format(colorstyle, version)
        else:
            data = "style={0}&version={1}".format(colorstyle, version) 
        
        head_contenttype = 'Content-Type: application/x-www-form-urlencoded'
        head_content_len= "Content-length: {0}".format(str(len(data)))
        #head_accept = 'Accept: text/html'
        head_accept = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        head_useragent = 'User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0'
        head_referer = 'Referer: {0}'.format(POSTURL_Referer)
        c = pycurl.Curl()
        c.setopt(c.URL, POSTURL)
        c.setopt(pycurl.HEADER, 0)
        #c.setopt(pycurl.INFOTYPE_HEADER_OUT, 1)
        #c.setopt(pycurl.RETURNTRANSFER, 1)
        c.setopt(pycurl.FORBID_REUSE, 1)
        c.setopt(pycurl.FRESH_CONNECT, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.HTTPHEADER, [head_useragent, head_referer, head_contenttype, head_accept, head_content_len])
        #c.setopt(c.POSTFIELDS, POSTDATA)
        c.setopt(c.VERBOSE, True)
        c.perform()
        c.close()
        print "Successfully Sent Local Purge Request for --> Style: {0} Ver: {1}".format(colorstyle, version)
        #head_authtoken = "Authorization: tok:{0}".format(token)
        #head_content_len= "Content-length: {0}".format(str(len(POSTDATA)))
        #head_accept = 'Accept: application/json'
        #head_contenttype = 'Content-Type: application/json'


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
#url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid
url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid

#url_colorstyle_pdp = 'http://www.belleandclive.com/browse/product.jsp?id=' + colorstyle

## Get all Img links on List page
listpage_urllist = url_get_links(url_catid)

## Parse urllist returning only versioned List page images
versioned_links = return_versioned_urls(listpage_urllist)
#count = 0


## purge prev if not deployed yet
if not versioned_links:
    url_catid = 'http://prev.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid
    listpage_urllist = url_get_links(url_catid)
    versioned_links = return_versioned_urls(listpage_urllist)
    

if len(versioned_links) <= 250:

    regex = re.compile(r'(.+?=)([0-9]{9})(.+?)(ver=[0-9][0-9]?[0-9]?[0-9]?)')
    for url_purge_local in versioned_links:
        colorstyle = re.findall(regex, url_purge_local[0])
        colorstyle = colorstyle.pop()[1]
        version  = re.findall(regex, url_purge_local[0])
        version = version.pop()[-1].split('=')[-1]
        #print "{0} and version num {1}".format(colorstyle,version)
        #try:
        POSTURL_BNC = "http://clearcache.bluefly.corp/BnCClear2.php"
        POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
        send_purge_request_localis(colorstyle,version,POSTURL_BNC)
        send_purge_request_localis(colorstyle,version,POSTURL_Mobile)
        #except:
        #    print sys.stderr().read()
    for url_purge in versioned_links:
        send_purge_request_edgecast(url_purge[0].replace('http://is.', 'http://cdn.is.'))
        csv_write_datedOutfile(url_purge)

else:
    print "Failed -- Over 250 URLs Submitted"    




