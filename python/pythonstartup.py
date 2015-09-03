#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 22:38:40 2013

@author: Johnb

import re
import readline
import rlcompleter
import atexit
import csv
import glob
import collections
readline.parse_and_bind("tab: complete")
#import sqlalchemy
# from bs4 import BeautifulSoup
# import requests
# import scrapy
#import MySQLdb
#os.chdir(os.path.dirname(__file__))
# dir_homedir 	        = os.path.expanduser('~')
# dir_homedir             = os.path.abspath(dir_homedir)
# dir_studioraw 	        = os.path.abspath("/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE")
# dir_studiozimages 	    = os.path.abspath("/mnt/Production_Raw/.zImages_1")
# dir_dropfinalfiles 	    = os.path.abspath("/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly")
# dir_uploadedarch 	    = os.path.abspath("/mnt/Post_Complete/Complete_Archive/Uploaded")
# dir_zimages 	        = os.path.abspath("/mnt/Post_Ready/zImages_1")
# #dir_pushfashion 	    = os.path.abspath("/mnt/Post_Ready/eFashionPush")
# dir_pushstill 	        = os.path.abspath("/mnt/Post_Ready/aPhotoPush")
# dir_imagedropfile7      = os.path.abspath("/mnt/Post_Complete/ImageDrop")
# dir_marketplace 	    = os.path.abspath("/mnt/Post_Complete/Complete_Archive/MARKETPLACE")
# #dir_apps 	            = os.path.abspath("/mnt/Dropbox/Apps")
# #dir_consig 	            = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment")
# dir_datacsv             = os.path.abspath("/mnt/Post_Ready/zProd_Server/imageServer7/data/csv")
#dir_dboxapps 		    = os.path.join(dir_homedir, "Dropbox/Apps")
#dir_spydermac 		    = os.path.join(dir_homedir, "Dropbox/Dropbox_sites/SpyderMac")
#wild_csvI7files         = os.path.join(dir_datacsv, "*.csv")
#wild_jpgZImgfiles       = os.path.join(dir_zimages, "*/*.jpg")
#glob_csvI7files         = glob.glob(wild_csvI7files)
#glob_jpgZImgfiles       = glob.glob(wild_jpgZImgfiles)



link_testreq = 'https://www.yousendit.com/dl?phi_action=app/orchestrateDownload&rurl=https%253A%252F%252Fwww.yousendit.com%252Ftransfer.php%253Faction%253Dbatch_download%2526send_id%253D2064268784%2526email%253D0813d1d13bbc4778ff7be299531aa0b4&s=19105&cid=tx-02002208350200000000'

########## REGEX PATTERN DEFINITIONS COMPILed

pattern_9digitstyle = re.compile(r'(\d{9})_?')
pattern_altnumber = re.compile(r'\d{9}_(\d{1})[.]')
pattern_filepath = re.compile(r'(/+?.+[.][a-zA-Z]{3})')

pattern_url = r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/'
regex_url = re.compile(r'/^(((http|https|ftp):\/\/)?([[a-zA-Z0-9]\-\.])+(\.)([[a-zA-Z0-9]]){2,4}([[a-zA-Z0-9]\/+=%&_\.~?\-]*))*$/')

#lftstrip = strline.strip('["')
#rtstrip = lftstrip.strip('"]')

pattern_dategeneric = re.compile(r'(\d{2,4}[/|-]+?.{2,3}[/|-]+?\d{2,4})')

#pattern_exifval = r'([A-Za-z0-9]*?\s*?\W+?)'
pattern_exiftag = r'([A-Z]\w+?:[A-Za-z]\w+?)'
pattern_exifval = r'([A-Z0-9]\w+?\s?[A-Za-z]+\')'
regex_exif = re.compile(pattern_exiftag + "=" + pattern_exifval)

#pattern = re.compile(r'(\d+?[/|-]+?\d+?[/|-]+?\d+?)')

#f = open(csvfile, 'rb')
#string = re.findall(pattern, f.read())
#sorted(string)
#print list(string)
#for f in listdir(dir_homedir):
#     fpath = os.path.abspath(f)
#     re.findall(pattern, fpath)

#querystr = 'http://www.bluefly.com/_/N-1aaq/Ntt-{style}/Nrk-all/Nrr-all/Nrt-{style}/Ntk-all/Ntx-mode+matchallpartial/search.fly?init=y'.format(style=colorstyle)


