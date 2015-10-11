#!/usr/bin/env python


################################################################################################################
################################################################################################################
################################################################################################################
#########              ##############     USER DEFINED FUNCTIONS     ###############              ##############
#########              ###################      MASTER FILE      ###################              ##############
################################################################################################################
#########              ######################   AUTHOR JOHNB   #####################              ##############
#########              #############################################################              ##############
################################################################################################################
################################################################################################################
###########          ############################          ###########################          ################
###########          ############################          ###########################          ################
###########          ############################          ###########################          ################
###########          ############################          ###########################          ################
################################################################################################################
################################################################################################################
################################################################################################################
###########          ############################          ###########################          ################
###########          #######  Set up Tab Completion when Running Interpreter  ########          ################
################################################################################################################
import readline, rlcompleter
readline.parse_and_bind("tab: complete")
def has_href_but_no_src(tag):
    return tag.has_key('href') and not tag.has_key('src')
################################################################################################################
###########          ############################          ###########################          ################
###########          ############################          ###########################          ################
################################################################################################################
###########          Union, Intersect, Unique List Sorting Functions          ########          ################
###########          ############################          ###########################          ################
################################################################################################################
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
    
    
    
    
## Build List of Regex Matches  
def find_regex_list(regex,filelist):
    import re,os
    matchedlist = []
    try:
        
        for f in filelist:
            found = re.findall(regex, f)
            if found:
                matchedlist.append(f)
                matchedlist = sorted(dig3tlist)
            else:
                continue
    except TypeError:
        print "Error"
    return matchedlist
    
## Incremental Renaming of single file
### If new name exists increment "_1" until newname is False, then Rename
def found3digit_rename(filename):
    import os
    #print filename
    fdir = os.path.dirname(filename)
    destdir = fdir #.strip("['")
    #print destdir
    fname = os.path.basename(filename)
    style = fname.split('_')[0]
    ext = fname.split('.')[-1]
    oldname = filename
    incr = 1
    newstyle = str(style + "_" + str(incr) + "." + ext)
    newname = os.path.join(destdir, newstyle)
    while os.path.isfile(newname) == True:
        newstyle = str(style + "_" + str(incr) + "." + ext)
        newname = os.path.join(destdir, newstyle)
        print newname
        incr += 1
        os.path.isfile(newname)
    else:
        #print newname
        os.rename(oldname,newname)
        return
#####
################################################################################################################
################################################################################################################
################################################################################################################
#########     URL/PATH Download Functions      #################################################################
############     Download Image Files     ######################################################################
############        and Html Doc        ########################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
###
########
########          Print Speed incl. Multiple Function Variations
###
####################################################################
##### 
#1E
###  COMBINED: Get All href Links "Specific JPEG href select, NOT IN THIS ONEfrom Beautiful Soup and Requests -- downloads URL as html and returns Unique Links to files in text formatted by BSoup
def url_get_links(targeturl):
    import os,re,sys,requests
    from bs4 import BeautifulSoup
    r = requests.get(targeturl)
    soup = BeautifulSoup(r.text)
    ###  soup is now Full HTML of target -- Below creates/returns list of unique links
    linklist = []
    for link in soup.find_all('a'):
        linklist.append(link.get('href'))
        sorted(linklist)
    ## Return list of unique links
    return list(set(linklist))


####################################
###########
#### 2 ####
###########   Download URL as file Uses urllib ###
###########   URL LIB 1  ###
###  Will SAVE FILE  to var - downloaddir-- 
###
def url_download_file_http(url):
    from time import time
    import os, urllib, subprocess
    try:
        downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
        if not downloaddir:
            os.mkdir(downloaddir)
        filename = url.split('/')[-1]
        filepath =  os.path.join(downloaddir, filename)
        url_start = time()
        downloadfile = urllib.urlretrieve(url, filepath)
        url_end = time()
        print "File: %s\vDownload Time -> %s"  % (filename,url_end - url_start)
    except OSError:
        print "OS Error {0}".format(filepath)
    except IOError:
        print "IO Error {0}".format(filepath)
    except AttributeError:
        print "Attribute Error - Type doesnt have a property requested {0}".format(filepath)
    #return downloadfile

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
##################
###########
#### 4 a #### Send headers 
################## GOOOD
def url2_download_read_http_utf8(targeturl):
    try:
        from time import time
        import urllib2, subprocess
        import requests
        import urllib2
        url_start = time()
        headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0', 'Content-Type': 'text/html;charset=utf-8'}
        req = requests.get(targeturl, headers=headers)
        response = req.text
        url_end = time()
        print "Download Time -> %s"  % (url_end - url_start)
        return response
    except TypeError:
        print "Unicode Obj Error"
