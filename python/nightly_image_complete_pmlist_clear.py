#!/usr/bin/env python

def send_purge_request_localis(colorstyle):
    if colorstyle != "":
        import pycurl,json

        ## Create send data
        #data = json.dumps({
        #'style' : colorstyle,
        #'version' : version
        #})
        POSTURL = "http://clearcache.bluefly.corp/BFClear2.php"
        POSTURL_Referer = POSTURL.replace('Clear2.php', 'Clear1.php')
        version= '1'
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
            
            

def daily_img_complete_list():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')
    cnx = orcl_engine.connect()
    results=cnx.execute('''select id from pomgr.product_color where image_ready_dt >= sysdate - 2''')
    reslist = [ r[0] for r in results ]
    return reslist
    
    

def modify_dt_img_list():
    import sqlalchemy
    mysql_engine  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
    cnx = mysql_engine.connect()
    sqlQuery_vendor_img_modify_dt = "select colorstyle from image_update where modify_dt BETWEEN SYSDATE( ) - INTERVAL 1 HOUR AND SYSDATE( ) + INTERVAL 2 DAY ORDER BY colorstyle DESC"
    #  and DATE_FORMAT(modify_dt,'%%Y-%%M-%%d') > DATE_FORMAT(create_dt,'%%Y-%%M-%%d') 
    results=cnx.execute(sqlQuery_vendor_img_modify_dt)
    reslist = [ r[0] for r in results ]
    return reslist
    

####################
import os, sys, re, csv

#versioned_links_null = [ pmlistpg[0] for colorstyle in daily_img_complete_list() ]
try:
    flag = sys.argv[1]
    if flag == '1':
        imagelist = modify_dt_img_list()
    else:
        india_imagelist = daily_img_complete_list()
        api_imagelist   = modify_dt_img_list()
        imagelist = api_imagelist + india_imagelist
except:
    india_imagelist = daily_img_complete_list()
    api_imagelist   = modify_dt_img_list()
    imagelist = api_imagelist + india_imagelist

count = len(imagelist)
if len(imagelist) <= 6550:
    for f in imagelist:
        try:
            colorstyle = f

            send_purge_request_localis(colorstyle)
            count -= 1
            print "{} Remaining styles to clear LOCAL IS".format(count)
            #except:
            #    print sys.stderr().read()
        except IndexError:
            pass
    count = len(imagelist)
    for f in imagelist:
        pmlistpg    =   'http://cdn.is.bluefly.com/mgen/Bluefly/prodImage.ms?productCode={0}&width=50&height=60&ver=null'.format(f)
        send_purge_request_edgecast(pmlistpg)
        count -= 1
        print "{} Remaining styles to clear EDGECAST".format(count)
        #csv_write_datedOutfile(url_purge)

else:
    print "Failed -- Over 550 URLs Submitted"    



## Now clear links from the generated urls
#generated_links = return_cleaned_bfly_urls(edgecast_listurls)



#send_purge_request_localis(colorstyle, version, POSTURL)

#print generated_links

