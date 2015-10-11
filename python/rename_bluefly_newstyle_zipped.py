#!/usr/bin/env python
import os, sys, re, csv
def pycurl_download_netsrv101(colorstyle, alt=None, save_dir=None):
    import pycurl, os
    #import FileReader
    if alt:
        colorstyle = "{0}_{1}".format(colorstyle, alt)

    if not save_dir:
        save_dir = os.path.abspath(os.path.join(os.path.expanduser('~'), 'Share'))
    if os.path.isdir(save_dir):
        pass #saveDir = os.path.abspath(os.path.abspath(os.path.expanduser('~'), 'Share'))
    else:
        save_dir = os.path.abspath(os.path.expanduser('~'))
    
    localFileName = "{0}.png".format(colorstyle)
    localFilePath = os.path.join(save_dir, localFileName)
    
    mediaType = "8"
    ftpURL = r'ftp://netsrv101.l3.bluefly.com//mnt/images/images/'
    
    ftpFilePath = os.path.join(ftpURL, colorstyle[:4], localFileName)
    ftpUSERPWD = "imagedrop:imagedrop0"

    if localFilePath != "" and ftpFilePath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.f = open(localFilePath, 'wb')
        c.setopt(pycurl.URL, ftpFilePath)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        c.setopt(pycurl.WRITEDATA, c.f)
        #m.add_handle(c)
        # store some info
        c.filename = localFilePath
        c.url = ftpFilePath

#        c.setopt(pycurl.PORT , 21)

        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        
        #c.setopt(pycurl.INFILE, f)
        #c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        #c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
#        c.setopt(pycurl.READFUNCTION, f.read());        
#        c.setopt(pycurl.READDATA, f.read()); 
        #c.setopt(pycurl.UPLOAD, 1L)

        try:
            c.perform()
            c.close()
            print "Successfully Downloaded --> {0}".format(localFileName)
            return localFileName
        except pycurl.error, error:
            errno, errstr = error
            print 'An error occurred: ', errstr
            try:
                c.close()
            except:
                print "Couldnt Close Cnx"
                pass
            return errno
#urlpaths=['https://optcentral.com/optportal/catalog/2712/large/11040_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11038_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11039_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11026_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11025_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11022_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11042_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11024_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11041_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/11023_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10902_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10904_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10906_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10907_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10908_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10910_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10911_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10912_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10913_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10915_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10918_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10920_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10921_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10922_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10923_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10924_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10925_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10927_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10930_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10931_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10932_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10934_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10936_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10937_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10938_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10940_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10943_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10946_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10949_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10952_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10953_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10954_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10955_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10956_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10957_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10958_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10960_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10962_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10963_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10964_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10965_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10966_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10967_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10968_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10974_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10976_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10977_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10978_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10979_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10980_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10981_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10985_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10986_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10987_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10988_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10989_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10990_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10991_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10992_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10993_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10994_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10995_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10996_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10997_1_WB.jpg', 'https://optcentral.com/optportal/catalog/2712/large/10998_1_WB.jpg']

rootdir = sys.argv[1]

oldnums = ['336482201', '336482202', '336482301', '336482401', '336482402', '336482403', '336482404', '336482405', '336482501', '336482502', '336482503', '336482601', '336482602', '336482701', '336482702', '336482703', '336482704', '336482705', '336482706', '336482801', '336482802', '336482803', '336482804', '336482805', '336482901', '336482902', '336482903', '336482904', '336483001', '336483002', '336483003', '336483004', '336483005', '336483006', '336483007', '336483008', '336483101', '336483102', '336483103', '336483104', '336483105', '336483106', '336483107', '336483108', '336483109', '336483110', '336483111', '336483112', '336483113', '336483114', '336483201', '336483202']
newnums = ['336674201', '336674301', '336674401', '336674501', '336674601', '336674701', '336674801', '336674901', '336675001', '336675101', '336675201', '336675301', '336675401', '336675501', '336675601', '336675701', '336675801', '336679201', '336679301', '336675901', '336676001', '336676101', '336676201', '336676301', '336676401', '336676501', '336676601', '336676701', '336676801', '336676901', '336677001', '336677101', '336677201', '336677301', '336677401', '336677501', '336677601', '336677701', '336677801', '336677901', '336678001', '336678101', '336678201', '336678301', '336678401', '336678501', '336678601', '336678701', '336678801', '336678901', '336679001', '336679101']

zipped = zip(oldnums,newnums)



import urllib2, httplib, requests,os
for su in zipped:
    
    oldnum = su[0]
    newnum = su[1]
    #urlget = su[1]
    #urlsavepost = os.path.join('/Users/johnb/Pictures', str(newnum + '_1.jpg'))
    #urlsavepre = os.path.join('/Users/johnb/Pictures', str(oldnum.split('/')[-1]))
    #print urlsavepost
    #res = requests.get(oldnum, stream=True, timeout=1)
    oldname = pycurl_download_netsrv101(oldnum,save_dir=os.path.abspath(rootdir))
    
    try:
        os.rename(os.path.join(rootdir,oldname), os.path.join(rootdir,oldname).replace(oldnum,newnum))
    except:
        pass
    # cnx=httplib.HTTPSConnection()
    # res=cnx.request('GET', urlget).read()
#    #response = urllib2.urlopen(req).read()
#    with open(urlsavepost, 'ab+') as f:
#        f.write(res.content)
#        f.close()