#startDateFrom=&startDateTo=&colorGroup=&searchBrand=&eventId=&productStatus=&merchantStatus=&inventory=&active=&store=&styleNumbers=324162301&vendorStyleNumbers=&shortName=&poHdrs=&searchCategory=&jdaCategory=&Submit=Search&exportToExcel=false&exportImages=false&solrQuery=&currentPage=0
#pythonpath = ['',
#             '/usr/local/lib/python2.7/site-packages',
             #'/usr/local/lib/python/site-packages',
#             '/usr/local/bin',
#             '/usr/local/sbin',
#             '/usr/bin',
#             '/usr/sbin',
             #'/usr/local/lib/python2.7/site-packages/Orange/orng',
             #'/usr/local/lib/python2.7/site-packages/IPython/extensions',
             #'/home/johnb/virtualenvs/DJDAM/lib/python2.7/site-packages',
             #'/home/johnb/virtualenvs/DJDAM/src/djdam',
             #'/home/johnb/virtualenvs/DJDAM/src',
#             '/usr/local/batchRunScripts/python',
#             '/usr/local/batchRunScripts/python/jbmodules',
#             '~/.ipython']
# #### REGEX PATTERN DEFINITIONS
# ###
# ## Walk Root Directory and Return List or all Files in all Subdirs too
# def recursive_dirlist(rootdir):
#     import os
#     walkedlist = []
#     for dirname, subdirnames, filenames in os.walk(rootdir):
#         # append path of all filenames to walkedlist
#         for filename in filenames:
#             file_path = os.path.abspath(os.path.join(dirname, filename))
#             if os.path.isfile(file_path):
#                 walkedlist.append(file_path)
#     # Advanced usage:
#     # editing the 'dirnames' list will stop os.walk() from recursing into there.
#     #if '.git' in dirnames:
#     # don't go into any .git directories.
#     #    dirnames.remove('.git')
#     walkedset = list(set(sorted(walkedlist)))
#     return walkedset



# ###########          ############################          ###########################          ################
# ################################################################################################################
# ###########          FTP AND CURL Functions          ########          ################
# ###########          ############################          ###########################          ################
# ################################################################################################################
# ## Upload to imagedrop via FTP Unreliable
# # def upload_to_imagedrop(file):
# #     import ftplib
# #     session = ftplib.FTP('file3.bluefly.corp', 'imagedrop', 'imagedrop0')
# #     fileread = open(file, 'rb')
# #     filename = str(file.split('/')[-1])
# #     session.cwd("ImageDrop/")
# #     session.storbinary('STOR ' + filename, fileread, 8*1024)
# #     fileread.close()
# #     session.quit()


# # #### Very Reliable FTP upload to Imagedrop using PyCurl
# # def pycurl_upload_imagedrop(localFilePath):
# #     import pycurl, os
# #     #import FileReader
# #     localFileName = localFilePath.split('/')[-1]

# #     mediaType = "8"
# #     ftpURL = "ftp://file3.bluefly.corp/ImageDrop/"
# #     ftpFilePath = os.path.join(ftpURL, localFileName)
# #     ftpUSERPWD = "imagedrop:imagedrop0"

# #     if localFilePath != "" and ftpFilePath != "":
# #         ## Create send data

# #         ### Send the request to Edgecast
# #         c = pycurl.Curl()
# #         c.setopt(pycurl.URL, ftpFilePath)
# #         c.setopt(pycurl.PORT , 21)
# #         c.setopt(pycurl.USERPWD, ftpUSERPWD)
# #         c.setopt(pycurl.VERBOSE, 1)
# #         f = open(localFilePath, 'rb')
# #         c.setopt(pycurl.INFILE, f)
# #         c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
# #         c.setopt(pycurl.UPLOAD, 1)

# #         try:
# #             c.perform()
# #             c.close()
# #             print "Successfully Sent Purge Request for --> {0}".format(localFileName)
# #         except pycurl.error, error:
# #             errno, errstr = error
# #             print 'An error occurred: ', errstr


# #END###### FTP FUNX

# """
# Return Date Formatted for Inserting to MySQL db
# """
# def dateMysql(date):
#     date = {}
#     import datetime
#     from string import Formatter
#     dt = unicode(datetime.datetime.today())
#     ##print dt
#     Formatter()
#     date = '{:.10}'.format(dt)
#     return date



