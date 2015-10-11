#!/usr/bin/env python
# -*- coding: utf-8 -*-

def query_version_number(colorstyle):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')    
    connection = orcl_engine.connect()
    
    querymake_version_number = "SELECT DISTINCT POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID AS colorstyle, POMGR.PRODUCT_COLOR_DETAIL.MEDIA_VERSION as version, POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE as main, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_1 as alt01, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_2 as alt02, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_3 as alt03, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_4 as alt04, POMGR.PRODUCT_COLOR_DETAIL.ALTERNATE_IMAGE_5 as alt05, POMGR.PRODUCT_COLOR_DETAIL.MAIN_IMAGE_SWATCH as swatch FROM POMGR.PRODUCT_COLOR_DETAIL WHERE POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID LIKE '%{0}%'".format(colorstyle)

    result = connection.execute(querymake_version_number)
    style_attribs = {}
    for row in result:
        style_info = {}
        style_info['version'] = row['version']
        style_info['swatch']  = row['swatch']
        style_info['alt01']   = 'alt01' if row['alt01'] == 'Y' else ''
        style_info['alt02']   = 'alt02' if row['alt02'] == 'Y' else ''
        style_info['alt03']   = 'alt03' if row['alt03'] == 'Y' else ''
        style_info['alt04']   = 'alt04' if row['alt04'] == 'Y' else ''
        style_info['alt05']   = 'alt05' if row['alt05'] == 'Y' else ''
        # Convert Colorstyle to string then set as KEY
        style_attribs[str(row['colorstyle'])] = style_info

    connection.close()
    return style_attribs

    
    
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
        head_content_len = 'Content-length: {0}'.format(str(len(data)))
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
        return 1
        #print "Successfully Sent Local Purge Request for --> Style: {0} Ver: {1}".format(colorstyle, version)
        
        #head_authtoken = "Authorization: tok:{0}".format(token)
        #head_content_len= "Content-length: {0}".format(str(len(POSTDATA)))
        #head_accept = 'Accept: application/json'
        #head_contenttype = 'Content-Type: application/json'


def send_purge_request_edgecast(mediaPath):
    import pycurl,json,sys,os,re
    ## Regex output
    #regex_url  = re.compile(r'^(?:.+?\.ms\?\w+=)(?P<colorstyle>[1-9][0-9]{8})(?:.*?)?(?:(?:&w=)|(?:&width=)|(?:&outputx=))?(?P<width>\d+)?(?:(?:&h=)|(?:&height=)|(?:&outputy=))?(?P<height>\d+)?(?:.*?)?((?:&ver=)(?P<version>\d+))?(?:&level=\d)?$', re.U)
    regex_url  = re.compile(r'^(?:.+?\.ms\?\w+=)(?P<colorstyle>[1-9][0-9]{8})(?:.*?)?&(?:.*?)?(?:(?:w=)|(?:width=)|(?:outputx=))?(?P<width>\d+)?(?:(?:&h=)|(?:&height=)|(?:&outputy=))?(?P<height>\d+)?(?:.*?)?((?:&ver=)(?P<version>\d+))?(?:&level=\d)?$', re.U)
    matched    = regex_url.match(mediaPath)
    colorstyle = matched.group('colorstyle')
    version    = matched.group('version')
    width      = matched.group('width')
    height     = matched.group('height')   

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

            print " \nPurge Sent Successfully --> \nColorstyle: {0}\nVersion: {1}\nImageSize: {2}x{3}\n".format(colorstyle, version, width, height) ##Sent Purge Request for --> {0}".format(mediaPath)
            return [colorstyle, version, width, height]
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr 


