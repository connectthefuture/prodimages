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


def query_version_number(colorstyle):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    connection = orcl_engine.connect()
    if type(colorstyle) == list:
        colorstyles = colorstyle
        colorstyles = tuple(["{0}".format(s) for s in colorstyles])
        querymake_version_number = "SELECT DISTINCT POMGR.PO_LINE.PRODUCT_COLOR_ID as colorstyle, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.VERSION as version FROM POMGR.PRODUCT_COLOR RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID RIGHT JOIN POMGR.PO_HDR ON POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID RIGHT JOIN POMGR.VENDOR ON POMGR.VENDOR.ID = POMGR.PO_HDR.VENDOR_ID INNER JOIN POMGR.LK_PO_TYPE ON POMGR.LK_PO_TYPE.ID = POMGR.PO_HDR.PO_TYPE_ID LEFT JOIN POMGR.INVENTORY ON POMGR.INVENTORY.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID LEFT JOIN POMGR.PRODUCT_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_DETAIL.PRODUCT_ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PRODUCT_COLOR_ID in {0} ORDER BY POMGR.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last, POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last".format(colorstyles)
    else:
        querymake_version_number = "SELECT DISTINCT POMGR.PO_LINE.PRODUCT_COLOR_ID as colorstyle, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.VERSION as version FROM POMGR.PRODUCT_COLOR RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID RIGHT JOIN POMGR.PO_HDR ON POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID RIGHT JOIN POMGR.VENDOR ON POMGR.VENDOR.ID = POMGR.PO_HDR.VENDOR_ID INNER JOIN POMGR.LK_PO_TYPE ON POMGR.LK_PO_TYPE.ID = POMGR.PO_HDR.PO_TYPE_ID LEFT JOIN POMGR.INVENTORY ON POMGR.INVENTORY.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID LEFT JOIN POMGR.PRODUCT_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_DETAIL.PRODUCT_ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PRODUCT_COLOR_ID like '%{0}%' ORDER BY POMGR.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last, POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last".format(colorstyle)

    try:
        result = connection.execute(querymake_version_number)


        styles = {}
        for row in result:
            #style_info = {}
            #style_info['version'] = row['version']
            # Convert Colorstyle to string then set as KEY
            styles[str(row['colorstyle'])] = row['version']
    except sqlalchemy.exc.DatabaseError:
        print 'This Search needs to have more than 1 style, \nyou returned zero or 1 style'

    connection.close()
    return styles


def send_purge_request_localis(colorstyle, version, POSTURL):
    if colorstyle != "" and version != "":
        import pycurl,json

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

import sys,re,os

alturl = 'altimage.ms'


#catid = get_catid_from_eventid(eventid)
## Join Catid to BC Url
#url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid
#url_catid = 'http://www.belleandclive.com/browse/sales/details.jsp?categoryId=' + catid

#www.bluefly.com/Harrison-pink-check-classic-fit-dress-shirt/p/323108302/detail.fly

#url_colorstyle_pdp = 'http://www.belleandclive.com/browse/product.jsp?id=' + colorstyle

## Get all Img links on PDP and append only the primary image urls and versions
## Then tack the generated urls for edgecast to list
list_urllist = []
edgecast_listurls = []
regex = re.compile(r'http:.+?ver=[1-9][0-9]?[0-9]?')

# How many list page styles to create list page to scrape from 96 is one full page
try:
    num_styles = sys.argv[1]
except IndexError:
    num_styles = '96'
    pass

# num_styles = '1000'
#urls_to_scrape = 'http://www.bluefly.com/new_arrivals?so=new&vl=l&ppp={0}&cp=2&sosc=true'.format(num_styles)
regex_url = re.compile(r'http://www\.[bB][eElL].+')

if num_styles.isdigit():
    try:
        arg = sys.argv[2]
        if arg.isdigit() and len(arg) < 2:
            page = sys.argv[2]
            bfly_url = 'http://www.bluefly.com/new_arrivals?so=new&vl=l&ppp={0}&cp={1}&sosc=true'.format(num_styles, page)
        elif re.findall(regex_url, arg):
            url = arg
            try:
                order = sys.argv[3]
                bfly_url = '{0}?so={1}&vl=l&ppp={2}&cp=1&sosc=true'.format(url,order,num_styles)
            except IndexError:
                bfly_url = '{0}?so=new&vl=l&ppp={1}&cp=1&sosc=true'.format(url,num_styles)
        else:
            dept = arg.replace(' ','-').replace('_','-').replace('&','').lower()
            bfly_url = 'http://www.bluefly.com/designer-{0}?so=new&vl=l&ppp={1}&cp=1&sosc=true'.format(dept,num_styles)
            try:
                val = sys.argv[3]
                val = val.replace(' ','-').replace('_','-').replace('&','').lower()
                apparel = '/apparel/'
                if dept == 'mens':
                    bfly_url = 'http://www.bluefly.com/{0}{3}designer-{1}?so=new&vl=l&ppp={2}&cp=1&sosc=true'.format(dept,val,num_styles,apparel)
                else:
                    bfly_url = 'http://www.bluefly.com/{0}/designer-{1}?so=new&vl=l&ppp={2}&cp=1&sosc=true'.format(dept,val,num_styles)
            except IndexError:
                print 'Using Default New Arrivals URL with {} Styles'.format(num_styles)
                bfly_url = 'http://www.bluefly.com/new_arrivals?so=new&vl=l&ppp={0}&cp=1&sosc=true'.format(num_styles)
                pass
    except:
        print 'Using Default New Arrivals URL with {} Styles'.format(num_styles)
        bfly_url = 'http://www.bluefly.com/new_arrivals?so=new&vl=l&ppp={0}&cp=1&sosc=true'.format(num_styles)
        pass