# """
# Return Exif info to KeyValue Array
# """
# def get_exif_pip(fn):

#     ret = {}
#     from PIL import Image
#     from PIL.ExifTags import TAGS
#     i = Image.open(fn)
#     info = i._getexif()
#     for tag, value in info.items():
#         decoded = TAGS.get(tag, tag)
#         ret[decoded] = value
#     return ret

# ###########################################################################################################################################################

#                             ###########
#                             ### CSV ###
#                             ###########

# #######################################
# #######################################################################
# ###########    CSV Write to file and CSV read from file delim=csv #####
# #### 1 ####
# ###########
# ########### CSV Write to file
# ############
# """
# Write a Text file of input -- File Named as Today Date to Pictures folder on Linux And OSX
# """
#     ##
# def csv_write_datedOutfile(lines):
#     import csv,datetime,os
#     dt = str(datetime.datetime.now())
#     today = dt.split(' ')[0]
#     f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
#     for line in lines:
#         with open(f, 'ab+') as csvwritefile:
#             writer = csv.writer(csvwritefile, delimiter=',')
#             writer.writerows([lines])

# ##################
# ###########
# #### 2 ####
# ###########
# ###########
# ### CSV read from file
# ##
# def csv_read_file(filename, delim):
#     with open(filename, 'rb') as f:
#         dialect = csv.Sniffer().sniff(f.read(1024))
#         reader = csv.reader(f, delimiter=delim, dialect=dialect)
#         rows = []
#         for row in reader:
#             rows.append(row)
#         return sorted(rows)

# ###########
# #### 2 ####
# ###########
# ########### CSV Write to file
# ##
# def csv_write_datedOutfile(lines):
#     import csv,datetime,os
#     dt = str(datetime.datetime.now())
#     today = dt.split(' ')[0]
#     f = os.path.join(os.path.expanduser('~'), today + '_write.csv')
#     for line in lines:
#         with open(f, 'ab+') as csvwritefile:
#             writer = csv.writer(csvwritefile, delimiter=',')
#             writer.writerows([lines])

# #################
# """
# Glob or Reg Search Dir for CSV output as:
#     filename(ie.style),photo_date(ie.createdate),file_location(url or filepath)

# """

# def outputExifCsvPipo(listDirGlob):
#     ret = {}
#     from PIL import Image
#     from PIL.ExifTags import TAGS
#     for fn in listDirGlob:
#         i = Image.open(fn)
#         info = i._getexif()
#         for tag, value in info.items():
#             decoded = TAGS.get(tag, tag)
#             ret[decoded] = value
#     return ret

# """
# Functions for returning union, intersection of 2 lists or Unique results of 1 list

# """
# def unique(a):
#     """ return the list with duplicate elements removed """
#     return list(set(a))
# def intersect(a, b):
#     """ return the intersection of two lists """
#     return list(set(a) & set(b))
# def union(a, b):
#     """ return the union of two lists """
#     return list(set(a) | set(b))


# ##############################
# ###########
# #### 1A ####
# ###########   Download URL doc/file -- Uses urllib2
# ###########   URL LIB 2  ###
# ###  DOES NOT SAVE FILE  -- use below func#3 url_download_rw_httpsave ###
# ###
# # def url2_download_read_http(targeturl):
# #     from time import time
# #     import urllib2, subprocess
# #     url_start = time()
# #     targetreq = urllib2.Request(targeturl)
# #     targetreq.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0')
# #     targetreq.add_unredirected_header('Content-Type', 'text/html;charset=utf-8')
# #     downloadfile = urllib2.urlopen(targetreq).read()
# #     url_end = time()
# #     print "Download Time -> %s"  % (url_end - url_start)
# #     return downloadfile


