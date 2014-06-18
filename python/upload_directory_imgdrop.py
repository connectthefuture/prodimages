#!/usr/bin/env python
import os, sys, re, csv




##### Upload tmp_loading dir to imagedrop via FTP using Pycurl  #####
def pycurl_upload_imagedrop(img):
    import pycurl, os
    #import FileReader
    localFileName = localFilePath.split('/')[-1]

    mediaType = "8"
    ftpURL = "ftp://file3.bluefly.corp/ImageDrop/"
    ftpFilePath = os.path.join(ftpURL, localFileName)
    ftpUSERPWD = "imagedrop:imagedrop0"

    if localFilePath != "" and ftpFilePath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.setopt(pycurl.URL, ftpFilePath)
        #c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
        #c.setopt(pycurl.FORBID_REUSE, 1)
        #c.setopt(pycurl.FRESH_CONNECT, 1)
        f = open(localFilePath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
        #c.setopt(pycurl.READFUNCTION, f.read());        
        #c.setopt(pycurl.READDATA, f.read()); 
        c.setopt(pycurl.UPLOAD, 1L)

        try:
            c.perform()
            c.close()
            print "Successfully Uploaded --> {0}".format(localFileName)
            ## return 200
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr
            try:
                c.close()
            except:
                print "Couldnt Close Cnx"
                pass
            return errno

#####
###
## backup for 56 then 7 curl err            
def upload_to_imagedrop(img):
    import ftplib
    session = ftplib.FTP('file3.bluefly.corp', 'imagedrop', 'imagedrop0')
    fileread = open(file, 'rb')
    filename = str(file.split('/')[-1])
    session.cwd("ImageDrop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit()

#[ shutil.move(file, os.path.join(tmp_loading, os.path.basename(file))) for file in load_jpgs ]

## UPLOAD FTP with PyCurl everything in tmp_loading
try:
    root_dir = sys.argv[1]
except:
    root_dir = os.path.abspath('.')
    
tmp_loading = os.path.join(root_dir, 
import time
upload_tmp_loading = glob.glob(os.path.join(tmp_loading, '*.*g'))
for upload_file in upload_tmp_loading:
    #### UPLOAD upload_file via ftp to imagedrop using Pycurl
    ## Then rm loading tmp dir
    try:
        code = pycurl_upload_imagedrop(upload_file)
        if code:
            print code, upload_file
            time.sleep(float(3))
            try:
                ftpload_to_imagedrop(upload_file)
                print "Uploaded {}".format(upload_file)
                time.sleep(float(.3))
                shutil.move(upload_file, archive_uploaded)
            except:
                pass
        else:
            print "Uploaded {}".format(upload_file)
            time.sleep(float(.3))
            shutil.move(upload_file, archive_uploaded)
    except:
        print "Error moving Finals to Arch {}".format(file)