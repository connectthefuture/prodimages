###
## Walk Root Directory and Return List or all Files in all Subdirs too
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


def make_createdirs_and_move_zimages_lowres_thumbnails_dir_or_singlefile(pathname):
    import os, sys, re, csv
    from PIL import Image
    import pyexiv2
    import glob, os, re
    size = 600, 720
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
    zimages_root = '/Users/JCut/Public/Production_Raw/zImages_1'
#    test_zimages = '/'.join(pathname.split('/')[:4])
#    if test_zimages == zimages_root:
#        pass
#    elif re.findall(regex_jpeg, pathname):
#        zimages_root = '/mnt/Post_Ready/zImages_1'
    ## If input variable is a single File Create 1 Thumb
    if os.path.isfile(pathname):
        #try:
        infile = os.path.abspath(pathname)
        filename, ext = os.path.splitext(infile)
        zimages_name = os.path.split(infile)[-1]
        zimages_dir = zimages_name[:4]
        zimages_dir = os.path.join(zimages_root, zimages_dir)
        zimages_filepath = os.path.join(zimages_dir, zimages_name)
        #print infile, zimages_filepath

        ## Try to make 4 digit directory or pass if already present
        try:
            os.mkdir(zimages_dir, 16877)
        except OSError:
            pass

        ## Test if this file has already been copied to Zimages Dir -- If not Make 600x720 jpg in zimagesdir
        if os.path.isfile(zimages_filepath):
            print "File Exists: {0}".format(zimages_filepath)
            pass
        else:
            try:

            ## Extract Originals Metadata prior to Resizing
                source_metadata = pyexiv2.ImageMetadata(infile)
                source_metadata.read()
            # Resize and Save Thumb copy to Zimages
                im = Image.open(infile)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(zimages_filepath , "JPEG")
                print infile, zimages_filepath
            # Copy EXIF data from Source to Resized Image
                dest_metadata = pyexiv2.ImageMetadata(zimages_filepath)
                dest_metadata.read()
                source_metadata.copy(dest_metadata, exif=True, iptc=True, xmp=True, comment=True)
            # set EXIF image size info to resized size
            #    dest_metadata.read()
            #    dest_metadata["Exif.Photo.PixelXDimension"] = im.size[0]
            #    dest_metadata["Exif.Photo.PixelYDimension"] = im.size[1]
                dest_metadata.write()
            except IOError:
                print "Bad Image File {}".format(zimages_filepath)
                pass
        return zimages_filepath

        #except:
             #   print "Error Creating Single File Thumbnail for {0}".format(infile)
        ## If input variable is a Directory Decend into Dir and Crate Thumnails for all jpgs
    elif os.path.isdir(pathname):
        dirname = os.path.abspath(pathname)
        print dirname
        for infile in glob.glob(os.path.join(dirname, "*.jpg")):
            try:
                infile = os.path.abspath(infile)
                filename, ext = os.path.splitext(infile)
                zimages_name = os.path.split(infile)[-1]
                zimages_dir = zimages_name[:4]
                zimages_dir = os.path.join(zimages_root, zimages_dir)
                zimages_filepath = os.path.join(zimages_dir, zimages_name)
                print infile, zimages_filepath

                ## Try to make 4 digit directory or pass if already present
                try:
                    os.mkdir(zimages_dir, 16877)
                except OSError:
                    pass

                ## Test if this file has already been copied to Zimages Dir -- If not Make 600x720 jpg in zimagesdir
                if os.path.isfile(zimages_filepath):
                    pass
                    print "File Exists: {0}".format(zimages_filepath)
                else:
                    ## Extract Originals Metadata prior to Resizing
                        source_metadata = pyexiv2.ImageMetadata(infile)
                        source_metadata.read()
                    # Resize and Save Thumb copy to Zimages
                        im = Image.open(infile)
                        im.thumbnail(size, Image.ANTIALIAS)
                        im.save(zimages_filepath , "JPEG")
                        print infile, zimages_filepath
                    # Copy EXIF data from Source to Resized Image
                        dest_metadata = pyexiv2.ImageMetadata(zimages_filepath)
                        dest_metadata.read()
                        source_metadata.copy(dest_metadata, exif=True, iptc=True, xmp=True, comment=True)
                    # set EXIF image size info to resized size
                    #    dest_metadata.read()
                    #    dest_metadata["Exif.Photo.PixelXDimension"] = im.size[0]
                    #    dest_metadata["Exif.Photo.PixelYDimension"] = im.size[1]
                        dest_metadata.write()
                return zimages_filepath
            except:
                print "Error Creating Thumbnail for {0}".format(infile)
                
                
def organize_files_by_4digit(pathname,destdir=None):
    import os, sys, re, shutil
    regex_jpeg = re.compile(r'.+?\.[jpgJPG]{3}$')
#    pathname = sys.arg[1]
#    if not destdir():
#        destdir = sys.argv[2]
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
        