#############
###########
#### 4 b ####
##################
###########

#unparsed = url2_download_read_http_utf8(targeturl)
#req = requests.get(unparsed)
#parsed = req.text
#f = codecs.open(htmlfile, encoding='utf-8')

def html_parse_getty_links(htmlpage):
    domain = 'http://corporate.gettyimages.com'
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmlpage)
    links = []
    for link in soup.find_all('a'):
        try:
            hrefstr = link.get('href')
            filenm = link.get('title')
            lastp = str(hrefstr)
            if hrefstr:
                dload = str(domain + "/" + lastp + "/" + filenm)
            if filenm:
                print dload
            links.append(dload)
        except TypeError:
            print "Unicode Obj Error"
    return links
###   Use as newlinks = html_parse_yousend_links(url2_download_read_http(link_testreq))
###########
#### 4 c ####
###########
########### Parse File with Beautifulsoup Module
####
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
####################
###########
#### 4 d ####
###########
def url2_download_file(url):
    try:
        from time import time
        import urllib2, subprocess, os, urllib
        downloaddir = os.path.join(os.path.expanduser('~'), 'Downloads')
        #    if downloaddir:
        #        continue
        #    else:
        #        os.mkdir(downloaddir)
        #os.mkdir(downloaddir)
        downloaddir = os.path.abspath(downloaddir)
        url_start = time()
        targetreq = urllib2.Request(url)
        downloadfile = urllib2.urlopen(targetreq)
        downloadtmp = downloadfile[0]
        regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.+?g)')
        imagename = str(re.findall(regex, url))
        imagename = imagename.split('/')[-1]
        downloadfinal = os.path.join(downloaddir, imagename)
        downloadfinal = downloadfinal.split("']")
        print downloadfinal
        os.path.rename(downloadfile, downloadfinal)
        url_end = time()
        print "Download Time -> %s"  % (url_end - url_start)
    except AttributeError:
        print "Attrib Error"
    except urllib2.HTTPError:
        print "HTTP Error - Bad File URL" 
    
    #except HTTPError:
    #    print "404 Error"
        #return 	downloadfinal
#for link in links:
#    import urllib2
#    try:
#        url2_download_file(link)
#    except urllib2.HTTPError:
#        print "HTTPError" 

####################
#############
            
######### 
#####################
###  END SECTION  ###
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
############    HTML File Handling/Parsing ################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
####################    html_get_parsed_images_fr_urls
####################
###########
#### 1 ####
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




###########
#### 2 ####
########## Parse and create list of href tags with title attr
##########
def html_parse_links(htmlpage, domain):
    #domain = 'https://www.yousendit.com'
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmlpage)
    links = []
    for link in soup.find_all('a'):
        try:
            hrefstr = link.get('href')
            filenm = link.get('title')
            #filenm = soup.select('a[href*="."]')
            lastp = str(hrefstr)
            if hrefstr:
                #dload = str(domain + "/" + lastp + "/" + filenm)
                dload = str(domain + "/" + lastp + "/" + filenm)
                links.append(dload)
            if filenm:
                print filenm
        except TypeError:
            print "Unicode Obj Error"
        except UnicodeEncodeError:
            print "Unicode ASCII Codec Error"
    return links


##########
#####################
###  END SECTION  ###
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###-##            Read And Write text to files            ##-##############################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################

                            ###########
                            ### CSV ###
                            ###########
                            
#######################################
#######################################################################
###########    CSV Write to file and CSV read from file delim=csv #####
#### 1 ####
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
        

###### In prog/version may not work right use above
#def csv_read_file(filename, delim):
#    with open(filename, 'rb') as f:
#            dialect = csv.Sniffer().sniff(f.read(1024))
#            reader = csv.reader(f, delimiter=delim, dialect=dialect)
#            for lines in reader:
#                cols = []
#                for col in lines:
#                    if str(col) == "None":
#                        continue
#                    else:
#                        print col
##################
###########
#### 3 ####
###########
###########
#######  Glob or Reg Search Dir for CSV output as filename(ie.style), photo_date(ie.createdate), file_location(url or filepath)
###
def csv_read_exiftags(list_or_glob):
    ret = {}
    from PIL import Image
    from PIL.ExifTags import TAGS
    for f in list_or_glob:
        i = Image.open(f)
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return ret


