# -*- coding: utf-8 -*-
"""
Created on WED JUL 24 11:23:55 2013

@author: jb
"""
"""
###
{{ Walk Root Directory and Return List or all Files in all Subdirs too }}
"""
<<<<<<< HEAD
=======

###########################################################################################################################################################
###########################################################################################################################################################
###      File System and Directory Related Functions       ################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################
>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0
def recursive_dirlist(rootdir):
    import os
    walkedlist = []
    for dirname, subdirnames, filenames in os.walk(rootdir):
        # append path of all filenames to walkedlist
        for filename in filenames:
            file_path = os.path.abspath(os.path.join(dirname, filename))
            if os.path.isfile(file_path):
                walkedlist.append(file_path)
    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    #if '.git' in dirnames:
    # don't go into any .git directories.
    #    dirnames.remove('.git')
    return walkedlist


<<<<<<< HEAD
=======

###########################################################################################################################################################
###########################################################################################################################################################
###      FTP Related Functions       ######################################################################################################################
###########################################################################################################################################################
###########################################################################################################################################################

>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0
"""
###
{{ Download File from FTP Server netsrv101 }}
"""
def getbinary_ftp_netsrv101(remote_pathtofile, outfile=None):
    # fetch a binary file
    import ftplib
    ftpdown = ftplib.FTP("netsrv101.l3.bluefly.com")
    ftpdown.login("imagedrop", "imagedrop0")
    if outfile is None:
        outfile = sys.stdout
    destfile = open(outfile, "wb")
    ftpdown.retrbinary("RETR " + remote_pathtofile, destfile.write, 8*1024)
    destfile.close()


"""
###
{{  Upload File to imagedrop via FTP }}
"""
<<<<<<< HEAD
## Upload to imagedrop via FTP
def upload(file):
    import ftplib
    ftpup = ftplib.FTP("file3.bluefly.corp/ImageDrop/")
    ftpup.login("imagedrop", "imagedrop0")
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftpup.storlines("STOR " + file, open(file))
    else:
        ftpup.storbinary("STOR " + file, open(file, "rb"), 8*1024)
=======
## backup for 56 then 7 curl err
def upload_to_imagedrop(file):
    import ftplib
    session = ftplib.FTP('file3.bluefly.corp', 'imagedrop', 'imagedrop0')
    fileread = open(file, 'rb')
    filename = str(file.split('/')[-1])
    session.cwd("ImageDrop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit()



### Better upload using Curl
## Upload to imagedrop via FTP
def pycurl_upload_imagedrop(localFilePath):
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
#        c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        f = open(localFilePath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
#        c.setopt(pycurl.READFUNCTION, f.read());
#        c.setopt(pycurl.READDATA, f.read());
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

>>>>>>> 00d5c280c263b375d191833004cfc6cf50e480b0

