#!/usr/bin/env python

## Walk Root Directory and Return List or all Files in all Subdirs too
def recursive_dirlist(rootdir):
    import os
    regex_CR2 = re.compile(r'.+?\.[CR2cr2]{3}')
    regex_jpg = re.compile(r'.+?\.[JPGjpg]{3}')
    regex_png = re.compile(r'.+?\.[pngPNG]{3}')
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


def rename_retouched_file(src_imgfilepath):
    import os,re
    regex_coded = re.compile(r'.+?/[1-9][0-9]{8}_[1-6]\.jpg')
    imgfilepath = src_imgfilepath
    if re.findall(regex_coded,imgfilepath):
        filedir = imgfilepath.split('/')[:-1]
        filedir = '/'.join(filedir)
        print filedir
        filename = imgfilepath.split('/')[-1]
        colorstyle = str(filename[:9])
        testimg = filename.split('_')[-1]
        alttest = testimg.split('.')[0]
        ext = filename.split('.')[-1]
        ext = ".{}".format(ext.lower())
        # if its 1
        if str.isdigit(alttest) & len(alttest) == 1:
            if alttest == '1':
                src_img_primary = src_imgfilepath.replace('_1.','.')
                os.rename(src_imgfilepath, src_img_primary)
                return src_img_primary
            else:
                alttest = int(alttest)
                print alttest
                alttest = alttest - 1
                alt = '_alt0{}'.format(str(alttest))
                print alt

                if alt:
                        #print type(filedir), type(colorstyle), type(alt), type(ext)
                        #print filedir, colorstyle, alt, ext
                    filename = "{}{}{}".format(colorstyle,alt,ext)
                    renamed = os.path.join(filedir, filename)
                    print renamed
        ##        except UnboundLocalError:
        ##            print "UnboundLocalError{}".format(imgfilepath)
                if renamed:
                    os.rename(src_imgfilepath, renamed)
                    if os.path.isfile(renamed):
                        return renamed
        else:
            return src_imgfilepath


def get_exif_metadata_value(image_filepath, exiftag=None):
    from PIL import Image
    import pyexiv2
    # Read EXIF data to initialize
    image_metadata = pyexiv2.ImageMetadata(image_filepath)
    metadata = image_metadata.read()
    # Add and Write new Tag to File
    if exiftag:
        exifvalue = metadata[exiftag]
        return (exiftag, exifvalue)
    # image_metadata[exiftag] = exifvalue
    # image_metadata.write()
    else:
        metadict = {}
        for mtag, mvalue in metadata.iteritems():
            metadict[mtag] = mvalue
        return metadict


######## Make Images For Upload to Website ##########

### Large Jpeg Mogrfy Dir with _l jpgs
def subproc_magick_large_jpg(imgdir):
    import subprocess,os,re

    ### Change to Large jpg dir to Mogrify using Glob
    os.chdir(imgdir)
    
    subprocess.call([
    "mogrify",
    '*.jpg[400x480]',
    "-filter",
    "Mitchell",
    "-compress",
    "none",
    "-format",
    "jpeg",
    "-adaptive-sharpen",
    "100",
    "-unsharp",
    "50",
    "-quality",
    "100",
    ])

### Medium Jpeg Mogrfy Dir with _m jpgs
def subproc_magick_medium_jpg(imgdir):
    import subprocess,os,re

    ### Change to Medium jpg dir to Mogrify using Glob
    os.chdir(imgdir)
    
    subprocess.call([
    "mogrify",
    '*.jpg[200x240]',
    "-filter",
    "Mitchell",
    "-compress",
    "none",
    "-format",
    "jpeg",
    "-adaptive-sharpen",
    "100",
    "-unsharp",
    "50",
    "-quality",
    "100",
    ])


### Png Create with Mogrify globbing png directories
def subproc_magick_png(imgdir):
    import subprocess,re,os
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    os.chdir(imgdir)
    
    subprocess.call([
    "mogrify",
    "-format",
    "png",
    '*.jpg',
    "-define",
    "png:preserve-colormap",
    "-define",
    "png:format=png24",
    "-define",
    "png:compression-level=N",
    "-define",
    "png:compression-strategy=N",
    "-define",
    "png:compression-filter=N",
    "-format",
    "png",
    "-quality",
    "100",
    "-adaptive-sharpen",
    "50",
    "-unsharp",
    "75",
    ])
    
    print "Done {}".format(imgdir)
    return