###
#####################
###  END SECTION  ###
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###      Date Related Conversion/Parsing Functions       ##################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###

###########
###########
#### 1 ####
###########
########### Receive Python Date Formated as tuple or other
###        Return Date Formatted for Inserting to MySQL db
##
def date_fmt_MySQL(date):
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

#####################
###  END SECTION  ###
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
###  Image Metadata Related Extracting/Embedding Functions   ########################################################################
######################## PYEXIV2 ####################################################################################################
#########################  AND   ####################################################################################################
############    Image Manipulation Functions    #####################################################################################
#####################################################################################################################################
#####################################################################################################################################
###
##

    #######################################################
    #######################################################
    #######################################################
    ###### Read and Write Metadata from image files  ######
    #######################################################
    #######################################################

                ###############
                ### Writing ###
                ###############

##################
###########
#### 1 ####
###########
########### Write IPTC Data to Image File
###
#def writeXmp(imgfile,xmpkey,xmpvalue):
#    import pyexiv2
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[xmpkey] = xmpvalue
#    

##################
###########
#### 2 ####
###########
########### Write IPTC Data to Image File
#def writeIptc(imgfile,iptckey,iptcvalue):
#    import pyexiv2
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[iptckey] = iptcvalue
#

##################
###########
#### 3 ####
###########
########### Write EXIF Data from Image File
#def writeExif(imgfile,exifkey,exifvalue):
#    import pyexiv2    
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    metadata[exifkey] = exifvalue
#

#######################################################
##################
#######################################################

                ###############
                ### Reading ###
                ###############

#######################################################
###########
#### 4 ####
########### 
########### Read IPTC Data from Image File
###
#def readIptc(imgfile):
#    import pyexiv2    
#    metadata = pyexiv2.ImageMetadata(imgfile)
#    mdataprint = metadata.read()
#    print metadata


#######################################################
###########
#### 5 ####
########### Return Exif info to KeyValue Array
###
def metadata_get_exif(imgfile):
    ret = {}
    from PIL import Image
    from PIL.ExifTags import TAGS
    i = Image.open(imgfile)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

###
###
#####################
###  END SECTION  ###
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
## Add new Function Def


#####################
###  END SECTION  ###
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
######################################################################################################################################
######################################################################################################################################
##########                                                    ########################################################################
##########         WebServer and Networking Functions         ########################################################################
##        --Reconfig Scripts to work with diff server Ports--        #################################################################
##########                                                    ########################################################################
######################################################################################################################################
######################################################################################################################################
###

##############
###########
###########
#### 1 ####
########### 
########### Start WebServer at http://localhost:8111
###

    #def www_run_httpd(url_serverroot='localhost',port_http=8111,server_class=BaseHTTPServer.HTTPServer,handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
    #    server_address = (url_serverroot, port_http)
    #    httpd = server_class(server_address, handler_class)
    #    httpd.serve_forever()


##############
###########
###########
#### 2 #### CLASS
########### AJAX Request/Response HANDLER CLASS
###########
#class http_request_handler(asynchat.async_chat):
#
#    def __init__(self, sock, addr, sessions, log):
#        asynchat.async_chat.__init__(self, sock=sock)
#        self.addr = addr
#        self.sessions = sessions
#        self.ibuffer = []
#        self.obuffer = ""
#        self.set_terminator("\r\n\r\n")
#        self.reading_headers = True
#        self.handling = False
#        self.cgi_data = None
#        self.log = log
#
#    def collect_incoming_data(self, data):
#        """Buffer the data"""
#        self.ibuffer.append(data)
#
#    def found_terminator(self):
#        if self.reading_headers:
#            self.reading_headers = False
#            self.parse_headers("".join(self.ibuffer))
#            self.ibuffer = []
#            if self.op.upper() == "POST":
#                clen = self.headers.getheader("content-length")
#                self.set_terminator(int(clen))
#            else:
#                self.handling = True
#                self.set_terminator(None)
#                self.handle_request()
#        elif not self.handling:
#            self.set_terminator(None) # browsers sometimes over-send
#            self.cgi_data = parse(self.headers, "".join(self.ibuffer))
#            self.handling = True
#            self.ibuffer = []
#            self.handle_request()

