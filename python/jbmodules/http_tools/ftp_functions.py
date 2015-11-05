#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
## backup for 56 then 7 curl err
def upload_to_imagedrop(img):
    import ftplib
    session = ftplib.FTP('netsrv101.l3.bluefly.com', 'imagedrop', 'imagedrop0')
    modified_time = session.sendcmd('MDTM ' + img)
    fileread = open(file, 'rb')
    filename = str(file.split('/')[-1])
    #session.cwd("ImageDrop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit()


def dload_ftplib(destpath, filename):
    import ftplib
    from os import path
    session = ftplib.FTP('netsrv101.l3.bluefly.com', 'imagedrop', 'imagedrop0')
    filewrite = open(path.join(destpath, filename), 'wb')
    remote_dir = path.join("/mnt/images/images", filename[:4])
    session.cwd(remote_dir)
    session.retrbinary('RETR ' + filename, filewrite.write)
    filewrite.close()
    session.quit()


def listcontents_ftplib(ftp_dir, remote_dir=None, ext_filter='', range_tuple=(1, '',)):
    import ftplib, collections, re
    from os import path
    from datetime import datetime, timedelta
    host = 'netsrv101.l3.bluefly.com'
    session = ftplib.FTP(host, 'imagedrop', 'imagedrop0')
    if not remote_dir:
        remote_dir = path.join("/mnt/images/images", ftp_dir)
    session.cwd(remote_dir)
    dirlist = session.nlst()
    print session.pwd(), dirlist
    cnt = 0
    ftpmodtime_dict = {}
    regex_filter = re.compile(r'.+?\.' + ext_filter)
    try:
        for fname in dirlist:
            if regex_filter.findall(fname):
                modified_time_ftp = session.sendcmd('MDTM ' + fname)
                moddate = datetime.strptime(modified_time_ftp.split()[-1], "%Y%m%d%H%M%S")
                # if not range_tuple[0]:
                #     start = datetime.now() - timedelta(days=range_tuple[0])
                #     #start = timedelta(range_tuple[0]) #datetime.strptime(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"), "%Y%m%d%H%M%S")
                #     delta = datetime.now() - start
                #     #end   = timedelta(days=range_tuple[1])
                # else:range_tuple[0]
                delta = datetime.now() - moddate # timedelta(days=range_tuple[0])
                range_bounds = range_tuple[0]
                if range_bounds > delta.days:
                    ftpmodtime_dict[path.join(host, remote_dir, fname)] = [delta.days, moddate] # .strftime("%Y%m%d %H:%M:%S")
                    cnt += 1
                else:
                    print fname, ' Failed -- Out of Date Bounds'
            else:
                print fname, ' Failed due to Filtering'
    except TypeError:
        print 'Type Error'
    finally:
        print 'End ', cnt, ' <-- TotalCount'
        #session.storbinary('STOR ' + filename, fileread, 8*1024)
        session.quit()
    sorted_ftpdict = collections.OrderedDict(sorted(ftpmodtime_dict.items(), key=lambda t: t[1][0], reverse=False))
    return sorted_ftpdict


if __name__ == '__main__':
    import sys
    if len(sys.argv[1:]) == 2:
        listcontents_ftplib(sys.argv[1],ext_filter='png', range_tuple=(sys.argv[2],'',))
    else:
        listcontents_ftplib(sys.argv[1],ext_filter='png'
