#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Path to file below is from the mountpoint on FTP, ie /mnt/images..

def url_download_file(url,filepath):
    import urllib, subprocess
    try:
        urllib.urlretrieve(url, os.path.join(filepath))
        #print "Retrieved: " + url + " ---> " + filepath
        return filepath
    except:
        #print  'FAILED ', url, filepath
        pass

## Download via FTP
def getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=None, new_alt=None, ext='.png', root_img_dir=None):
    # fetch a binary file from primary bfly site repo
    import ftplib,sys, os
    ftp_host        = "netsrv101.l3.bluefly.com" 
    ftp_user        = "imagedrop"
    ftp_pass        = "imagedrop0"
    remote_img_dir  = "/mnt/images/images"
    fname_parent    = colorstyle[:4]

    if int(old_alt) == 1:
        fname1    = colorstyle + ext
    elif int(old_alt) > 1:
        altext1   = int(old_alt) - 1
        fname1    = colorstyle + '_alt0' + str(altext1) + ext
    
    # Reprocess and upload old_alt img# for style in case jpgs failed to generate and load
    if not new_alt:
        remote_pathtofile = os.path.join(ftp_host, remote_img_dir, fname_parent, fname1)
        outfile = os.path.join(os.path.abspath(root_img_dir), colorstyle + '_' + str(old_alt) + ext)
        destfile = open(outfile, "wb")
        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)    
        session.retrbinary("RETR " + remote_pathtofile, destfile.write, 8*1024)
        destfile.close()
        session.quit()
        return [os.path.abspath(outfile)]
    # Switch position of new and old images
    else:
        if int(new_alt) > 1:
            altext2   = int(new_alt) - 1
            fname2    = colorstyle + '_alt0' + str(altext2) + ext
        elif int(new_alt) == 1:
            fname2     = colorstyle + ext

        remote_pathtofile1 = os.path.join(ftp_host, remote_img_dir, fname_parent, fname1)
        remote_pathtofile2 = os.path.join(ftp_host, remote_img_dir, fname_parent, fname2)

        outfile1 = os.path.join(os.path.abspath(root_img_dir), colorstyle + '_' + str(new_alt) + ext)
        outfile2 = os.path.join(os.path.abspath(root_img_dir), colorstyle + '_' + str(old_alt) + ext)

        destfile1 = open(outfile1, "wb")
        destfile2 = open(outfile2, "wb")

        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)    
        session.retrbinary("RETR " + remote_pathtofile1, destfile1.write, 8*1024)
        session.retrbinary("RETR " + remote_pathtofile2, destfile2.write, 8*1024)
        destfile1.close()
        destfile2.close()
        session.quit()

        return [os.path.abspath(outfile1), os.path.abspath(outfile2)]

def getpngall_ftp_netsrv101(colorstyle, root_img_dir=None):
    import os
    countOne = 0
    countAlt = 0
    netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
    colorstyle = str(colorstyle)
    ext     = '.png'

    netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext)

    if not root_img_dir:
        root_img_dir = os.path.abspath('.')    
    colorstyle_file = os.path.join(root_img_dir, colorstyle + ext)
    
    print netsrv101_url_file, colorstyle_file
    try:
        url_download_file(netsrv101_url_file, colorstyle_file)
        countOne += 1
        alt = 0
        for x in xrange(1,6):
            try:
                alt = x
                ext_ALT = '_alt0{0}{1}'.format(str(alt),ext)
                colorstylealt = colorstyle + ext_ALT
                colorstyle_filealt = os.path.join(root_img_dir, colorstylealt)

                netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)

                if url_download_file(netsrv101_url_filealt, colorstyle_filealt):
                    url_download_file(netsrv101_url_filealt, colorstyle_filealt)
                    countAlt += 1
            except IOError:
                print 'IOERROR --> {} -- {}'.format(colorstyle, alt)
                pass
    except IOError:
        pass

