# -*- coding: utf-8 -*-
"""
Created on WED JUL 24 11:23:55 2013

@author: jb
"""
"""
###
{{ Walk Root Directory and Return List or all Files in all Subdirs too }}
"""
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

"""
###
{{ Download File from FTP Server netsrv101 }}
"""
def getbinary_ftp_netsrv101(pathtofile, outfile=None):
    # fetch a binary file
    ftp = ftplib.FTP("netsrv101.l3.bluefly.com")
    ftp.login("imagedrop", "imagedrop0")
    if outfile is None:
        outfile = sys.stdout
        ftp.retrbinary("RETR " + pathtofile, outfile.write)

"""
###
{{  Upload File to imagedrop via FTP }}
"""
def upload(file):
    ftpup = ftplib.FTP("file3.bluefly.corp/ImageDrop/")
    ftpup.login("imagedrop", "imagedrop0")
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftpup.storlines("STOR " + file, open(file))
    else:
        ftpup.storbinary("STOR " + file, open(file, "rb"), 1024)