#####################
###  END SECTION  ###
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################


## Add new Section or Function Def


#####################
###  END SECTION  ###
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################


## Add new Section or Function Def

#
###
#####
################################################################################################################################################################################
################################################################################################################################################################################
################################################################                                                                        ########################################
###################   END   ####################################                                                                        ########################################
#########    Function Definitions    ###########################                                                                        ########################################
################################################################                                                                        ########################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################                                                                        ########################################
################################################################                                                                        ########################################
################################################################                Execute Above Function Definitions Below                ########################################
################################################################                                                                        ########################################                
################################################################                                                                        ########################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################                                                                        ########################################
######     Begin Executble Scripting Tests     #################                                                                        ########################################
###################  AKA Scratch  ##############################                                                                        ########################################
################################################################                                                                        ########################################
################################################################################################################################################################################
################################################################################################################################################################################
#####
###
#
#import os, re
#dir_homedir = os.path.expanduser('~')
###
#regex2 = re.compile(r'.+?/([A-Za-z0-9-_%]+?.jpg)')  ## Regex to extract/find name of jpegs from a full file/url path
#
##htmlfile1 = sys.argv[0]
#
##htmlfile1 = os.path.join(dir_homedir, 'nasa.html')
#
#htmlfile1 = 'http://webpy.org/cookbook/'
#
#get_images_parse_htmllinks(htmlfile1)
##print imagelinksdict
#
#
#
#
#



###  END SCRIPTING SECTION  ###############################################################################################################################
###############################
###  END SCRIPTING SECTION  ###
###############################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
##########################################    MISC. Buggy/In prog Scripts     #############################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###############################
###







############################  END MISC SECTION 1 ###
###########################################################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
#########################################   Even More MISC. Buggy/In prog Scripts   #######################################################################
###########################################################################################################################################################
###########################################################################################################################################################
###############################
###

##################
###########
#### 1 ####
###########
###########
##    Write a Text file of input -- File Named as Today Date to Pictures folder on Linux And OSX
#     ###-->Script may work and just be redundant

#def file_readwrite_FileFormatted(input_list,outfilename):
#    #ret = {}
#    from datetime import datetime
#    from string import Formatter    
#    from os import path
#    dt = unicode(datetime.today())
#    print dt
#    Formatter()
#    date = '{:.10}'.format(dt)
#    print date    
#    dir_homedir = path.expanduser('~')
#    
#    myfile = unicode(path.join(dir_homedir, 'Pictures/' + outfilename + '-' + date + '.txt'))   
#    #frd  = file()
#    print myfile    
#    #fwrt = file(myfile, 'w+')     
#    wrt = open(myfile, 'w+')
#    for line in fn:
#        sline = str(line)
#        print sline
#        wrt.write(sline + '\n')
#    wrt.close


########
########
###########################################################################################################################################################
########
########


###############################
###  END MISC SECTION 2 ###
###########################################################################################################################################################
########
########
######################
##################################################################################
###################### Misc Notes and Snips to End(EOF) ############################
##################################################################################
##################################################################################
###################### 

## Original Root Html file parsed for html files in site root html
#sublink = getlinkfrmhtml(siteroot, htmlfile1, regex)

	##<----##### New Html File sub1 from Harvested Link from orig html file  
#linkedreader = url2_download_read_http(sublink)
#linkedreader = linkedreader[0]

## sub1 Html file parsed for html files in site root html
#	sublink_sub1 = getlinkfrmhtml(siteroot, linkedreader, regex)
#	print sublink_sub1

#htmlfile_sub1 = linkedreader
#with open(htmlfile_sub1) as f:
#		for line in f:
#			print line

#def getlinkfrmhtml(siteroot, htmlfile, regex):
#	with open(htmlfile) as f:
#		next(f)
#		for line in f:
#			print line.strip('')
#			linkedpath = re.findall(regex, line)
#			for line in linkedpath:
#				
#				if line:
#					linkedpath = str(line)
#					pageurl = str(siteroot + linkedpath)
#					
#					print pageurl
#				else:
#					continue
#				return pageurl

	#### Read HTML fromDownload
#	with open(downloadfile[0]) as newf:
#		for line in newf:
#			print line
	####
	
	#[IMG][/IMG]
	#regex = re.compile(r'src="([^"]+)"') ##

###########################################################################################################################################################
###  END FILE  ################
###########################################################################################################################################################
