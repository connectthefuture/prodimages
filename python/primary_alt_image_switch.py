#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Path to file below is from the mountpoint on FTP, ie /mnt/images..
## Download via FTP
def getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=None, new_alt=None, ext='.png', destdir=None):
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
        outfile = os.path.join(os.path.abspath(destdir), colorstyle + '_' + str(old_alt) + ext)
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

        outfile1 = os.path.join(os.path.abspath(destdir), colorstyle + '_' + str(new_alt) + ext)
        outfile2 = os.path.join(os.path.abspath(destdir), colorstyle + '_' + str(old_alt) + ext)

        destfile1 = open(outfile1, "wb")
        destfile2 = open(outfile2, "wb")

        session = ftplib.FTP(ftp_host, ftp_user, ftp_pass)    
        session.retrbinary("RETR " + remote_pathtofile1, destfile1.write, 8*1024)
        session.retrbinary("RETR " + remote_pathtofile2, destfile2.write, 8*1024)
        destfile1.close()
        destfile2.close()
        session.quit()

        return [os.path.abspath(outfile1), os.path.abspath(outfile2)]

def getpngall_ftp_netsrv101(colorstyle, destdir=None):
    import os
    countOne = 0
    countAlt = 0
    netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
    colorstyle = str(colorstyle)
    ext     = '.png'

    netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext)

    if not destdir:
        destdir = os.path.abspath('.')    
    colorstyle_file = os.path.join(destdir, colorstyle + ext)
    
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
                colorstyle_filealt = os.path.join(destdir, 'ALT', colorstylealt)

                netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)

                #error_check = urllib.urlopen(netsrv101_url_filealt)
                #urlcode_value = error_check.getcode()
                #if urlcode_value == 200:
                colorstyle_filealt_root = os.path.join(destdir, 'ALT')
                if os.path.isdir(colorstyle_filealt_root):
                    pass
                else:
                    os.makedirs(colorstyle_filealt_root)

                if url_download_file(netsrv101_url_filealt, colorstyle_filealt):
                    url_download_file(netsrv101_url_filealt, colorstyle_filealt)
                    countAlt += 1
            except IOError:
                pass
    except IOError:
        pass

#ex currentalt_newalt_pairs=tuple((1,4,))
def main(colorstyle=None, currentalt_newalt_pairs=None, destdir=None):
    import os, sys, glob
    os.chdir(os.path.dirname(__file__))
    import magicColorspaceReloadSwitcher as magickProcLoad
    uploaddir = '/mnt/Post_Complete/ImageDrop'
    if not destdir:
        try:
            destdir = '/mnt/Post_Complete/Complete_to_Load/reprocess'
            if os.path.isdir(destdir):
                destdir_reproc = destdir
                destdir = os.path.join(destdir_reproc, str(colorstyle))
                pass            
            else:
                destdir = os.path.join(os.path.abspath(os.path.expanduser('~')), 'Pictures', 'reprocess')
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
        except:
            destdir = os.path.abspath('.')

    # # Clean out desination dir prior to running new files
    cleardest = glob.glob(os.path.join(destdir, '*.??g'))
    # filter(os.path.isfile, os.listdir(destdir))
    if cleardest:
        for image in cleardest:
            import shutil, os

            try:
                os.remove(os.path.abspath(image))
            except:
                pass

    if len(currentalt_newalt_pairs) == 2:
        old_alt = currentalt_newalt_pairs[0]
        new_alt = currentalt_newalt_pairs[1]
        if old_alt != new_alt:
            # Download Zoom of both files renaming on dest dir save
            res = getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=old_alt, new_alt=new_alt, destdir=destdir)
            os.chdir(destdir)
            # Process newely named files and upload
            root_img_dir = destdir
            magickProcLoad.main(root_img_dir=root_img_dir, destdir=uploaddir)
            import shutil
            shutil.rmtree(root_img_dir)
            print 'Done Switching Style {2} Image #{0} With Image #{1}'.format(old_alt, new_alt, colorstyle)
    
    elif len(currentalt_newalt_pairs) == 1 and str(currentalt_newalt_pairs[0]).isdigit():
        old_alt = currentalt_newalt_pairs[0]
        res = getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=old_alt, destdir=destdir)
        # Reprocess Downloaded Style's Image and re-upload
        os.chdir(destdir)
        root_img_dir = destdir
        magickProcLoad.main(root_img_dir=root_img_dir, destdir=uploaddir)
        import shutil
        shutil.rmtree(root_img_dir)
        print 'Done Reloading Image {0} For Only the Main for Style {1} to {2}'.format(old_alt, colorstyle, uploaddir)
        print 'Deleted dir --> {0}'.format(root_img_dir)

    ## reload ALL styles's images
    elif str(currentalt_newalt_pairs[0]).upper() == str('ALL'):
        os.chdir(destdir)
        root_img_dir = destdir
        getpngall_ftp_netsrv101(colorstyle, destdir=root_img_dir)
        magickProcLoad.main(root_img_dir=root_img_dir, destdir=uploaddir)
        import shutil
        shutil.rmtree(root_img_dir)
        print 'Done Reloading ALL Images for Style {0} to {1}'.format(colorstyle,uploaddir)
        print 'Deleted dir --> {0}'.format(root_img_dir)
    else:
         print 'Pair Tuple aint len 1 or 2. Thats too bad. Why not try something else that works?'
         pass

    ## Clear downloaded pngs from destdir, leaving uploaded files in 1/uploaded dir 
    # todelete1 = glob.glob(os.path.join(destdir, '*.*g'))
    # todelete2 = glob.glob(os.path.join(destdir, '*/*.??g'))
    # todelete = todelete1 + todelete2
    # #filter(os.path.isfile, os.listdir(destdir))
    # for image in todelete:
    #     import shutil,os
    #     try:
    #         os.remove(os.path.abspath(image))
    #     except:
    #         pass
        #shutil.rmtree()
        #shutil.rmtree()

    # if todelete:
    #     for f in todelete:
    #         os.remove(os.path.abspath(f))
    #         print 'Deleted {}'.format(os.path.abspath(f))
    # else:
    #     pass


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
            a1 = 1
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
        results = main(colorstyle=colorstyle, currentalt_newalt_pairs=pairs, destdir=None)
        print 'Success ', colorstyle, results,'results'
    else:
        try:
            print 'Utter failure in ', os.path.abspath(__file__)
        except:
            pass
            print 'Total Utterfailure ', colorstyle