else:
    try:
        arg = sys.argv[1]
        if re.findall(regex_url, arg):
            bfly_url = arg
        elif arg == 'designer' or arg == 'D' or arg == 'brand':
            slug = 'designer'
            try:
                brand = sys.argv[2]
                brand = brand.replace(' ','-').replace('_','-').replace('&','').lower()
                try:
                    num_styles = sys.argv[3]
                    q = '?so=new&vl=l&ppp={0}&cp=1'.format(num_styles)
                    bfly_url = 'http://www.bluefly.com/{0}/{1}{2}'.format(slug,brand, q)
                except IndexError:
                    bfly_url = 'http://www.bluefly.com/{0}/{1}'.format(slug,brand)

            except IndexError:
                print 'Using Default New Arrivals URL with 48 Styles'
                bfly_url = 'http://www.bluefly.com/new_arrivals?so=new&vl=l&ppp=48&cp=1&sosc=true'
                pass
    except IndexError:
        print 'Using Default New Arrivals URL with 48 Styles'
        bfly_url = 'http://www.bluefly.com/new_arrivals?so=new&vl=l&ppp=48&cp=1&sosc=true'
        pass

print 'Scraping -->' + bfly_url
found_links = ''

found_links = url_get_links(bfly_url)

colorstyles = []
for link in found_links:
    if link:
        list_urllist.append(link)
        colorstyle=link.split('/prodImage.ms?productCode=')[-1][:9]
        if colorstyle.isdigit():
            colorstyles.append(colorstyle)
            ## Create list page urls for Edgecast
            oldlistpg      =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=157&height=188'.format(colorstyle)
            newlistpg      =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=251&height=300'.format(colorstyle)
            pdpg           =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)
            pmlistpg       =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=50&height=60&ver=null'.format(colorstyle)
            pmeventimg     =   'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=200&outputy=240&level=1&ver=null'.format(colorstyle)
            email_img1     =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=140&height=182'.format(colorstyle)
            email_img2     =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=200&height=250'.format(colorstyle)

            edgecast_listurls.append(oldlistpg)
            edgecast_listurls.append(newlistpg)
            edgecast_listurls.append(pdpg)
            edgecast_listurls.append(pmlistpg)
            edgecast_listurls.append(pmeventimg)
            edgecast_listurls.append(email_img1)
            edgecast_listurls.append(email_img2)

colorstyles = list(set(sorted(colorstyles)))
clrversions = query_version_number(colorstyles)

for colorstyle in colorstyles:
    version = clrversions.get(colorstyle)
    if version:
        ### ZOOM HI REZ
        pdpZOOM   = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
        edgecast_listurls.append(pdpZOOM)
        testurl='http://cdn.is.bluefly.com/mgen/Bluefly/altimage.ms?img={0}_alt01.jpg&w=75&h=89&ver={1}'.format(colorstyle, version)
        ### ALT 1
        if testurl in edgecast_listurls:
            pdpalt01z = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=1800&outputy=2160&level=1&ver={1}'.format(colorstyle, version)
            edgecast_listurls.append(pdpalt01z)
            pdpalt01l = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt01.pct&outputx=583&outputy=700&level=1&ver={1}'.format(colorstyle, version)
            edgecast_listurls.append(pdpalt01l)
            print "SUCCESS1"
            #'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=340&height=408'.format(colorstyle)

## Parse urllist returning only versioned List page images
#versioned_links = return_versioned_urls(list_urllist)
import newAll_Sites_CacheClear_subproc
#print versioned_links
#count = 0
#if len(versioned_links) <= 5000:
for k,v in clrversions.iteritems():
    try:
        colorstyle = k
        version = v
        POSTURL_ALLSITES = "http://clearcache.bluefly.corp/ClearAll2.php"
        POSTURL_BFY = "http://clearcache.bluefly.corp/BFClear2.php"
        POSTURL_Mobile = "http://clearcache.bluefly.corp/BFMobileClear2.php"
        #send_purge_request_localis(colorstyle,version,POSTURL_BFY)
        #send_purge_request_localis(colorstyle,version,POSTURL_Mobile)
        newAll_Sites_CacheClear_subproc.subproc_localIS(colorstyle=colorstyle,version=version)
            #except:
            #    print sys.stderr().read()
    except IndexError:
        pass
    #csv_write_datedOutfile(url_purge)

## Now clear links from the generated urls
#generated_links = return_cleaned_bfly_urls(edgecast_listurls)

#print generated_links
count = 0
if len(edgecast_listurls) <= 12000:

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
        newAll_Sites_CacheClear_subproc.send_purge_using_requests_edgecast(url_purge)
        #csv_write_datedOutfile(url_purge)

else:
    print "Failed -- Over 12000 URLs Submitted"


#print edgecast_listurls
