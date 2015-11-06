#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb; pdb.set_trace()

###
# ## backup for 56 then 7 curl err
# def upload_to_imagedrop(img):
#     import ftplib
#     session = ftplib.FTP('netsrv101.l3.bluefly.com', 'imagedrop', 'imagedrop0')
#     modified_time = session.sendcmd('MDTM ' + img)
#     fileread = open(file, 'rb')
#     filename = str(file.split('/')[-1])
#     #session.cwd("ImageDrop/")
#     session.storbinary('STOR ' + filename, fileread, 8*1024)
#     fileread.close()
#     session.quit()
#
#
# def dload_ftplib(destpath, filename):
#     import ftplib
#     from os import path
#     session = ftplib.FTP('netsrv101.l3.bluefly.com', 'imagedrop', 'imagedrop0')
#     filewrite = open(path.join(destpath, filename), 'wb')
#     remote_dir = path.join("/mnt/images/images", filename[:4])
#     session.cwd(remote_dir)
#     session.retrbinary('RETR ' + filename, filewrite.write)
#     filewrite.close()
#     session.quit()


def listcontents_ftplib(ftp_dir, remote_dir=None, ext_filter='', range_tuple=(1, '',), download=False, destdir=None):
    import ftplib, collections, re
    from urllib import urlretrieve
    from os import path, makedirs
    from datetime import datetime, timedelta
    host = 'netsrv101.l3.bluefly.com'
    login_url_string  = 'ftp://imagedrop:imagedrop0@' + host
    session = ftplib.FTP(host, 'imagedrop', 'imagedrop0')
    if not remote_dir:
        rootdir = '/mnt/images'
        reldir = path.join("images", ftp_dir)
        remote_dir = path.join(rootdir, reldir)
    session.cwd(reldir)
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
                    print fname, ' \t\t\t Counted -- {}'.format(cnt)
                else:
                    print fname, ' \t\t\t Failed -- Out of Date Bounds'
            else:
                print fname, ' \t\t\t Failed due to Filtering'
        #session.quit()
    except TypeError:
        print 'Type Error'
    finally:
        print 'End ', cnt, ' <-- TotalCount'
        #session.storbinary('STOR ' + filename, fileread, 8*1024)
        session.quit()
    sorted_ftpdict = collections.OrderedDict(sorted(ftpmodtime_dict.items(), key=lambda t: t[1][0], reverse=False))
    if download is True:
        print 'To Download {} File to \v{}: '.format(cnt,destdir)
        confirm = str(raw_input('Enter "Yes" to begin: '))
        if confirm[0].lower() == 'y':
            downloaded_files_dict = {}

            if destdir:
                for k,v in sorted_ftpdict.items():
                    if path.exists(destdir):
                        pass
                    else:
                        makedirs(destdir)
                    srcpath_url = login_url_string + "/" + k
                    destpath = path.join(destdir, k.split('/')[-1])
                    res = urlretrieve(srcpath_url, destpath)
                    downloaded_files_dict[k.split('/')[-1]] = destpath
                    print res
                    print 'Finished Downloading {} Files to: {}'.format(cnt,destpath)
                    return downloaded_files_dict
            else:
                print 'Cannot Download {} Files without DOWNLOAD or download as the sys arg 3 or destdir kwarg, \nit is None currently'.format(cnt)
        else:
            print 'You responded: "-- {} --".\nWhich means you decided to forgo the download this time.'.format(confirm)
    else:
        print locals()
        return sorted_ftpdict


if __name__ == '__main__':
    import sys
    from os import path, makedirs
    if len(sys.argv[1:]) < 4:
        ext_filter = 'png'
    if len(sys.argv[1:]) == 2:
        listcontents_ftplib(sys.argv[1],ext_filter=ext_filter, range_tuple=(sys.argv[2],'',))
    elif len(sys.argv[1:]) == 3 and sys.argv[3].lower() == 'download':
        if sys.argv[3].upper() == 'DOWNLOAD':
            dest=path.join(path.expanduser('~'), 'Pictures', ext_filter.upper(), sys.argv[1])
        else:
            dest=path.join(path.abspath('.'), 'FilesDownloaded', ext_filter.upper(), sys.argv[1])
        listcontents_ftplib(sys.argv[1],ext_filter=ext_filter, range_tuple=(sys.argv[2],'',), download=True, destdir=dest)
    else:
        listcontents_ftplib(sys.argv[1],ext_filter=ext_filter)