# def recurse_dir_list(directory):
#     filepaths = {}
#     for dirpath,subdir,files in os.walk(directory):
#         for f in files:
#             filepaths[dirpath] = f
#     recursivefilelist = []
#     for path,file in filepaths.iteritems():
#         filepath = "{0}/{1}".format(path,file)
#         recursivefilelist.append(filepath)
#     regex = re.compile(r'.+?[.]jpg$')
#     alljpgs = []
#     for f in recursivefilelist:
#         foundjpgs = re.findall(regex,f)
#         if foundjpgs:
#             alljpgs.append(f)
#     return alljpgs
# ##################
# #################
# #### 1B,C/D and  E# Better Simpler version of Above Function with Extraction of Links from retrieved url
# ################# Split up as sep funcs to make_soup=only returns the HTML for further parsing
# #################  and soup_from_url recieves BeautifulSoup formatted soup and returns Unique links
# ################# 1E is the verbose version of combining 1B & C
# #####  Beautiful Soup and Requests downloads URL as html and returns in text formatted by BSoup
# #####
# ####################################################################
# ##### Get HTML from URL and make Soup
# #1B
# def soup_from_url(targeturl):
#     from bs4 import BeautifulSoup
#     import requests
#     r = requests.get(targeturl)
#     soup = BeautifulSoup(r.text)
#     return soup

# ##### Return Links from Soup
# #1C
# def soup_get_links(soup):
#     from bs4 import BeautifulSoup
#     ###  soup is now Full HTML of target -- Below creates/returns list of unique links
#     linklist = []
#     for link in soup.find_all('a'):
#         linklist.append(link.get('href'))
#         sorted(linklist)
#     ## Return list of unique links
#     return list(set(linklist))



# ##### Return JPG links from Soup
# #1D
# def soup_get_links_jpgs(soup):
#     from bs4 import BeautifulSoup
#     linklist = []
#     for link in soup.select('a[href$="jpg"]'):
#         linklist.append(link.get('href'))
#         sorted(linklist)
#     ## Return list of unique links to jpg Files
#     return list(set(linklist))

# ### Combined consolidated func run like --> linklist = url_get_links(targeturl)  --- Use url_download_fileslist_dbx(imglinks) to download
# ####################################################################
# #####
# #1E
# ###  COMBINED: Get All href Links "Specific JPEG href select, NOT IN THIS ONEfrom Beautiful Soup and Requests -- downloads URL as html and returns Unique Links to files in text formatted by BSoup
# # def url_get_links(targeturl):
# #     import os,re,sys,requests
# #     from bs4 import BeautifulSoup
# #     r = requests.get(targeturl)
# #     soup = BeautifulSoup(r.text)
# #     ###  soup is now Full HTML of target -- Below creates/returns list of unique links
# #     linklist = []
# #     for link in soup.find_all('a'):
# #         linklist.append(link.get('href'))
# #         sorted(linklist)
# #     ## Return list of unique links
# #     return list(set(linklist))


# # ####################################
# # ###########
# # #### 2 ####
# # ###########   Download URL as file Uses urllib ###
# # ###########   URL LIB 1  ###
# # ###  Will SAVE FILE  to var - downloaddir--
# # ###
# # def url_download_file_http(url):
# #     from time import time
# #     import urllib, subprocess
# #     try:
# #         downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
# #         if not downloaddir:
# #             os.mkdir(downloaddir)
# #         filename = url.split('/')[-1]
# #         filepath =  os.path.join(downloaddir, filename)
# #         filepath =  os.path.join(filepath, '.file')
# #         url_start = time()
# #         downloadfile = urllib.urlretrieve(url, filepath)
# #         url_end = time()
# #         print "Download Time -> %s"  % (url_end - url_start)
# #     except OSError:
# #         print "OS Error"
# #     except AttributeError:
# #         print "Attribute Error - Type doesnt have a property requested"
# #     return downloadfile

# # ### Below accepts single URL Above doesnt iterate and takes only 1 URL
# # #imglinkslist = soup_get_links((soup_from_url(targeturl)))
# def url_download_fileslist_dbx(imglinkslist):
#     import urllib,os,time,subprocess
#     downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
#     for link in imglinkslist:
#         try:
#             filename = str(link.split('/')[-1])
#             filepath =  os.path.join(downloaddir, filename)
#             os.chdir(downloaddir)
#             #url_start = time()
#             downloadfile = urllib.urlretrieve(link, filepath)
#             #url_end = time()
#             #print "File %s Download Time -> %s" % (downloadfile, url_end - url_start)
#         except AttributeError:
#             print "Attribute Error -- None Type"
#         except IOError:
#             print "IO Error No File or Dir to save {0}".format(filepath)
#         except OSError:
#             print "OS Error {0}".format(filepath)
#             return downloadfile