##### Upload tmp_loading dir to imagedrop via FTP using Pycurl  #####
def pycurl_upload_imagedrop(localFilePath):
    import pycurl, os
    #import FileReader
    localFileName = localFilePath.split('/')[-1]

    mediaType = "8"
    ftpURL = "ftp://file3.bluefly.corp/ImageDrop/"
    ftpFilePath = os.path.join(ftpURL, localFileName)
    ftpUSERPWD = "imagedrop:imagedrop0"

    if localFilePath != "" and ftpFilePath != "":
        ## Create send data

        ### Send the request to Edgecast
        c = pycurl.Curl()
        c.setopt(pycurl.URL, ftpFilePath)
#        c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
#        c.setopt(pycurl.FORBID_REUSE, 1)
#        c.setopt(pycurl.FRESH_CONNECT, 1)
        f = open(localFilePath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
#        c.setopt(pycurl.READFUNCTION, f.read());        
#        c.setopt(pycurl.READDATA, f.read()); 
        c.setopt(pycurl.UPLOAD, 1L)

        try:
            c.perform()
            c.close()
            print "Successfully Uploaded --> {0}".format(localFileName)
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


########### RUN #################
# def convert_jpg_png(imgsrc_jpg,imgdest_png):
import os, sys, re, shutil, datetime, glob

### Can pass as sys.argv a direcectory with nested directories containing jpgs. Must have nested dirs
try:
    testdir = sys.argv[1]
    if os.path.isdir(testdir):
       rootdir = testdir
    else:
        rootdir = '/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly'
except IndexError:
    rootdir = '/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly'


### Regex Pattern Defs
regex_CR2 = re.compile(r'.+?\.[CR2cr2]{3}')
regex_jpg = re.compile(r'.+?\.[JPGjpg]{3}')
regex_png = re.compile(r'.+?\.[pngPNG]{3}')
regex_coded = re.compile(r'.+?/[1-9][0-9]{8}_[1-6]\.jpg')
regex_primary_jpg = re.compile(r'.+?/[1-9][0-9]{8}\.jpg')
regex_alt_jpg = re.compile(r'.+?/[1-9][0-9]{8}_alt0[1-6]\.jpg')

### Date Defs
todaysdate = '{:%Y,%m,%d}'.format(datetime.datetime.now())
todaysdatefull = '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())
todaysdatearch = '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())

### Define tmp and archive paths prior to Creating
tmp_processing = os.path.join("/mnt/Post_Complete/Complete_to_Load/.tmp_processing" , "tmp_" + str(todaysdatefull).replace(",", ""))
tmp_processing_l = os.path.join(tmp_processing, "largejpg")
tmp_processing_m = os.path.join(tmp_processing, "mediumjpg")
tmp_loading = os.path.join("/mnt/Post_Complete/Complete_Archive/.tmp_loading" , "tmp_" + str(todaysdatefull).replace(",", ""))

## Define for Creating Archive dirs
archive = '/mnt/Post_Complete/Complete_Archive/Uploaded'
archive_uploaded = os.path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""), "uploaded_" + str(todaysdatearch).replace(",", ""))

imgdest_jpg_final = os.path.join(archive_uploaded, 'JPG_RETOUCHED_ORIG')
imgdest_png_final = os.path.join(archive_uploaded, 'PNG')

## Test for existing files to load or kill entire process prior to dir creation
walkedout_tmp = glob.glob(os.path.join(rootdir, '*/*.*g'))
if len(walkedout_tmp) == 0:
    print "Nothing to Process"
else:
### Make Tmp Folders for Processing And Uploading -- tmp_dirs are dated with time(hr:min)to prevent collisions
    try:
        os.makedirs(archive_uploaded, 16877)
    except:
        pass

    try:
        os.makedirs(tmp_processing, 16877)
    except:
        pass

    try:
        os.makedirs(tmp_processing_l, 16877)
    except:
        pass

    try:
        os.makedirs(tmp_processing_m, 16877)
    except:
        pass

    try:
        os.makedirs(tmp_loading, 16877)
    except:
        pass

    try:
        os.makedirs(imgdest_png_final, 16877)
    except:
        pass

    try:
        os.makedirs(imgdest_jpg_final, 16877)
    except:
        pass

####################################################
## Begin Processing and compiling images for Loading
####################################################


## Move All DropFinal Files from Retouchers dirs to tmp_processing from drop folders Then Mogrify to create pngs copy to load and arch dirs
walkedout_tmp = glob.glob(os.path.join(rootdir, '*/*.*g'))
[ shutil.move(file, os.path.join(tmp_processing, os.path.basename(file))) for file in walkedout_tmp ]