#ex currentalt_newalt_pairs=tuple((1,4,))
def main(colorstyle=None, currentalt_newalt_pairs=None, root_img_dir=None):
    import os, sys, glob, sys
    sys.path.append(os.path.dirname(__file__))
    import magicColorspaceReloadSwitcher as magickProcLoad
    uploaddir = '/mnt/Post_Complete/ImageDrop'
    if not os.path.isdir(uploaddir):
        uploaddir = uploaddir.replace('/mnt/','/Volumes/')
    print uploaddir, root_img_dir, 'UPLOAD DIR THE' 
    if not root_img_dir:
        try:
            root_img_dir = '/mnt/Post_Complete/Complete_to_Load/reprocess'
            if os.path.isdir(root_img_dir):
                root_img_dir_reproc = root_img_dir
                root_img_dir = os.path.join(root_img_dir_reproc, str(colorstyle))
                print root_img_dir_reproc, ' root reproc and root --> ', root_img_dir
                if not os.path.isdir(root_img_dir):
                    os.makedirs(root_img_dir)
            elif os.path.isdir(root_img_dir.replace('/mnt/','/Volumes/')):
                root_img_dir = root_img_dir.replace('/mnt/','/Volumes/')                
                root_img_dir_reproc = root_img_dir
                root_img_dir = os.path.join(root_img_dir_reproc, str(colorstyle))
                if not os.path.isdir(root_img_dir):
                    os.makedirs(root_img_dir)
            else:
                root_img_dir = os.path.join(os.path.abspath(os.path.expanduser('~')), 'Pictures', 'reprocess')
                if not os.path.isdir(root_img_dir):
                    os.makedirs(root_img_dir)
        except:
            root_img_dir = os.path.abspath('.')
            'ROOT IS CURR ', root_img_dir
    # # Clean out desination dir prior to running new files
    cleardest = glob.glob(os.path.join(root_img_dir, '*.??g'))
    # filter(os.path.isfile, os.listdir(root_img_dir))
    if cleardest:
        for image in cleardest:
            import shutil, os

            try:
                os.remove(os.path.abspath(image))
            except:
                print image, ' IMAGE'
                pass

    if len(currentalt_newalt_pairs) == 2:
        old_alt = currentalt_newalt_pairs[0]
        new_alt = currentalt_newalt_pairs[1]
        if old_alt != new_alt:
            # Download Zoom of both files renaming on dest dir save
            res = getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=old_alt, new_alt=new_alt, root_img_dir=root_img_dir)
            os.chdir(root_img_dir)
            # Process newely named files and upload
            root_img_dir = root_img_dir
            magickProcLoad.main(root_img_dir=root_img_dir, destdir=uploaddir)
            import shutil
            shutil.rmtree(root_img_dir)
            print 'Done Switching Style {2} Image #{0} With Image #{1}'.format(old_alt, new_alt, colorstyle)
    
    elif len(currentalt_newalt_pairs) == 1 and str(currentalt_newalt_pairs[0]).isdigit():
        old_alt = currentalt_newalt_pairs[0]
        res = getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=old_alt, root_img_dir=root_img_dir)
        # Reprocess Downloaded Style's Image and re-upload
        os.chdir(root_img_dir)
        root_img_dir = root_img_dir
        magickProcLoad.main(root_img_dir=root_img_dir, destdir=uploaddir)
        print root_img_dir, ' ROOOOOTOOTOTO ', destdir
        import shutil
        shutil.rmtree(root_img_dir)
        print 'Done Reloading Image {0} For Only the Main for Style {1} to {2}'.format(old_alt, colorstyle, uploaddir)
        print 'Deleted dir --> {0}'.format(root_img_dir)

    ## reload ALL styles's images
    elif currentalt_newalt_pairs is None or str(currentalt_newalt_pairs[0]).upper() == str('ALL'):
        os.chdir(root_img_dir)
        root_img_dir = root_img_dir
        getpngall_ftp_netsrv101(colorstyle, root_img_dir=root_img_dir)
        print uploaddir, ' uploaddir'
        magickProcLoad.main(root_img_dir=root_img_dir, destdir=uploaddir)
        print os.listdir(root_img_dir), ' <-- root_img_dir'
        import shutil
        shutil.rmtree(root_img_dir)
        print 'Done Reloading ALL Images for Style {0} to {1}'.format(colorstyle,uploaddir)
        print 'Deleted dir --> {0}'.format(root_img_dir)
    else:
         print 'Pair Tuple aint len 1 or 2. Thats too bad. Why not try something else that works?'
         pass


##########################
##########################

if __name__ == '__main__':
    import sys, os
    pairs = ''
    try:
        colorstyle = sys.argv[1]
        try:
            a1 = sys.argv[2]
        except IndexError:
            # if only colorstylee provide assume to just reload the primary
            a1 = 'ALL'
    except:
        print 'You need at least 2 args, first is colorstyle then img # to Download. primary img is 1, etc. A 3rd arg can be the img# to swap with arg 2 or empty reloads the image only'
        pass

    try:
        a2 = sys.argv[3]
        pairs = tuple((a1,a2,))
    except IndexError:
        pairs = tuple((a1,))

    # Run it
    if colorstyle:
        print colorstyle, pairs
        results = main(colorstyle=colorstyle, currentalt_newalt_pairs=pairs)
        print 'Success ', colorstyle, results,'results'
    else:
        try:
            print 'Utter failure in ', os.path.abspath(__file__)
        except:
            pass
            print 'Total Utterfailure ', colorstyle
