#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import pdb; pdb.set_trace()

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

def url_download_file(url, filepath):
    import urllib
    try:
        urllib.urlretrieve(url, filepath)
        print "Retrieved: " + url + " ---> " + filepath
        return filepath
    except:
        print 'FAILED ', url, filepath
        pass

from timeout import timeout, TimeoutError
@timeout(7)
def prompt_confirm():
    try:
        input_from_user = str(raw_input('\n\nEnter "Yes" to begin: \tYou have 7 seconds to cancel download\n\n-----\n-----\n\n'))
        return input_from_user
    except TimeoutError:
        print 'timeout signaled: proceeding with download.'
        return 'Yes'

def listcontents_ftplib(ftp_dir, remote_dir='', ext_filter='', download='', destdir='', range_tuple=(1, '',)):
    import ftplib, collections, re
    from os import path, makedirs
    from datetime import datetime, timedelta
    host = 'netsrv101.l3.bluefly.com'
    login_url_string  = 'ftp://imagedrop:imagedrop0@' + host
    netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images'
    session = ftplib.FTP(host, 'imagedrop', 'imagedrop0')
    if not remote_dir:
        rootdir = '/mnt/images'
        reldir = path.join("images", ftp_dir)
        remote_dir = path.join(rootdir, reldir)
        try:
            session.cwd(reldir.split('/')[0])
            session.cwd(reldir.split('/')[1])
            print 'Remote Directory at URL:\t\t{}\nParentDir:\t\t{}.'.format(remote_dir, session.pwd())
        except ftplib.error_perm:
            print session.pwd(), '1 --55> ', remote_dir, ' Rem <-- --> Rel ', reldir
            print session.nlst()
            session.cwd("images")
            print session.pwd(), '2 --58> ', remote_dir, ' Rem <-- --> Rel ', reldir
            print session.nlst()
            session.cwd(ftp_dir)
            print 'Remote Directory at URL: {} does not exist, closing ftp session.'.format(remote_dir)
            #session.close()
        except AttributeError:
            print '64 AttributeError '
        finally:
            #dirlist = session.nlst()
            print session.pwd(), ' <-- 4 - Present'
            pass
    dirlist = session.nlst()
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
                range_bounds = int(range_tuple[0])
                if range_bounds > delta.days:
                    ftpmodtime_dict[path.join(host, remote_dir, fname)] = [delta.days, moddate] # .strftime("%Y%m%d %H:%M:%S")
                    cnt += 1
                    print fname, '\t\t\t\t\t Count Index -- {}\n\t\t\t\t\t Date: {}\vModified a mere {} Days Ago'.format(cnt, moddate.strftime("%b %d, %Y"), delta.days)
                else:
                    print fname, ' \t\t\t\t ModDate - {} - Beyond Date Bounds'.format(moddate.strftime("%b %d, %Y"))
            else:
                print fname, ' \t\t\t Failed due to Filtering only {}'.format(ext_filter)
        #session.quit()
    except TypeError:
        print 'Type Error'
    except AttributeError:
        print '96 -- AttributeError Error'
    finally:
        #session.storbinary('STOR ' + filename, fileread, 8*1024)
        session.quit()
    sorted_ftpdict = collections.OrderedDict(sorted(ftpmodtime_dict.items(), key=lambda t: t[1][0], reverse=False))
    oldest_date = sorted_ftpdict.popitem()
    #final_message = 'End ',  ' <-- \nFiles Modified: ', cnt, '\t\tSince {0:%b %d -- %Y}'.format(oldest_date[1][1])
    sorted_ftpdict.update(zip(oldest_date[0],oldest_date[1]))
    if download is True:
        print '\n-----\n-----\nTo Download {0} Files\n\tLoaded Since {1:%b %d -- %Y} to \v{2}: '.format(cnt, oldest_date[1][1], destdir)
        confirm = prompt_confirm()
        start_cnt = cnt
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
                    res = url_download_file(srcpath_url, destpath)
                    downloaded_files_dict[k.split('/')[-1]] = destpath
                    print res
                    cnt -= 1
                    print 'Downloading ... {} Files Remain - File: {}'.format(cnt,destpath)
                print 'End ',  ' <-- \nFiles Modified: ', start_cnt, '\t\tSince {0:%b %d -- %Y}'.format(oldest_date[1][1])
                return downloaded_files_dict
            else:
                print 'Cannot Download {} Files without DOWNLOAD or download as the sys arg 3 or destdir kwarg, \nit is None currently'.format(cnt)
        else:
            print 'You responded: "-- {} --".\nWhich means you decided to forgo the download this time.'.format(confirm)
    else:
        print 'End ',  ' <-- \nFiles Modified: ', cnt, '\t\tSince {0:%b %d -- %Y}'.format(oldest_date[1][1])
        return sorted_ftpdict



def pycurl_ftp_download(imageurl=None, destdir=None, **kwargs):
    import pycurl, urllib
    from os import path
    filename = imageurl.split('/')[-1]
    if kwargs.get('destpath'):
        destpath = kwargs.get('destpath')
    else:
        destpath = path.join(destdir, filename)
    imageurl = path.join(*urllib.unquote(imageurl).split('\\'))
    mediaType = "8"
    if kwargs.get('ftpuser') or kwargs.get('ftppass'):
        ftpUSERPWD = '{ftpuser}:{ftppass}'.format(**kwargs)
    else:
        ftpUSERPWD = imageurl.split('@')[0].replace('ftp://', '')
    ftpURL = 'ftp://' + imageurl.split('@')[1]

    print 'FTP TRY --> ', imageurl, '\n\t-Dest--> ', destpath, '\n\t--UserPassUrl--> ', ftpUSERPWD, '-->| ', ftpURL
    if destpath != "" and imageurl != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.f = open(destpath, 'wb')
        c.setopt(pycurl.URL, ftpURL)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        c.setopt(pycurl.WRITEDATA, c.f)
        #m.add_handle(c)
        # store some info
        c.filename = destpath
        c.url = ftpURL

#        c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        #c.setopt(pycurl.INFILE, f)
        #c.setopt(pycurl.INFILESIZE, path.getsize(destdir))
        #c.setopt(pycurl.INFILESIZE_LARGE, path.getsize(destdir))
#        c.setopt(pycurl.READFUNCTION, f.read());
#        c.setopt(pycurl.READDATA, f.read());
        #c.setopt(pycurl.UPLOAD, 1L)

        try:
            c.perform()
            c.close()
            print "Successfully Retrieved --> {0}".format(filename)
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


if __name__ == '__main__':
    import sys
    from os import path, makedirs
    args = sys.argv[1:]
    if len(args) < 4:
        ext_filter = 'png'
    if len(args) == 2:
        listcontents_ftplib(args[0],ext_filter=ext_filter, range_tuple=(args[1],'',))
    elif len(args) == 3 and args[2].lower() == 'download':
        if args[2].upper() == 'DOWNLOAD':
            dest=path.join(path.abspath(path.expanduser('~')), 'Pictures', ext_filter.upper(), args[0])
            print dest, ' 1'
        else:
            dest=path.join(path.abspath('.'), 'FilesDownloaded', ext_filter.upper(), args[0])
            print dest, ' 2'
        listcontents_ftplib(args[0],ext_filter=ext_filter, range_tuple=(args[1],'',), download=True, destdir=dest)
    else:
        listcontents_ftplib(args[0],ext_filter=ext_filter)