### Rename Files moved into Temp Processing Floder
walkedout_tmp = glob.glob(os.path.join(tmp_processing, '*.jpg'))
[ rename_retouched_file(file) for file in walkedout_tmp ]


## Copy Full Size Retouched Jpg to tmp Large and Med jpg folders for Glob Mogrify AND to Final Archive JPG_RETOUCHED_ORIG
walkedout_renamed = glob.glob(os.path.join(tmp_processing, '*.jpg'))


## Large
[ shutil.copy2(file, os.path.join(tmp_processing_l, os.path.basename(file))) for file in walkedout_renamed ]
walkedout_large = glob.glob(os.path.join(tmp_processing_l, '*.jpg'))
### Remove alt images and rename as _l
for f in walkedout_large:
    if re.findall(regex_alt_jpg, f):
        os.remove(f)
    elif re.findall(regex_primary_jpg, f):
        f_large = f.replace('.jpg', '_l.jpg')
        os.rename(f, f_large)

## Mofrify directory of only primary renamed _l Files  to 400x480
subproc_magick_large_jpg(tmp_processing_l)


## Medium
[ shutil.copy2(file, os.path.join(tmp_processing_m, os.path.basename(file))) for file in walkedout_renamed ]
walkedout_medium = glob.glob(os.path.join(tmp_processing_m, '*.jpg'))
### Bypass rename alt images and rename only primary jpgs as _m
for f in walkedout_medium:
    if re.findall(regex_primary_jpg, f):
        f_medium = f.replace('.jpg', '_m.jpg')
        os.rename(f, f_medium)

## Mofrify directory of renamed _m Files and unrenamed alts to 200x240
subproc_magick_medium_jpg(tmp_processing_m)

####
#### JPEGS Have Been CREATED in Each of the tmp_processing folders named _l + _m
####

## PNG
##### PNG CREATE FROM RETOUCHED JPGS ## All files in Root of tmp_processing will be mogrified to PNGs leaving JPG to Arch
##  make png frpm hirez jpg then move copy to losding and orig to archive
subproc_magick_png(tmp_processing)

### Glob created PNGs and copy to Load Dir then Store in Arch dir 
tmp_png = glob.glob(os.path.join(tmp_processing, '*.png'))
[ shutil.copy2(file, os.path.join(tmp_loading, os.path.basename(file))) for file in tmp_png ]
[ shutil.move(file, os.path.join(imgdest_png_final, os.path.basename(file))) for file in tmp_png ]

## ARCHIVED Backup
## All JPGs in Root dir Only of tmp_processing will be now Archived as all Conversions are completed
jpgs_to_archive = glob.glob(os.path.join(tmp_processing, '*.jpg'))
[ shutil.move(file, os.path.join(imgdest_jpg_final, os.path.basename(file))) for file in jpgs_to_archive ]


###### All PNGs Created and moved to Archive plus Copy sent to Load Directory
###
######
#### All Files Converted for Upload, Now glob search and move large and medium named jpgs to tmp loading
###
load_jpgs = glob.glob(os.path.join(tmp_processing, '*/*.jpg'))
[ shutil.move(file, os.path.join(tmp_loading, os.path.basename(file))) for file in load_jpgs ]

## UPLOAD FTP with PyCurl everything in tmp_loading
###
import time
upload_tmp_loading = glob.glob(os.path.join(tmp_loading, '*.*g'))
for upload_file in upload_tmp_loading:
    #### UPLOAD upload_file via ftp to imagedrop using Pycurl
    ## Then rm loading tmp dir
    try:
        code = pycurl_upload_imagedrop(upload_file)
        if code:
            print code, upload_file
            time.sleep(float(.8))
        else:
            print "Uploaded {}".format(upload_file)
            time.sleep(float(.1))
            shutil.move(upload_file, archive_uploaded)
    except:
        print "Error moving Finals to Arch {}".format(file)
        

## After completed Process and Load to imagedrop
###  Finally Remove the 2 tmp folder trees for process and load if Empty
upload_tmp_loading_remainder = glob.glob(os.path.join(tmp_loading, '*.*g'))
if len(upload_tmp_loading_remainder) == 0:
    shutil.rmtree(tmp_loading)

upload_tmp_processing_png_remainder = glob.glob(os.path.join(tmp_processing, '*.*g'))
upload_tmp_processing_jpg_remainder = glob.glob(os.path.join(tmp_processing, '*/*.*g'))
if len(upload_tmp_processing_png_remainder) == 0 and len(upload_tmp_processing_jpg_remainder) == 0:
    shutil.rmtree(tmp_processing)
