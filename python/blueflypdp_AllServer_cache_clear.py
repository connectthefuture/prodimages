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
    
    

def return_cleaned_bfly_urls(text):
    regex = re.compile(r'http:.+?mgen/Bluefly/.+?')
    listurls = []
    for line in text:
        testfind =  regex.findall(line)
        if testfind:
            listurls.append(testfind)
            #print testfind
        else:
            pass
    return listurls

    
    
def send_purge_request_localis(colorstyle, version, POSTURL):
    if colorstyle != "" and version != "":
        import pycurl,json
        
        #BNCPHP = "http://clearcache.bluefly.corp/BFClear2.php"
        #POSTDATA = "'style={colorstyle}&version={version}'".format(colorstyle=colorstyle, version=version)
        #POSTDATA = "'{colorstyle} {version}'".format(colorstyle=colorstyle, version=version)
        ## Create send data
        #data = json.dumps({
        #'style' : colorstyle,
        #'version' : version
        #})
        POSTURL_Referer = POSTURL.replace('Clear2.php', 'Clear1.php')
        
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
colorstyle_list = sys.argv[1:]

alturl = 'altimage.ms'


#catid = get_catid_from_eventid(eventid)
## Join Catid to BC Url
#url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid
#url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid



#www.bluefly.com/Harrison-pink-check-classic-fit-dress-shirt/p/323108302/detail.fly

#url_colorstyle_pdp = 'http://www.belleandclive.com/browse/product.jsp?id=' + colorstyle

## Get all Img links on PDP and append only the primary image urls and versions
## Then tack the generated urls for edgecast to list
pdp_urllist = []
edgecast_listurls = []

for colorstyle in colorstyle_list:
    bflypdp_url = "http://www.bluefly.com/Bluefly-generic-pdp-slug/p/{0}/detail.fly".format(colorstyle)
    found_links = url_get_links(bflypdp_url)
    for link in found_links:
        if colorstyle in link:
            pdp_urllist.append(link)
            ## Create list page urls for Edgecast
            if alturl not in link:
                oldlistpg = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=157&height=188'.format(colorstyle)
                newlistpg = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(colorstyle)
                
#                newlistpg = '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt01.pct&outputx=1800&outputy=2160&level=1&ver=1'
#                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt02.pct&outputx=1800&outputy=2160&level=1&ver=1'
#                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt03.pct&outputx=1800&outputy=2160&level=1&ver=1'
#                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt04.pct&outputx=1800&outputy=2160&level=1&ver=1'.format(colorstyle, version)
#                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt05.pct&outputx=1800&outputy=2160&level=1&ver=1'.format(colorstyle, version)
#                
#                
#                
#                '/mgen/Bluefly/altimage.ms?img=325084201_alt05.jpg&w=75&h=89&ver=1'.format(colorstyle, version)
#                
#                
#                '/mgen/Bluefly/eqzoom85.ms?img={0}_alt05.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
#                
#                
#                
                
                edgecast_listurls.append(oldlistpg)
                edgecast_listurls.append(newlistpg)





## Parse urllist returning only versioned List page images
versioned_links = return_versioned_urls(pdp_urllist)

#print versioned_links
count = 0
if len(versioned_links) <= 150:

    regex = re.compile(r'(.+?=)([0-9]{9})(.+?)(ver=[0-9][0-9]?[0-9]?[0-9]?)')
    for url_purge_local in versioned_links:
        colorstyle = re.findall(regex, url_purge_local[0])
        colorstyle = colorstyle.pop()[1]
        version  = re.findall(regex, url_purge_local[0])
        version = version.pop()[-1].split('=')[-1]
        #print "{0} and version num {1}".format(colorstyle,version)
        #try:
        POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
        POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
        send_purge_request_localis(colorstyle,version,POSTURL_BFY)
        send_purge_request_localis(colorstyle,version,POSTURL_Mobile)
        #except:
        #    print sys.stderr().read()
    for url_purge in versioned_links:
        send_purge_request_edgecast(url_purge[0])
        #csv_write_datedOutfile(url_purge)

else:
    print "Failed -- Over 100 URLs Submitted"    



## Now clear links from the generated urls
#generated_links = return_cleaned_bfly_urls(edgecast_listurls)

#print generated_links
count = 0
if len(edgecast_listurls) <= 100:

    #regex = re.compile(r'(.+?=)([0-9]{9})(.+?)(ver=[0-9][0-9]?[0-9]?[0-9]?)')

### DO NOT NEED TO CLEAR IS SERVERS SINCE ABOVE CLEARS ALL BASED ON STYLE AND VERSION, NOT URL
#
#    for url_purge_local in edgecast_listurls:
#        colorstyle = re.findall(regex, url_purge_local[0])
#        colorstyle = colorstyle.pop()[1]
#        version  = re.findall(regex, url_purge_local[0])
#        version = version.pop()[-1].split('=')[-1]
#        #print "{0} and version num {1}".format(colorstyle,version)
#        #try:
#        send_purge_request_localis(colorstyle,version)
        #except:
        #    print sys.stderr().read()
####
    for url_purge in edgecast_listurls:
        send_purge_request_edgecast(url_purge)
        #csv_write_datedOutfile(url_purge)

else:
    print "Failed -- Over 100 URLs Submitted"    


#print edgecast_listurls

