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
    walkedset = list(set(sorted(walkedlist)))
    return walkedset


def organize_files_by_4digit(pathname,destdir):
    import os, sys, re, shutil
    regex_jpeg = re.compile(r'.+?\.[a-zA-Z]{3}$')
    #pathname = sys.argv[1]
    #if not destdir():
    #    destdir = sys.argv[2]
    if os.path.isfile(pathname):
        #try:
        infile = os.path.abspath(pathname)
        filename, ext = os.path.splitext(infile)
        new_name = filename## zimages_name[:4]
        ext_dir = os.path.join(destdir, ext)
        new_filepath = os.path.join(ext_dir, new_name)
        #print infile, zimages_filepath

        ## Try to make 4 digit directory or pass if already present
        try:
            os.mkdir(ext_dir, 16877)
        except OSError:
            pass
        
        shutil.move(pathname,new_filepath)
        
        
import os, sys, re, shutil, glob
if __name__ == "__main__":
##if sys.argv[1]:
    try:
        rootdir = sys.argv[1]
    except:
        print "Sys Arg 1 must be the directory with files to organize"

    try:
        destdir = sys.argv[2]
    except:
        destdir = '/mnt/Production_Raw/.zImages_1'

    #filepaths = recursive_dirlist(rootdir)
    filepaths = glob.glob(os.path.abspath(os.path.join(rootdir, '*.*')))
    for pathname in filepaths:
        organize_files_by_4digit(pathname,destdir=destdir)
