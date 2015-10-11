# -*- coding: utf-8 -*-
import sys
import os
#from sys import * 
#from os import * 
import readline 
import rlcompleter
import atexit
import csv
import glob
import collections
readline.parse_and_bind("tab: complete")
import sqlalchemy
import MySQLdb

"""
Initial Directory Variables to Set at Start
"""
dir_homedir 	        = os.path.expanduser('~') 
dir_zimages 	        = os.path.abspath("/mnt/Post_Ready/zImages_1")
dir_pushfashion 	    = os.path.abspath("/mnt/Post_Ready/eFashionPush")
dir_pushstill 	        = os.path.abspath("/mnt/Post_Ready/aPhotoPush")
dir_sites 	            = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/sites") 
dir_apps 	            = os.path.abspath("/mnt/Dropbox/Apps") 
dir_consig 	            = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment")
dir_datacsv             = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/data/csv")
dir_dboxapps 		    = os.path.abspath('/Users/johnb/Dropbox/Apps')
wild_csvI7files         = os.path.join(dir_datacsv, "*.csv")
wild_jpgZImgfiles       = os.path.join(dir_zimages, "*/*.jpg")
glob_csvI7files         = glob.glob(wild_csvI7files)
#glob_jpgZImgfiles       = glob.glob(wild_jpgZImgfiles)


# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 22:38:40 2013

@author: JCut

FUNCTION DEFINITIONS
"""



"""
Return Exif info to KeyValue Array
"""
def get_exif(fn):
    
    ret = {}
    from PIL import Image
    from PIL.ExifTags import TAGS
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
    
###########
###########
#### 1 ####
###########
########### Receive Python Date Formated as tuple or other
###        Return Date Formatted for Inserting to MySQL db
##
"""
Return Date Formatted for Inserting to MySQL db
"""
def dateMysql(date):
    date = {}
    import datetime
    from string import Formatter    
    dt = unicode(datetime.datetime.today())
    ##print dt
    Formatter()
    date = '{:.10}'.format(dt)
    return date



##################
###########
#### 2 ####
###########
########### Return Directory List With Simple Formatted CreateDate(Y-m-d) from normal datetimestamp output
###
def date_fmt_CreateDateFix(fndir):
    import datetime, os
    ret = {}
    for fn in fndir:
        info = os.stat(fn)
        ctime = info[9]
        d = datetime.date.fromtimestamp(ctime)
        d = d.isocalendar(datetime.date.fromtimestamp(d))
        d = d.strftime("%Y-%m-%d")
    return ret

############
"""
Write a Text file of input -- File Named as Today Date to Pictures folder on Linux And OSX
"""    
    ##
def csv_write_datedOutfile(lines):
    import csv,datetime,os
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter=',')
            writer.writerows([lines])

##################
###########
#### 2 ####
###########
########### 
### CSV read from file
##
def csv_read_file(filename, delim):
    with open(filename, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        reader = csv.reader(f, delimiter=delim, dialect=dialect)
        rows = []
        for row in reader: 
            rows.append(row)
        return sorted(rows)
        
###########
#### 2 ####
###########
########### CSV Write to file
##
def csv_write_datedOutfile(lines):
    import csv,datetime,os
    dt = str(datetime.datetime.now())
    today = dt.split(' ')[0]
    f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
    for line in lines:
        with open(f, 'ab+') as csvwritefile:
            writer = csv.writer(csvwritefile, delimiter=',')
            writer.writerows([lines])
                    
#################
"""
Glob or Reg Search Dir for CSV output as:
    filename(ie.style),photo_date(ie.createdate),file_location(url or filepath)

"""

def outputExifCsv(listDirGlob):
    ret = {}
    from PIL import Image
    from PIL.ExifTags import TAGS
    for fn in listDirGlob:
        i = Image.open(fn)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return ret

"""
Functions for returning union, intersection of 2 lists or Unique results of 1 list