# ##################
# ###########
# #### 3 ####
# ###########   Download URL string AND Save tmp file obj to Local User Directory
# ###########   URL LIB 2  ###
# ###  To Change final location of SAVED Download change var downloaddir  ###
# ###
# def url2_download_rw_httpsave(targeturl):
#     from time import time
#     import urllib2, subprocess, os
#     downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
#     #    if downloaddir:
#     #        continue
#     #    else:
#     #        os.mkdir(downloaddir)
#     os.mkdir(downloaddir)
#     downloaddir = os.path.abspath(downloaddir)
#     url_start = time()
#     targetreq = urllib2.Request(targeturl)
#     downloadfile = urllib2.urlopen(targetreq)
#     downloadtmp = downloadfile[0]
#     regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.jpg)')
#     imagename = re.findall(regex, targeturl)
#     downloadfinal = os.path.join(downloaddir, imagename)
#     print downloadfinal
#     os.path.rename(downloadtmp, downloadfinal)
#     url_end = time()
#     print "Download Time -> %s"  % (url_end - url_start)
#     return 	downloadfinal
# ##################
# ###########
# #### 4 a #### Send headers
# ################## GOOOD
# def url2_download_read_http_utf8(targeturl):
#     try:
#         from time import time
#         import urllib2, subprocess
#         import requests
#         import urllib2
#         url_start = time()
#         headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:20.0) Gecko/20100101 Firefox/20.0', 'Content-Type': 'text/html;charset=utf-8'}
#         req = requests.get(targeturl, headers=headers)
#         response = req.text
#         url_end = time()
#         print "Download Time -> %s"  % (url_end - url_start)
#         return response
#     except TypeError:
#         print "Unicode Obj Error"
# #############
# ###########
# #### 4 b ####
# ##################
# ###########

# #unparsed = url2_download_read_http_utf8(targeturl)
# #req = requests.get(unparsed)
# #parsed = req.text
# #f = codecs.open(htmlfile, encoding='utf-8')

# def html_parse_getty_links(htmlpage):
#     domain = 'http://corporate.gettyimages.com'
#     from bs4 import BeautifulSoup
#     soup = BeautifulSoup(htmlpage)
#     links = []
#     for link in soup.find_all('a'):
#         try:
#             hrefstr = link.get('href')
#             filenm = link.get('title')
#             lastp = str(hrefstr)
#             if hrefstr:
#                 dload = str(domain + "/" + lastp + "/" + filenm)
#             if filenm:
#                 print dload
#             links.append(dload)
#         except TypeError:
#             print "Unicode Obj Error"
#     return links
# ###   Use as newlinks = html_parse_yousend_links(url2_download_read_http(link_testreq))
# ###########
# #### 4 c ####
# ###########
# ########### Parse File with Beautifulsoup Module
# # ####
# # ###
# # def html_get_parsed_images_fr_urls(htmlfile):
# #     import os,re
# #     from bs4 import BeautifulSoup
# #     downloaddir = os.path.abspath(os.path.join(os.path.expanduser('~'), 'script_dowloads'))
# #     soup = BeautifulSoup(open(htmlfile))
# #     imagelinksdict = soup.select('a[href*="."]')
# #     for line in imagelinksdict:
# #         imageurl = line['src']
# #         print imageurl
# #         downloadobj = url2_download_read_http(imageurl)
# #         downloadtmp = downloadobj[0]
# #         #regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.jpg)')
# #         regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.?)')
# #         imagename = re.findall(regex, imageurl)
# #         downloadfinal = os.path.join(downloaddir, imagename)
# #         print downloadfinal
# #         os.path.rename(downloadtmp, downloadfinal)
# # ####################
# # ###########
# # #### 4 d ####
# # ###########
# # # def url2_download_file(url):
# # #     try:
# # #         from time import time
# # #         import urllib2, subprocess, os, urllib
# # #         downloaddir = os.path.join(os.path.expanduser('~'), 'Downloads')
# # #         #    if downloaddir:
# # #         #        continue
# # #         #    else:
# # #         #        os.mkdir(downloaddir)
# # #         #os.mkdir(downloaddir)
# # #         downloaddir = os.path.abspath(downloaddir)
# # #         url_start = time()
# # #         targetreq = urllib2.Request(url)
# # #         downloadfile = urllib2.urlopen(targetreq)
# # #         downloadtmp = downloadfile[0]
# # #         regex = re.compile(r'.+?/([A-Za-z0-9-_%]+?.+?g)')
# # #         imagename = str(re.findall(regex, url))
# # #         imagename = imagename.split('/')[-1]
# # #         downloadfinal = os.path.join(downloaddir, imagename)
# # #         downloadfinal = downloadfinal.split("']")
# # #         print downloadfinal
# # #         os.path.rename(downloadfile, downloadfinal)
# # #         url_end = time()
# # #         print "Download Time -> %s"  % (url_end - url_start)
# # #     except AttributeError:
# # #         print "Attrib Error"
# # #     except urllib2.HTTPError:
# # #         print "HTTP Error - Bad File URL"

