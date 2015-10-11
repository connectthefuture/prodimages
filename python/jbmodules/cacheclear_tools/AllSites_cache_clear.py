#!/usr/bin/env python
# -*- coding: utf-8 -*-

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



def return_versioned_urls(text):
    import os,sys,re
    regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')
    regex_swatch = re.compile(r'^http.*mgen/Bluefly/swatch.ms\?productCode=[0-9]{9}&width=49&height=59.*$')
    listurls = []
    for line in text:
        testfind =  regex.findall(line)
        testswatch = regex_swatch.findall(line)
        if testfind:
            listurls.append(testfind)
            #print testfind
        if testswatch:
            listurls.append(testswatch)
    return listurls
    
    

def return_cleaned_bfly_urls(text):
    import os,sys,re
    regex = re.compile(r'http:.+?mgen/Bluefly/.+?')
    listurls = []
    for line in text:
        testfind =  regex.findall(line)
        if testfind:
            listurls.append(testfind)
            #print testfind

    return listurls

    
    
def send_purge_request_localis(colorstyle, version, POSTURL):
    if colorstyle != "" and version != "":
        import pycurl,json,re

        ## Create send data
        #data = json.dumps({
        #'style' : colorstyle,
        #'version' : version
        #})
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
def main():
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
    regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')

    for colorstyle in colorstyle_list:
        bflypdp_url = "http://www.bluefly.com/Bluefly-generic-pdp-slug/p/{0}/detail.fly".format(colorstyle)
        found_links = url_get_links(bflypdp_url)
        for link in found_links:
            if colorstyle in link:
                pdp_urllist.append(link)
                vertest=link.split('&')[-1]
                version = ''
                if vertest[:4] == 'ver=':
                    version = vertest[-1]
                ## Create and append to edgecast list page urls for Edgecast
                if alturl not in link:
                    oldlistpg     =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=157&height=188'.format(colorstyle)
                    newlistpg     =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(colorstyle)
                    pdpg          =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
                    pmlistpg      =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=50&height=60&ver=null'.format(colorstyle)
                    pmeventimg    =   'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=200&outputy=240&level=1&ver=null'.format(colorstyle)
                    email_img     =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=140&height=182'.format(colorstyle)
                    email_img1     = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=140&height=182'.format(colorstyle)
                    email_img2     =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=200&height=250'.format(colorstyle)

                    edgecast_listurls.append(oldlistpg)
                    edgecast_listurls.append(newlistpg)
                    edgecast_listurls.append(pdpg)
                    edgecast_listurls.append(pmlistpg)
                    edgecast_listurls.append(pmeventimg)
                    edgecast_listurls.append(email_img1)
                    edgecast_listurls.append(email_img2)

                if version:
                    ### ZOOM HI REZ
                    pdpZOOM   = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                    edgecast_listurls.append(pdpZOOM)
                    testurl='http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt01.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                    ### ALT 1
                    if testurl in pdp_urllist:
                        pdpalt01z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt01z)
                        pdpalt01l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt01l)
                        print "SUCCESS1"
                        #'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
                    
                    ### ALT 2
                    if testurl.replace('_alt01','_alt02') in pdp_urllist:
                        pdpalt02z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt02.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt02z)
                        pdpalt02l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt02.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt02l)
                        print "SUCCESS2"
                    ### ALT 3
                    if testurl.replace('_alt01','_alt03') in pdp_urllist:
                        pdpalt03z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt03.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt03z)
                        pdpalt03l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt03.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt03l)
                        print "SUCCESS3"
                    ### ALT 4
                    if testurl.replace('_alt01','_alt04') in pdp_urllist:
                        pdpalt04z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt04.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt04z)
                        pdpalt04l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt04.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt04l)
                        print "SUCCESS4"
                    ### ALT 5
                    if testurl.replace('_alt01','_alt05') in pdp_urllist:
                        pdpalt05z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt05.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt05z)
                        pdpalt05l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt05.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                        edgecast_listurls.append(pdpalt05l)
                        print "SUCCESS5"
                    ## Unique Set
                    edgecast_listurls = list(set(edgecast_listurls))
                    print pdp_urllist

    #                newlistpg = '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt01.pct&outputx=1800&outputy=2160&level=1&ver=1'
    #                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt02.pct&outputx=1800&outputy=2160&level=1&ver=1'
    #                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt03.pct&outputx=1800&outputy=2160&level=1&ver=1'
    #                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt04.pct&outputx=1800&outputy=2160&level=1&ver=1'.format(colorstyle, version)
    #                '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt05.pct&outputx=1800&outputy=2160&level=1&ver=1'.format(colorstyle, version)
    #                           ## 75x89 not needed as it is added to url list during the scraping of PDP
                    #pdpalt01t = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt01.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                    #pdpalt02t = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt02.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                    #pdpalt03t = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt03.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                    #pdpalt04t = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt04.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                    #pdpalt05t = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt05.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                    ##edgecast_listurls.append(pdpalt01t)
      
    #                for alturls in [pdpalt01z,pdpalt01l,pdpalt01t,pdpalt02z,pdpalt02l,pdpalt02t,pdpalt03z,pdpalt03l,pdpalt03t,pdpalt04z,pdpalt04l,pdpalt04t,pdpalt05z,pdpalt05l,pdpalt05t]:
    #                    edgecast_listurls.append(alturls)  
    #                pmlistpage='http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode=331460101&width=50&height=60'
    #                
    #                '/mgen/Bluefly/altimage.ms?img=325084201_alt05.jpg&w=75&h=89&ver=1'.format(colorstyle, version)
    #                
    #                
    #                '/mgen/Bluefly/eqzoom85.ms?img={0}_alt05.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
    #                
    #                
    #                
                    



    ## Parse urllist returning only versioned List page images
    versioned_links = return_versioned_urls(pdp_urllist)

    #print versioned_links
    count = 0
    if not versioned_links:
        import time
        for x in xrange.__reversed__(xrange(5)):
            print "Product is not Live. Skipping Edgecast CDN Purge Commencing Local Purge of {0} styles in ... {1}".format(len(colorstyle_list), x+1)
            time.sleep(.85)
        for colorstyle in colorstyle_list:
            version= "1"
            POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
            POSTURL_BC = "http://clearcache.bluefly.corp/BnCClear2.php"
            POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
            send_purge_request_localis(colorstyle,version,POSTURL_BFY)
            send_purge_request_localis(colorstyle,version,POSTURL_BC)
            send_purge_request_localis(colorstyle,version,POSTURL_Mobile)

    elif len(versioned_links) <= 4550:

        regex = re.compile(r'(.+?=)([0-9]{9})(.+?)(ver=[0-9][0-9]?[0-9]?[0-9]?)')
        for url_purge_local in versioned_links:
            try:
                colorstyle = re.findall(regex, url_purge_local[0])
                colorstyle = colorstyle.pop()[1]
                version  = re.findall(regex, url_purge_local[0])
                version = version.pop()[-1].split('=')[-1]
                #print "{0} and version num {1}".format(colorstyle,version)
                #try:
                POSTURL_ALLSITES = "http://clearcache.bluefly.corp/ClearAll2.php"
                POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
                POSTURL_BC = "http://clearcache.bluefly.corp/BnCClear2.php"
                POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
                
                send_purge_request_localis(colorstyle,version,POSTURL_ALLSITES)
                #send_purge_request_localis(colorstyle,version,POSTURL_BFY)
                #send_purge_request_localis(colorstyle,version,POSTURL_BC)
                #send_purge_request_localis(colorstyle,version,POSTURL_Mobile)
                
                #except:
                #    print sys.stderr().read()
            except IndexError:
                import time
                for x in xrange.__reversed__(xrange(5)):
                    print "Product is not Live. Skipping Edgecast CDN Purge Will Do Local Purge in ... {0}".format(x+1)
                    time.sleep(.75)
                POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
                POSTURL_BC = "http://clearcache.bluefly.corp/BnCClear2.php"
                POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
#                version = '1'
#                send_purge_request_localis(colorstyle,version,POSTURL_BFY)
#                send_purge_request_localis(colorstyle,version,POSTURL_BC)
#                send_purge_request_localis(colorstyle,version,POSTURL_Mobile)
                pass
        for url_purge in versioned_links:
            send_purge_request_edgecast(url_purge[0])
            #csv_write_datedOutfile(url_purge)

    else:
        print "Failed -- Over 4550 URLs Submitted"    



    ## Now clear links from the generated urls
    #generated_links = return_cleaned_bfly_urls(edgecast_listurls)

    #print generated_links
    count = 0
    if len(edgecast_listurls) <= 3550:

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
        for url_purge in set(sorted(edgecast_listurls)):
            send_purge_request_edgecast(url_purge)
            #csv_write_datedOutfile(url_purge)

    else:
        print "Failed -- Over 3550 URLs Submitted"    


#print edgecast_listurls

if __name__ == '__main__':
    main()