""" 
def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a)) 
def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b)) 
def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))







##############################
###########
#### 1 ####
###########   Download URL doc/file -- Uses urllib2
###########   URL LIB 2  ###
###  DOES NOT SAVE FILE  -- use below func#3 url_download_rw_httpsave ###
###
def url2_download_read_http(targeturl):
    from time import time
    import urllib2, subprocess
    url_start = time()
    targetreq = urllib2.Request(targeturl)
    targetreq.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0')
    # targetreq.add_unredirected_header('Content-Type', 'text/html;charset=utf-8')
    downloadfile = urllib2.urlopen(targetreq).read()
    url_end = time()
    print "Download Time -> %s"  % (url_end - url_start)
    return downloadfile

##################
###########
#### 2 ####
###########   Download URL string as tmp file to cache-- Uses urllib ###
###########   URL LIB 1  ###
###  DOES NOT SAVE FILE  -- use below func#3 url2_download_read_httpsave ###
###
def url_download_read_http(targeturl):
    from time import time
    import urllib, subprocess
    url_start = time()
    downloadfile = urllib.urlretrieve(targeturl)
    url_end = time()
    print "Download Time -> %s"  % (url_end - url_start)
    return downloadfile

##################
###########
#### 3 ####
###########   Download URL string AND Save tmp file obj to Local User Directory
###########   URL LIB 2  ###
###  To Change final location of SAVED Download change var downloaddir  ###
###					
def url2_download_rw_httpsave(targeturl):
    from time import time
    import urllib2, subprocess, os
    downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
    #    if downloaddir:
    #        continue
    #    else:
    #        os.mkdir(downloaddir)
    os.mkdir(downloaddir)
    downloaddir = os.path.abspath(downloaddir)
    url_start = time()
    targetreq = urllib2.Request(targeturl)
    downloadfile = urllib2.urlopen(targetreq)
    downloadtmp = downloadfile[0]
    regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.jpg)')
    imagename = re.findall(regex, targeturl) 
    downloadfinal = os.path.join(downloaddir, imagename)
    print downloadfinal
    os.path.rename(downloadtmp, downloadfinal)
    url_end = time()
    print "Download Time -> %s"  % (url_end - url_start)
    return 	downloadfinal
    
####################
###########
#### 4 ####
###########
########### Parse File with Beautifulsoup Module
####  for link in soup.find_all('a'):
##    print(link.get('href'))
###
def html_get_parsed_images_fr_urls(htmlfile):
    import os,re
    from bs4 import BeautifulSoup
    downloaddir = os.path.abspath(os.path.join(os.path.expanduser('~'), 'script_dowloads'))
    soup = BeautifulSoup(open(htmlfile))
    imagelinksdict = soup.select('a[href*="."]')
    for line in imagelinksdict:
        imageurl = line['src']
        print imageurl
        downloadobj = url2_download_read_http(imageurl)
        downloadtmp = downloadobj[0]
        #regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.jpg)')
        regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.?)')
        imagename = re.findall(regex, imageurl)
        downloadfinal = os.path.join(downloaddir, imagename)
        print downloadfinal
        os.path.rename(downloadtmp, downloadfinal)
        
        
        
#############
#############
#######
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
###     Oracle Bfly Queries included - Only can run local to Bfly   ################################################################## 
##      --Reconfig Scripts to work with diff MySql/Orcl servers--    #################################################################
######################################################################################################################################
######################################################################################################################################
###

##############
###########
###########
#### 1 ####
########### 
########### Use in loop to return Dict of colorstyle & prod attribute metadata
######        Then use to Create exif exec strings or Use data for Reporting as usual
###
def sql_query_Metatags(style,f):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()    
    
    querymake_metatags="SELECT DISTINCT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.BRAND.NAME AS brand, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD') AS copy_dt, POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL AS category_parent, POMGR_SNP.PRODUCT_FOLDER.LABEL AS category_sub, MAX(ATG_SNP.EVENT.ID) AS event_id, POMGR_SNP.LK_PRODUCT_STATUS.NAME AS production_status, MAX(ATG_SNP.EVENT.EVENT_DESCRIPTION) AS event_title, MAX(to_date(POMGR_SNP.SAMPLE_TRACKING.CREATE_DT, 'YYYY-MM-DD')) AS sample_dt, MAX(POMGR_SNP.LK_SAMPLE_STATUS.NAME) AS sample_status, MAX(POMGR_SNP.PO_LINE.PO_HDR_ID) AS po_num, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style FROM POMGR_SNP.PRODUCT_COLOR LEFT JOIN ATG_SNP.EVENT_PRODUCT_COLOR ON POMGR_SNP.PRODUCT_COLOR.ID = ATG_SNP.EVENT_PRODUCT_COLOR.PRODUCT_COLOR_ID INNER JOIN POMGR_SNP.LK_PRODUCT_STATUS ON POMGR_SNP.PRODUCT_COLOR.PRODUCTION_STATUS_ID = POMGR_SNP.LK_PRODUCT_STATUS.ID LEFT JOIN ATG_SNP.EVENT ON ATG_SNP.EVENT_PRODUCT_COLOR.EVENT_ID = ATG_SNP.EVENT.ID INNER JOIN POMGR_SNP.PRODUCT ON POMGR_SNP.PRODUCT_COLOR.PRODUCT_ID = POMGR_SNP.PRODUCT.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER ON POMGR_SNP.PRODUCT.PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER.ID INNER JOIN POMGR_SNP.BRAND ON POMGR_SNP.PRODUCT.BRAND_ID = POMGR_SNP.BRAND.ID INNER JOIN POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED ON POMGR_SNP.PRODUCT_FOLDER.PARENT_PRODUCT_FOLDER_ID = POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.ID LEFT JOIN POMGR_SNP.SAMPLE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.SAMPLE.PRODUCT_COLOR_ID LEFT JOIN POMGR_SNP.SAMPLE_TRACKING ON POMGR_SNP.SAMPLE.ID = POMGR_SNP.SAMPLE_TRACKING.SAMPLE_ID LEFT JOIN POMGR_SNP.LK_SAMPLE_STATUS ON POMGR_SNP.SAMPLE_TRACKING.STATUS_ID = POMGR_SNP.LK_SAMPLE_STATUS.ID LEFT JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PRODUCT_COLOR.ID = '" + style + "' GROUP BY POMGR_SNP.PRODUCT_COLOR.ID, POMGR_SNP.BRAND.NAME, to_date(POMGR_SNP.PRODUCT_COLOR.COPY_READY_DT, 'YYYY-MM-DD'), POMGR_SNP.PRODUCT_FOLDER_DENORMALIZED.LABEL, POMGR_SNP.PRODUCT_FOLDER.LABEL, POMGR_SNP.LK_PRODUCT_STATUS.NAME, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE ORDER BY POMGR_SNP.PRODUCT_COLOR.ID DESC"
    
    result = connection.execute(querymake_metatags)
    metatags = {}
    for row in result:
        metatag = {}        
        metatag['colorstyle'] = row['colorstyle']
        metatag['Keywords'] = row['brand']
        metatag['IPTC:SpecialInstructions'] = row['copy_dt']
        metatag['XMP:Album'] = row['category_parent'] + "_" + row['category_sub']
        #metatag['category_sub'] = row['category_sub']
        metatag['XMP:Genre'] = row['event_id']
        metatag['IPTC:CopyrightNotice'] = row['production_status']
        metatag['IPTC:Credit'] = row['event_title']
        metatag['IPTC:Source'] = row['sample_dt']
        metatag['IPTC:SimilarityIndex'] = row['sample_status']
        metatag['IPTC:PONumber'] = row['po_num']
        metatag['IPTC:VendorStyle'] = row['vendor_style']
        #metatag['SourceFile'] = str(f)
        ## file path as dict KEY
        metatags[f] = metatag
        ## colorstyle as dict KEY
        #metatags[row['colorstyle']] = metatag
        
    connection.close()
    return metatags

###---------###

##################
###########
#### 2 ####
########### 
########### Query Mysql DB using 2 attribs. Filed(ie. 'colorstyle', param(ie.'302332901'))
###
def sql_query_StylesAttribute(searchField,searchParam):
    import sqlalchemy
    #engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
    
    engine = sqlalchemy.create_engine('mysql://root:root@localhost/data_imagepaths')
    connection = engine.connect()

    ## Create Query
    #querymake = "select * from product_snapshot where " + searchField + " like %" + searchParam + "%"
    querymake = "select * from product_snapshot where " + searchField + " = " + searchParam
    
    engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
    #querymake = "select * from " + searchtable + " where " + searchField + " = " + searchParam
    #result = connection.execute("select * from product_snapshot where brand = 'Gucci'")
    result = connection.execute(querymake)

    ### Print Results of Query
    for row in result:
        print "colorstyle:",        row['colorstyle']
        print "production status:", row['production_status']
        print "brand:",             row['brand']
        print "sample status:",     row['sample_status']
        print "sample date:",       row['status_dt']
    connection.close()
    #return ret


##################
###########
#### 3 ####
########### 
########### Query EVENTS Mysql DB using 2 attribs. Filed(ie. 'colorstyle', param(ie.'302332901'))
###
def sql_query_EventsGeneral(searchtable,searchField,searchParam):
    import sqlalchemy
    #import os
    #import sys
    #import csv
    #ret = {}
    ##  Create Sql Engine and Connection Obj -- Connected  --- 
    ##  Includes local replicated server & remote connections
    #engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
    engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imports')
    connection = engine.connect()

    ## Create Query
    #querymake = "select * from product_snapshot where " + searchField + " like %" + searchParam + "%"
  
    querymake = "select * from " + searchtable + " where " + searchField + " = " + searchParam
    #result = connection.execute("select * from product_snapshot where brand = 'Gucci'")
    result = connection.execute(querymake)
    rowsss = {}
    ### Print Results of Query
    for row in result:
        print "colorstyle:",        row['colorstyle']
        print "event group:",       row['event_group']        
        print "event id:",          row['event_id']
        print "event title:",       row['event_title']        
        print "event start:",       row['ev_start']
        #print "production status:", row['production_status']        
        
    connection.close()
    return rowsss

##################
###########
#### 4 ####
########### 
########### Upcoming Events in Dict by Colorstyle Key ### Nothing is Passed to Function ## Its obviously limited in scope ###
###
def sql_query_EventsUpcoming():
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_eventscal = "select atg_snp.event.id, atg_snp.event.start_date, atg_snp.event.event_description from atg_snp.event where atg_snp.event.start_date >= trunc(sysdate) order by start_date desc"
    result = connection.execute(querymake_eventscal)
    events = {}
    for row in result:
        event = {}        
        event['ID'] = row['ID']
        event['START_DATE'] = row['START_DATE']
        event['EVENT_DESCRIPTION'] = row['EVENT_DESCRIPTION']
        events[row['ID']] = event

    print events
    connection.close()
    return events

##################
###########
#### 5 ####
########### 
########### Primary Consignment to Bfly image renamer -- Genrates Dict of input -- Iterate for multi-key Dict
###
def sqlQueryConsigRename(vnum, ponum):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()    

    querymake_consig_stylefix="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PRODUCT_COLOR.VENDOR_STYLE LIKE '" + vnum + "%' AND POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "'"

    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['colorstyle'] = row['colorstyle']
        #consigstyle['vendor_style'] = row['vendor_style']
        consigstyles[row['vendor_style']] = consigstyle

    #print consigstyles
    connection.close()
    return consigstyles
    
    
##################
###########
#### 6 ####
########### 
########### Return Dict of Colorstyle -- with sku value -- Inputing sku
###
def sqlQuerySkuColorstyleConvert(sku):
    import sqlalchemy
    #sku = str(sku)
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()    
    
    querymake_consig_stylefix="SELECT Distinct POMGR_SNP.SKU.PRODUCT_COLOR_ID AS colorstyle, POMGR_SNP.SKU.SKU_CODE AS sku FROM POMGR_SNP.SKU WHERE POMGR_SNP.SKU.SKU_CODE LIKE '" + sku + "' ORDER by POMGR_SNP.SKU.PRODUCT_COLOR_ID ASC"
    
    result = connection.execute(querymake_consig_stylefix)
    consigstyles = {}
    for row in result:
        consigstyle = {}        
        consigstyle['colorstyle'] = row['colorstyle']
        #consigstyle['vendor_style'] = row['vendor_style']
        consigstyles[row['sku']] = consigstyle
        
    #print consigstyles
    connection.close()
    return consigstyles

##################
###########
#### 7 ####
########### 
########### Return Dict of PO -key -- with colorstyle value -- Inputing PO
###
def sqlQueryReturnStylesbyPO(ponum):
    import sqlalchemy
    ponum = str(ponum)
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
    connection = orcl_engine.connect()
    querymake_ponum_to_colorstyle="SELECT POMGR_SNP.PRODUCT_COLOR.ID AS colorstyle, POMGR_SNP.PO_LINE.PO_HDR_ID AS po_hdr FROM POMGR_SNP.PRODUCT_COLOR INNER JOIN POMGR_SNP.PO_LINE ON POMGR_SNP.PRODUCT_COLOR.ID = POMGR_SNP.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR_SNP.PO_LINE.PO_HDR_ID = '" + ponum + "'"
    result = connection.execute(querymake_ponum_to_colorstyle)
    #result = result.__iter__()
    connection.close()
    colorstyle_po_ret = {}
    for key, value in result.iteritems():
        ret = {}
        ret['colorstyle'] = value['colorstyle']
        colorstyle_po_ret[value['po_hdr']] = ret
    return colorstyle_po_ret