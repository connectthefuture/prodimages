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
    return walkedlist


def organize_files_by_4digit(pathname,destdir=None):
    import os, sys, re, shutil
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
    pathname = sys.arg[1]
    if not destdir():
        destdir = sys.argv[2]
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
        
        shutil.move(pathname,zimages_filepath)
        
        
import os, sys, re, shutil
##if __name__ == "__main__":
if sys.arg[1]:
    try:
        rootdir = sys.arg[1]
    except:
        print "Sys Arg 1 must be the directory with files to organize"

    try:
        destdir = sys.argv[2]
    except:
        destdir = '/mnt/Production_Raw/.zImages_1'

    filepaths = recursive_dirlist(rootdir)
    for pathname in filepaths:
        organize_files_by_4digit(pathname,destdir=destdir)