# # #     #except HTTPError:
# # #     #    print "404 Error"
# # #         #return 	downloadfinal
# # # #for link in links:
# # # #    import urllib2
# # # #    try:
# # # #        url2_download_file(link)
# # # #    except urllib2.HTTPError:
# # # #        print "HTTPError"

# # ####################
# # #############
# # """
# # Glob or Reg Search Dir for CSV output as:
# #     filename(ie.style),photo_date(ie.createdate),file_location(url or filepath)

# # """

# # # def outputExifCsv(listDirGlob):
# # #     ret = {}
# # #     from PIL import Image
# # #     from PIL.ExifTags import TAGS
# # #     for fn in listDirGlob:
# # #         i = Image.open(fn)
# # #         info = i._getexif()
# # #         for tag, value in info.items():
# # #             decoded = TAGS.get(tag, tag)
# # #             ret[decoded] = value
# # #     return ret

# # # def dateCreateFix(fndir):
# # #     import datetime, os
# # #     ret = {}
# # #     for fn in fndir:
# # #         info = os.stat(fn)
# # #         ctime = info[9]
# # #         d = datetime.date.fromtimestamp(ctime)
# # #         d = d.isocalendar(datetime.date.fromtimestamp(d))
# # #         d = d.strftime("%Y-%m-%d")
# # #     return ret


# Query Mysql DB using 2 attribs. Filed(ie. 'colorstyle', param(ie.'302332901'))

# def sqlQueryStyles(searchField,searchParam):
#     import sqlalchemy
#     #import os
#     #import sys
#     #import csv
#     #ret = {}
#     ##  Create Sql Engine and Connection Obj -- Connected  ---
#     ##  Includes local replicated server & remote connections
#     #engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')

#     engine = sqlalchemy.create_engine('mysql://root:root@localhost/data_imagepaths')
#     connection = engine.connect()

#     ## Create Query
#     #querymake = "select * from product_snapshot where " + searchField + " like %" + searchParam + "%"
#     querymake = "select * from product_snapshot where " + searchField + " = " + searchParam

#     engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
#     #querymake = "select * from " + searchtable + " where " + searchField + " = " + searchParam
#     #result = connection.execute("select * from product_snapshot where brand = 'Gucci'")
#     result = connection.execute(querymake)

#     ### Print Results of Query
#     for row in result:
#         print "colorstyle:",        row['colorstyle']
#         print "production status:", row['production_status']
#         print "brand:",             row['brand']
#         print "sample status:",     row['sample_status']
#         print "sample date:",       row['status_dt']
#     connection.close()
#     #return ret
# """
# Query EVENTS Mysql DB using 2 attribs. Filed(ie. 'colorstyle', param(ie.'302332901'))
# """
# def sqlQueryEvents(searchtable,searchField,searchParam):
#     import sqlalchemy
#     #import os
#     #import sys
#     #import csv
#     #ret = {}
#     ##  Create Sql Engine and Connection Obj -- Connected  ---
#     ##  Includes local replicated server & remote connections
#     #engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imagepaths')
#     engine = sqlalchemy.create_engine('mysql://root:root@192.168.21.111:3301/data_imports')
#     connection = engine.connect()

#     ## Create Query
#     #querymake = "select * from product_snapshot where " + searchField + " like %" + searchParam + "%"

#     querymake = "select * from " + searchtable + " where " + searchField + " = " + searchParam
#     #result = connection.execute("select * from product_snapshot where brand = 'Gucci'")
#     result = connection.execute(querymake)
#     rowsss = {}
#     ### Print Results of Query
#     for row in result:
#         print "colorstyle:",        row['colorstyle']
#         print "event group:",       row['event_group']
#         print "event id:",          row['event_id']
#         print "event title:",       row['event_title']
#         print "event start:",       row['ev_start']
#         #print "production status:", row['production_status']

