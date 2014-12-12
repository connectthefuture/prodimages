#!/usr/bin/env python
# -*- coding: utf-8 -*-

def query_version_number(colorstyle):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')    
    connection = orcl_engine.connect()
    
    querymake_version_number = "SELECT DISTINCT POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID AS colorstyle, POMGR.PRODUCT_COLOR_DETAIL.MEDIA_VERSION as version, POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE as main, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_1 as alt1, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_2 as alt2, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_3 as alt3, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_4 as alt4, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_5 as alt5, POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE_SWATCH as swatch FROM POMGR.PRODUCT_COLOR_DETAIL WHERE POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID LIKE '%{0}%'".format(colorstyle)

    result = connection.execute(querymake_version_number)
    styles = {}
    for row in result:
        style_info = {}
        style_info['version'] = row['version']
        # Convert Colorstyle to string then set as KEY
        styles[str(row['colorstyle'])] = style_info

    connection.close()
    return styles

    
    
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
    pdp_urllist = []
    edgecast_listurls = []
    regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')
    print colorstyle_list
    for colorstyle in colorstyle_list:
        version =  query_version_number(colorstyle)[colorstyle]['version']
        ## static standard urls
        oldlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=157&height=188'.format(colorstyle)
        newlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(colorstyle)
        pdpg         = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
        pmlistpg     = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=50&height=60&ver=null'.format(colorstyle)
        pmeventimg   = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=200&outputy=240&level=1&ver=null'.format(colorstyle)
        pdpZOOMthumb = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
        pdpZOOM      = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
        pdpaltthumb  = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt01.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
        pdpalt01z    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
        pdpalt01l    = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
        email_img1   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=140&height=182'.format(colorstyle)
        email_img2   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=200&height=250'.format(colorstyle)

        mobile_list  = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=226&height=271'.format(colorstyle)
        mobile_zoom  = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=720&outputy=864&level=1'.format(colorstyle)

        # remote cdn to clear
        edgecast_listurls.append(oldlistpg)
        edgecast_listurls.append(newlistpg)
        edgecast_listurls.append(pdpg)
        edgecast_listurls.append(pmlistpg)
        edgecast_listurls.append(pmeventimg)
        edgecast_listurls.append(email_img1)
        edgecast_listurls.append(email_img2)
        edgecast_listurls.append(mobile_list)
        edgecast_listurls.append(mobile_zoom)
        ## version urls using db query not scraped
        edgecast_listurls.append(pdpZOOMthumb)
        edgecast_listurls.append(pdpZOOM)
        edgecast_listurls.append(pdpalt01z)
        edgecast_listurls.append(pdpalt01l)
        edgecast_listurls.append(pdpaltthumb) 
        
        ## Standard urls to clear
        pdp_urllist.append(oldlistpg)
        pdp_urllist.append(newlistpg)
        pdp_urllist.append(pdpg)
        pdp_urllist.append(pmlistpg)
        # version urls using db query not scraped
        pdp_urllist.append(pdpZOOMthumb)
        pdp_urllist.append(pdpZOOM)
        pdp_urllist.append(pdpalt01z)
        pdp_urllist.append(pdpalt01l)
        pdp_urllist.append(pdpaltthumb)


if __name__ == '__main__':
    import sys,re,os
    if not colorstyle_list:
        colorstyle_list = sys.argv[1:]
    main(colorstyle_list=colorstyle_list)