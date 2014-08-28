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


#ex currentalt_newalt_pairs=tuple((1,4,))
def main(colorstyle=None, currentalt_newalt_pairs=None, destdir=None):
    import os, sys
    import magicColorspaceModAspctLoad as magickProcLoad
    if not destdir:
        try:
            destdir = '/mnt/Post_Complete/Complete_to_Load/.tmp_processing'
            if os.path.isdir(destdir):
                print 'Isdir'
                pass
            
            else:
                destdir = os.path.join(os.path.abspath(os.path.expanduser('~')), 'Pictures')
        except:
            destdir = os.path.abspath('.')
    print destdir
    if len(currentalt_newalt_pairs) == 2:
        old_alt = currentalt_newalt_pairs[0]
        new_alt = currentalt_newalt_pairs[1]
        if old_alt != new_alt:
            # Download Zoom of both files renaming on dest dir save
            res = getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=old_alt, new_alt=new_alt, destdir=destdir)
            
            # Process newely named files and upload
            magickProcLoad.main(root_img_dir=destdir)
            print res
            print 'Done Switching Style {2} Image #{0} With Image #{1}'.format(old_alt, new_alt, colorstyle)
            return res
    elif len(currentalt_newalt_pairs) == 1:
        old_alt = currentalt_newalt_pairs[0]
        res = getpngpair_ftp_netsrv101_renamed_output(colorstyle, old_alt=old_alt, destdir=destdir)
        # Reprocess Downloaded Style's Image and re-upload
        magickProcLoad.main(root_img_dir=destdir)
        print res
        print 'Done Reloading Image {0} For Style {1}'.format(old_alt, colorstyle)
        return res
    else:
         print 'Pair Tuple aint len 1 or 2. Thats too bad. Why not try something else that works?'
         pass


if __name__ == '__main__':
    import sys
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
        main(colorstyle=colorstyle, currentalt_newalt_pairs=pairs, destdir=None)
        print 'Success ', colorstyle, #currentalt_newalt_pairs
    else:
        print 'Utterfailure in ', os.path.abspath(__file__)

