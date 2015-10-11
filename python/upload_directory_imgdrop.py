#!/usr/bin/env python

##### Upload tmp_loading dir to imagedrop via FTP using Pycurl  #####
def pycurl_upload_imagedrop(img):
    import pycurl, os
    #import FileReader
    localFilePath = os.path.abspath(img)
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

def main(root_dir=None):
    ## UPLOAD FTP with PyCurl everything in tmp_loading
    import os, sys, re, csv, shutil, glob
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.[JjPpNnGg]{3}$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    if not root_dir:
        try:
            root_dir = sys.argv[1]
        except:
            root_dir = os.path.abspath('.')
    else:
        root_dir = root_dir
    
    archive_uploaded = os.path.join(root_dir, 'uploaded')
    tmp_failed = os.path.join(root_dir, 'failed_upload')
    try:
        os.makedirs(archive_uploaded, 16877)
    except:
        pass

    try:
        os.makedirs(tmp_failed, 16877)
    except:
        pass

    import time
    upload_tmp_loading = glob.glob(os.path.join(root_dir, '*.*g'))
    for upload_file in upload_tmp_loading:
        #### UPLOAD upload_file via ftp to imagedrop using Pycurl
        ## Then rm loading tmp dir
        if regex_valid_style.findall(upload_file):
            try:
                code = pycurl_upload_imagedrop(upload_file)
                if code == '200':
                    shutil.move(upload_file, archive_uploaded)
                    print "1stTryOK"
                elif code:
                    print code, upload_file
                    time.sleep(float(.3))
                    try:
                        ftpload_to_imagedrop(upload_file)
                        print "Uploaded {}".format(upload_file)
                        time.sleep(float(.3))
                        shutil.move(upload_file, archive_uploaded)
                    except:
                        shutil.move(upload_file, tmp_failed)
                        pass
                else:
                    print "Uploaded {}".format(upload_file)
                    time.sleep(float(.3))
                    shutil.move(upload_file, archive_uploaded)
            except shutil.Error:
                try:
                    shutil.move(upload_file, tmp_failed)
                except:
                    pass
            except OSError:
                print "Error moving Finals to Arch {}".format(file)
                shutil.move(upload_file, tmp_failed)
                pass
        else:
            shutil.move(upload_file, tmp_failed)

    try:
        if sys.argv[2]:
            destdir = os.path.abspath(sys.argv[2])
            for f in glob.glob(os.path.join(archive_uploaded, '*.*g')):
                shutil.move(f, destdir)
    except:
        pass
            