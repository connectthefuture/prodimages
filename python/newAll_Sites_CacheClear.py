#!/usr/bin/env python
# -*- coding: utf-8 -*-

def query_version_number(colorstyle):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()

    querymake_version_number = "SELECT DISTINCT POMGR.PO_LINE.PRODUCT_COLOR_ID as colorstyle,  POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.VERSION as version FROM POMGR.PRODUCT_COLOR RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID RIGHT JOIN POMGR.PO_HDR ON POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID RIGHT JOIN POMGR.VENDOR ON POMGR.VENDOR.ID = POMGR.PO_HDR.VENDOR_ID INNER JOIN POMGR.LK_PO_TYPE ON POMGR.LK_PO_TYPE.ID = POMGR.PO_HDR.PO_TYPE_ID LEFT JOIN POMGR.INVENTORY ON POMGR.INVENTORY.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID LEFT JOIN POMGR.PRODUCT_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_DETAIL.PRODUCT_ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PRODUCT_COLOR_ID LIKE '%{0}%' ORDER BY POMGR.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last, POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last".format(colorstyle)

    result = connection.execute(querymake_version_number)
    styles = {}
    for row in result:
        style_info = {}
        style_info['version'] = row['version']
        # Convert Colorstyle to string then set as KEY
        styles[str(row['colorstyle'])] = style_info

    connection.close()
    return styles


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
def main(colorstyle_list=None):
    import sys,re,os

    if not colorstyle_list:
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
    listonly_urllist = []
    edgecast_listurls = []
    regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')

    for colorstyle in colorstyle_list:
        bflypdp_url = "http://www.bluefly.com/Bluefly-generic-pdp-slug/p/{0}/detail.fly".format(colorstyle)
        found_links = url_get_links(bflypdp_url)
        try:
            version =  query_version_number(colorstyle)[colorstyle]['version']
        except KeyError:
            version = 'NA'
        ## static standard urls
        oldlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=157&height=188'.format(colorstyle)
        newlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(colorstyle)
        pdpg         = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
        pmlistpg     = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=50&height=60&ver=null'.format(colorstyle)
        pmeventimg   = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=200&outputy=240&level=1&ver=null'.format(colorstyle)
        email_img1   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=140&height=182'.format(colorstyle)
        email_img2   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=200&height=250'.format(colorstyle)
        mobile_list  = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=226&height=271'.format(colorstyle)
        mobile_zoom  = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=720&outputy=864&level=1'.format(colorstyle)

        ## Uses Version # above does not
        pdplgurl     = "http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}".format(colorstyle,version)
        pdpZOOMthumb = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
        pdpZOOM      = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
        pdpaltthumb  = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt01.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
        pdpalt01z    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
        pdpalt01l    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
        bnclistpg    = "http://cdn.is.belleandclive.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=320&height=430&ver={1}".format(colorstyle,version)
        bncpdpmain   = "http://cdn.is.belleandclive.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=340&outputy=408&level=1&ver={1}".format(colorstyle,version)
        bncpdppopup  = "http://cdn.is.belleandclive.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1480&outputy=1680&level=1&ver={1}".format(colorstyle,version)
        bncZoomthumb = "http://cdn.is.belleandclive.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=59&h=78&ver={1}".format(colorstyle,version)
        #bncZoom      = "http://cdn.is.belleandclive.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1480&outputy=1680&level=1&ver={1}".format(colorstyle,version)

        
        if not found_links:
            if str(sys.argv[-1]).lower() == 'listpage':
                edgecast_listurls.append(newlistpg)
            if version == 'NA': 
                edgecast_listurls.append(newlistpg) ## or us a pass \
            else:
                ## version urls using db query not scraped
                edgecast_listurls.append(newlistpg)
                edgecast_listurls.append(pdplgurl)
                edgecast_listurls.append(pdpZOOMthumb)
                edgecast_listurls.append(pdpZOOM)
                edgecast_listurls.append(pdpaltthumb)
                edgecast_listurls.append(pdpalt01z)
                edgecast_listurls.append(pdpalt01l)
                ## B and C
                edgecast_listurls.append(bnclistpg)
                edgecast_listurls.append(bncpdpmain)
                edgecast_listurls.append(bncpdppopup)
                edgecast_listurls.append(bncZoomthumb)

            # remote cdn to clear
            ## Bluefly
            edgecast_listurls.append(oldlistpg)
            edgecast_listurls.append(newlistpg)
            edgecast_listurls.append(pdpg)
            edgecast_listurls.append(pmlistpg)
            edgecast_listurls.append(pmeventimg)
            edgecast_listurls.append(email_img1)
            edgecast_listurls.append(email_img2)
            edgecast_listurls.append(mobile_list)
            edgecast_listurls.append(mobile_zoom)
            

            ## Standard urls to clear
            #pdp_urllist.append(oldlistpg)
            #pdp_urllist.append(newlistpg)
            #pdp_urllist.append(pdpg)
            #pdp_urllist.append(pdplgurl)
            #pdp_urllist.append(pmlistpg)
            ## version urls using db query not scraped
            #pdp_urllist.append(pdpZOOMthumb)
            #pdp_urllist.append(pdpZOOM)
            #pdp_urllist.append(pdpalt01z)
            #pdp_urllist.append(pdpalt01l)
            #pdp_urllist.append(pdpaltthumb)

        else:
            for link in found_links:
                if colorstyle in link:
                    pdp_urllist.append(link)
                    vertest=link.split('&')[-1]
                    version = ''
                    if vertest[:4] == 'ver=':
                        version = vertest[-1]
                    else:
                        try:
                            version =  query_version_number(colorstyle)[colorstyle]['version']
                        except KeyError:
                            version = 'NA'
                    ## Create and append to edgecast list page urls for Edgecast
                    if alturl not in link:
                        ## static standard urls
                        oldlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=157&height=188'.format(colorstyle)
                        newlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(colorstyle)
                        pdpg         = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
                        pdplgurl     = "http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}".format(colorstyle,version)
                        pmlistpg     = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=50&height=60&ver=null'.format(colorstyle)
                        pmeventimg   = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=200&outputy=240&level=1&ver=null'.format(colorstyle)
                        pdpZOOMthumb = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                        pdpZOOM      = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                        pdpaltthumb  = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt01.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
                        pdpalt01z    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                        pdpalt01l    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                        email_img1   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=140&height=182'.format(colorstyle)
                        email_img2   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=200&height=250'.format(colorstyle)
           

                        bnclistpg    = "http://cdn.is.belleandclive.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=320&height=430&ver={1}".format(colorstyle,version)
                        bncpdpmain   = "http://cdn.is.belleandclive.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=340&outputy=408&level=1&ver={1}".format(colorstyle,version)
                        bncpdppopup  = "http://cdn.is.belleandclive.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1480&outputy=1680&level=1&ver={1}".format(colorstyle,version)
                        bncZoomthumb = "http://cdn.is.belleandclive.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=59&h=78&ver={1}".format(colorstyle,version)
                        #bncZoom      = "http://cdn.is.belleandclive.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1480&outputy=1680&level=1&ver={1}".format(colorstyle,version)


                        mobile_list  = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=226&height=271'.format(colorstyle)
                        mobile_zoom  = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=720&outputy=864&level=1'.format(colorstyle)

                        ## Bluefly
                        edgecast_listurls.append(oldlistpg)
                        edgecast_listurls.append(newlistpg)
                        edgecast_listurls.append(pdpg)
                        edgecast_listurls.append(pdplgurl)
                        edgecast_listurls.append(pmlistpg)
                        edgecast_listurls.append(pmeventimg)
                        edgecast_listurls.append(pmeventimg)
                        edgecast_listurls.append(email_img1)
                        edgecast_listurls.append(email_img2)
                        edgecast_listurls.append(mobile_list)
                        edgecast_listurls.append(mobile_zoom)

                        ## B and C
                        edgecast_listurls.append(bnclistpg)
                        edgecast_listurls.append(bncpdpmain)
                        edgecast_listurls.append(bncpdppopup)
                        edgecast_listurls.append(bncZoomthumb)


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
                            mobile_alt1 = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=720&outputy=864&level=1'.format(colorstyle)
                            #'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
                            edgecast_listurls.append(mobile_alt1)
                        ### ALT 2
                        if testurl.replace('_alt01','_alt02') in pdp_urllist:
                            pdpalt02z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt02.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt02z)
                            pdpalt02l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt02.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt02l)
                            mobile_alt2 = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt02.pct&outputx=720&outputy=864&level=1'.format(colorstyle)
                            edgecast_listurls.append(mobile_alt2)
                            print "SUCCESS2"
                        ### ALT 3
                        if testurl.replace('_alt01','_alt03') in pdp_urllist:
                            pdpalt03z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt03.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt03z)
                            pdpalt03l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt03.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt03l)
                            mobile_alt3 = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt03.pct&outputx=720&outputy=864&level=1'.format(colorstyle)
                            edgecast_listurls.append(mobile_alt3)
                            print "SUCCESS3"
                        ### ALT 4
                        if testurl.replace('_alt01','_alt04') in pdp_urllist:
                            pdpalt04z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt04.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt04z)
                            pdpalt04l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt04.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt04l)
                            print "SUCCESS4"
                            mobile_alt4 = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt04.pct&outputx=720&outputy=864&level=1'.format(colorstyle)
                            edgecast_listurls.append(mobile_alt4)
                        ### ALT 5
                        if testurl.replace('_alt01','_alt05') in pdp_urllist:
                            pdpalt05z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt05.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt05z)
                            pdpalt05l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt05.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
                            edgecast_listurls.append(pdpalt05l)
                            mobile_alt5 = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt05.pct&outputx=720&outputy=864&level=1'.format(colorstyle)
                            edgecast_listurls.append(mobile_alt5)
                            print "SUCCESS5"
                        ## Unique Set
                        edgecast_listurls = list(set(edgecast_listurls))

                        print pdp_urllist

                        #newlistpg = '/mgen/Bluefly/eqzoom85.ms?img=325084201_alt01.pct&outputx=1800&outputy=2160&level=1&ver=1'
                        #'/mgen/Bluefly/eqzoom85.ms?img=325084201_alt02.pct&outputx=1800&outputy=2160&level=1&ver=1'
                        #'/mgen/Bluefly/eqzoom85.ms?img=325084201_alt03.pct&outputx=1800&outputy=2160&level=1&ver=1'
                        #'/mgen/Bluefly/eqzoom85.ms?img=325084201_alt04.pct&outputx=1800&outputy=2160&level=1&ver=1'.format(colorstyle, version)
                        #'/mgen/Bluefly/eqzoom85.ms?img=325084201_alt05.pct&outputx=1800&outputy=2160&level=1&ver=1'.format(colorstyle, version)
                        ### 75x89 not needed as it is added to url list during the scraping of PDP
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
        print "Product is not Live. Skipping Edgecast CDN Purge and Local Purge."
        for colorstyle in colorstyle_list:
            try:
                version =  query_version_number(colorstyle)[colorstyle]['version']
            except KeyError:
                version = 'NA'
            if version == 'NA':
                pass
            else:
                POSTURL_ALLSITES = "http://clearcache.bluefly.corp/ClearAll2.php"
                POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
                POSTURL_BC = "http://clearcache.bluefly.corp/BnCClear2.php"
                POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
                send_purge_request_localis(colorstyle,version,POSTURL_ALLSITES)
                #send_purge_request_localis(colorstyle,version,POSTURL_BFY)
                #send_purge_request_localis(colorstyle,version,POSTURL_BC)
                send_purge_request_localis(colorstyle,version,POSTURL_Mobile)

    elif len(versioned_links) <= 11550:

        regex = re.compile(r'(.+?=)([0-9]{9})(.+?)(ver=[0-9][0-9]?[0-9]?[0-9]?)')
        for url_purge_local in versioned_links:
            try:
                colorstyle = re.findall(regex, url_purge_local[0])
                colorstyle = colorstyle.pop()[1]
                try:
                    version  = re.findall(regex, url_purge_local[0])
                    version = version.pop()[-1].split('=')[-1]
                except:
                    version = 'NA'
                #poprint "{0} and version num {1}".format(colorstyle,version)
                #try:
                POSTURL_ALLSITES = "http://clearcache.bluefly.corp/ClearAll2.php"
                POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
                POSTURL_BC = "http://clearcache.bluefly.corp/BnCClear2.php"
                POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"

                if version == 'NA:
                    pass
                else:
                    send_purge_request_localis(colorstyle,version,POSTURL_ALLSITES)
                #send_purge_request_localis(colorstyle,version,POSTURL_BFY)
                #send_purge_request_localis(colorstyle,version,POSTURL_BC)
                #send_purge_request_localis(colorstyle,version,POSTURL_Mobile)

                #except:
                #    print sys.stderr().read()
            except IndexError:
                print "Product is not Live. Skipping Edgecast CDN Purge and Local Purge."
    #            POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
    #            POSTURL_BC = "http://clearcache.bluefly.corp/BnCClear2.php"
    #            POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
    #            send_purge_request_localis(colorstyle,version,POSTURL_BFY)
    #            send_purge_request_localis(colorstyle,version,POSTURL_BC)
    #            send_purge_request_localis(colorstyle,version,POSTURL_Mobile)
                pass
        for url_purge in versioned_links:
            send_purge_request_edgecast(url_purge[0])
            #csv_write_datedOutfile(url_purge)

    else:
        print "Failed -- Over 8550 URLs Submitted"



    ## Now clear links from the generated urls
    #generated_links = return_cleaned_bfly_urls(edgecast_listurls)

    #print generated_links
    count = 0
    if len(edgecast_listurls) <= 8550:

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
        print "Failed -- Over 8550 URLs Submitted"


#print edgecast_listurls

if __name__ == '__main__':
    main()
