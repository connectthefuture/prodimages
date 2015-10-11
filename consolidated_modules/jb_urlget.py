
def url_download_fileslist_dbx(imglinkslist):
    import urllib,os,time,subprocess
    downloaddir = os.path.join(os.path.expanduser('~'), 'script_dowloads')
    for link in imglinkslist:
        try:
            filename = str(link.split('/')[-1])
            filepath =  os.path.join(downloaddir, filename)
            os.chdir(downloaddir)
            #url_start = time()
            downloadfile = urllib.urlretrieve(link, filepath)
            #url_end = time()
            #print "File %s Download Time -> %s" % (downloadfile, url_end - url_start)
        except AttributeError:
            print "Attribute Error -- None Type"
        except IOError:
            print "IO Error No File or Dir to save {0}".format(filepath)
        except OSError:
            print "OS Error {0}".format(filepath)
            return downloadfile