#     connection.close()
#     return rowsss




# def sqlQueryEventsUpcoming():
#     import sqlalchemy
#     orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://jbragato:Blu3f!y@192.168.30.66:1531/dssprd1')
#     connection = orcl_engine.connect()
#     querymake_eventscal = "select atg_snp.event.id, atg_snp.event.start_date, atg_snp.event.event_description from atg_snp.event where atg_snp.event.start_date >= trunc(sysdate) order by start_date desc"
#     result = connection.execute(querymake_eventscal)
#     events = {}
#     for row in result:
#         event = {}
#         event['ID'] = row['ID']
#         event['START_DATE'] = row['START_DATE']
#         event['EVENT_DESCRIPTION'] = row['EVENT_DESCRIPTION']
#         events[row['ID']] = event

#     print events
#     connection.close()
#     return events





# ##########
# ############ AJAX CLASSES

# import asyncore, socket

# class HTTPClient(asyncore.dispatcher):

#     def __init__(self, host, path):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.connect( (host, 80) )
#         self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % path

#     def handle_connect(self):
#         pass

#     def handle_close(self):
#         self.close()

#     def handle_read(self):
#         print self.recv(8192)

#     def writable(self):
#         return (len(self.buffer) > 0)

#     def handle_write(self):
#         sent = self.send(self.buffer)
#         self.buffer = self.buffer[sent:]


# #client = HTTPClient('www.python.org', '/')
# #asyncore.loop()


# import asyncore
# import socket

# class EchoHandler(asyncore.dispatcher_with_send):

#     def handle_read(self):
#         data = self.recv(8192)
#         if data:
#             self.send(data)

# class EchoServer(asyncore.dispatcher):

#     def __init__(self, host, port):
#         asyncore.dispatcher.__init__(self)
#         self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.set_reuse_addr()
#         self.bind((host, port))
#         self.listen(5)

#     def handle_accept(self):
#         pair = self.accept()
#         if pair is not None:
#             sock, addr = pair
#             print 'Incoming connection from %s' % repr(addr)
#             handler = EchoHandler(sock)
# ###  Start Server
# #server = EchoServer('localhost', 8080)
# #asyncore.loop()
# import asynchat

# class HttpRequestHandler(asynchat.async_chat):

#     def __init__(self, sock, addr, sessions, log):
#         asynchat.async_chat.__init__(self, sock=sock)
#         self.addr = addr
#         self.sessions = sessions
#         self.ibuffer = []
#         self.obuffer = ""
#         self.set_terminator("\r\n\r\n")
#         self.reading_headers = True
#         self.handling = False
#         self.cgi_data = None
#         self.log = log

#     def collect_incoming_data(self, data):
#         """Buffer the data"""
#         self.ibuffer.append(data)

#     def found_terminator(self):
#         if self.reading_headers:
#             self.reading_headers = False
#             self.parse_headers("".join(self.ibuffer))
#             self.ibuffer = []
#             if self.op.upper() == "POST":
#                 clen = self.headers.getheader("content-length")
#                 self.set_terminator(int(clen))
#             else:
#                 self.handling = True
#                 self.set_terminator(None)
#                 self.handle_request()
#         elif not self.handling:
#             self.set_terminator(None) # browsers sometimes over-send
#             self.cgi_data = parse(self.headers, "".join(self.ibuffer))
#             self.handling = True
#             self.ibuffer = []
#             self.handle_request()



# #### Walks a Dir and returns a Dict
# def recursive_dirlist(rootdir):
#     import os
#     walkedlist = []
#     for dirname, subdirnames, filenames in os.walk(rootdir):
#         # append path of all filenames to walkedlist
#         for filename in filenames:
#             file_path = os.path.abspath(os.path.join(dirname, filename))
#             if os.path.isfile(file_path):
#                 walkedlist.append(file_path)
#     # Advanced usage:
#     # editing the 'dirnames' list will stop os.walk() from recursing into there.
#     #if '.git' in dirnames:
#     # don't go into any .git directories.
#     #    dirnames.remove('.git')
#     walkedset = list(set(sorted(walkedlist)))
#     return walkedset