############ RUN ###########
def compile_edgecast_urls_list(colorstyle_list=None):
    import sys,re,os
    
    edgecast_listurls = []
    #print colorstyle_list
    for colorstyle in colorstyle_list:
        res = query_version_number(colorstyle)
        version = res[colorstyle]['version']
        
        ## static standard urls
        oldlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=157&height=188'.format(colorstyle)
        newlistpg    = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(colorstyle)
        pdpg         = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
        pdplgurl     = "http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=583&outputy=700&level=1&ver={1}".format(colorstyle,version)
        pmlistpg     = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=50&height=60&ver=null'.format(colorstyle)
        pmeventimg   = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=200&outputy=240&level=1&ver=null'.format(colorstyle)
        pdpZOOMthumb = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
        pdpZOOM      = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
        email_img1   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=140&height=182'.format(colorstyle)
        email_img2   = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=200&height=250'.format(colorstyle)

        mobile_list  = 'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=226&height=271'.format(colorstyle)
        mobile_zoom  = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=720&outputy=864&level=1'.format(colorstyle)

        
        # remote cdn to clear
        edgecast_listurls.append(oldlistpg)
        edgecast_listurls.append(newlistpg)
        edgecast_listurls.append(pdpg)
        edgecast_listurls.append(pdplgurl)
        edgecast_listurls.append(pmlistpg)
        edgecast_listurls.append(pmeventimg)
        edgecast_listurls.append(email_img1)
        edgecast_listurls.append(email_img2)
        edgecast_listurls.append(mobile_list)
        edgecast_listurls.append(mobile_zoom)
        ## version urls using db query not scraped
        edgecast_listurls.append(pdpZOOMthumb)
        edgecast_listurls.append(pdpZOOM)
        
        ## Check for alt images and add thumb and zoom and list for each found
        #alts = [alt1,alt2,alt3,alt4,alt5]
        swatch     = res[colorstyle]['swatch']
        #print 'SWATCH ', swatch
        #
        alts       = []
        alts.append(res[colorstyle]['alt01'])
        alts.append(res[colorstyle]['alt02'])
        alts.append(res[colorstyle]['alt03'])
        alts.append(res[colorstyle]['alt04'])
        alts.append(res[colorstyle]['alt05'])
        #print 'Alts ', alts
        #print edgecast_listurls
        for alt in alts:
            altcount = 0
            if alt:
                altcount += 1
                pdpaltthumb  = 'http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_{1}.jpg&w=75&h=89&ver={2}'.format(colorstyle, alt, version)
                edgecast_listurls.append(pdpaltthumb) 
                pdpaltz = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_{1}.pct&outputx=1800&outputy=2160&level=1&ver={2}'.format(colorstyle, alt, version)
                edgecast_listurls.append(pdpaltz)
                pdpaltl = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_{1}.pct&outputx=583&outputy=700&level=1&ver={2}'.format(colorstyle, alt, version)
                edgecast_listurls.append(pdpaltl)
                print "SUCCESS Adding ",alt, " ", altcount, " --> ", colorstyle
                mobile_alt = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_{1}.pct&outputx=720&outputy=864&level=1'.format(colorstyle, alt)
                #'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
                edgecast_listurls.append(mobile_alt)
    return edgecast_listurls


def main(colorstyle_list=None):
    ##########################################
    ## Send the urls to clear local and cdn ##
    ##########################################
    import os,re,sys
    if not colorstyle_list:
        colorstyle_list = sys.argv[1:]

    edgecast_listurls = compile_edgecast_urls_list(colorstyle_list=colorstyle_list)
    #1regex_url  = re.compile(r'^(?:.+?\.ms\?\w+?=)(?P<colorstyle>[1-9][0-9]{8})(?:.+?)?((?:&w=)|(?:&width=)|(?:&outputx=))(?P<width>\d+)?((?:&h=)|(?:&height=)|(?:&outputy=))?(?P<height>\d+)?(?:.+?)?(?:&ver=)?(?P<version>\d+?)?$', re.U)
    #2regex_url  = re.compile(r'^(?:.+?\.ms\?\w+=)(?P<colorstyle>[1-9][0-9]{8})(?:.*?)?(?:(?:&w=)|(?:&width=)|(?:&outputx=))?(?P<width>\d+)?(?:(?:&h=)|(?:&height=)|(?:&outputy=))?(?P<height>\d+)?(?:.*?)?((?:&ver=)(?P<version>\d+))?(?:&level=\d)?$', re.U)
    #3
    regex_url  = re.compile(r'^(?:.+?\.ms\?\w+=)(?P<colorstyle>[1-9][0-9]{8})(?:.*?)?&(?:.*?)?(?:(?:w=)|(?:width=)|(?:outputx=))?(?P<width>\d+)?(?:(?:&h=)|(?:&height=)|(?:&outputy=))?(?P<height>\d+)?(?:.*?)?((?:&ver=)(?P<version>\d+))?(?:&level=\d)?$', re.U)
    ## Clear Local image servers first
    kvpairs = []
    for url_purge in edgecast_listurls:
        try:
            matched = regex_url.match(url_purge)
            colorstyle = matched.group('colorstyle')
            version    = matched.group('version')
            width      = matched.group('width')
            height     = matched.group('height')
            pair = (colorstyle, version)
            kvpairs.append(pair)
            print pair, ' Pair'
            #except:
            #    print sys.stderr().read()
        except AttributeError:
            print "Product is not Live. Skipping Edgecast CDN Purge and Local Purge."
            pass
        except IndexError:
            print "Product is not Live. Skipping Edgecast CDN Purge and Local Purge."
            pass
    POSTURL_ALLSITES = "http://clearcache.bluefly.corp/ClearAll2.php"
    print 'KVPAIRS ', kvpairs

    ## Send unique pairs to local clear
    uniquepairs = list(set(sorted([ kvpair for kvpair in kvpairs if kvpair[1] ])))
    count = [ send_purge_request_localis(pair[0],pair[1],POSTURL_ALLSITES) for pair in uniquepairs if pair[1] ]
    #print ret
    ## Now Clear Edgecast
    from collections import defaultdict
    sent_items = defaultdict(list)
    for url_purge in edgecast_listurls:
        sent = send_purge_request_edgecast(url_purge)
        sent_items[sent[0]].append(sent[1])
    ## return colorstyle, version, width, height as list of lists
    print "Total Styles with Version Local: {0}\nTotal Styles Remote: {1}".format(str(count),str(len(sent_items)))
    return sent_items


if __name__ == '__main__':
    main()

