#!/usr/bin/env python

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
    walkedset = walkedlist.append(file_path)
    return walkedset


def organize_files_by_4digit(pathname,destdir):
    import os, sys, re, shutil
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
    #pathname = sys.argv[1]
    #if not destdir():
    #    destdir = sys.argv[2]
    if os.path.isfile(pathname):
        #try:
        infile = os.path.abspath(pathname)
        filename, ext = os.path.splitext(infile)
        zimages_name = os.path.split(infile)[-1]
        zimages_dir = zimages_name[:4]
        zimages_dir = os.path.join(destdir, zimages_dir)
        zimages_filepath = os.path.join(zimages_dir, zimages_name)
        #print infile, zimages_filepath

        ## Try to make 4 digit directory or pass if already present
        try:
            os.mkdir(zimages_dir, 16877)
        except OSError:
            pass

        if os.path.isfile(zimages_filepath):
            os.remove(zimages_filepath)
            shutil.move(pathname,zimages_filepath)
        else:
            shutil.move(pathname,zimages_filepath)
            #pass


import os, sys, re, shutil,glob
if __name__ == "__main__":
    destdir = '/mnt/Production_Raw/.zImages_1'
    try:
        if len(sys.argv[1:]) <= 2:

            destdir = sys.argv[2]
    except:
        destdir = '/mnt/Production_Raw/.zImages_1'

    if sys.argv[1] != 'GLOBOUT':
        try:
            if os.path.isdir(sys.argv[1]):
                rootdir = sys.argv[1]
                filepaths = recursive_dirlist(rootdir)
                for pathname in filepaths:
                    organize_files_by_4digit(pathname,destdir=destdir)
            elif os.path.isfile(sys.argv[1]):
                organize_files_by_4digit(os.path.abspath(sys.argv[1]),destdir=destdir)
        except:
            print "Sys Arg 1 must be the Root directory with files to organize"
    elif sys.argv[1] == 'GLOBOUT':
        destdir = '/mnt/Production_Raw/.zImages_1'
        try:
            g='/mnt/Production_Raw/PHOTO_STUDIO_OUTPUT/ON_FIGURE/*/*/OUTPUT/*CR2.jpg'
            globbed_output_jpgs = glob.glob(g)
            print globbed_output_jpgs
            ##if len(globbed_output_jpgs) > 0:
            for f in globbed_output_jpgs:
                try:
                    organize_files_by_4digit(os.path.abspath(f),destdir=destdir)
                except:
                    pass
        except:
            pass




    #if len(sys.argv[1:]) >= 3:
#        if os.path.isdir(sys.argv[:][0]):
#            destdir=sys.argv[1]
#        else:
#            destdir = '/mnt/Production_Raw/.zImages_1'
#
#        arglist = sys.argv[1:]
#        for f in arglist:
#            organize_files_by_4digit(os.path.abspath(f), destdir=destdir)
