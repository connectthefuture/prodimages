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


###
def subproc_magick_l_m_jpg(imgsrc, imgdestdir):
    import subprocess,os,re
    outsize_l = '400x480'
    outsize_m = '200x240'
    outsize_png = '2000x2400'
    
    colorstyle = str(imgsrc.split('/')[-1][:9])
    image_dest_l = os.path.join(imgdestdir, colorstyle + '_l.jpg')
    image_dest_m = os.path.join(imgdestdir, colorstyle + '_m.jpg')
    
    regex_primary_jpg = re.compile(r'.+?/[1-9][0-9]{8}\.jpg') 
    regex_alt_jpg = re.compile(r'.+?/[1-9][0-9]{8}_alt0[1-6]\.jpg')
    
    
    if re.findall(regex_primary_jpg, imgsrc):
        
        subprocess.call([
        "convert",
        "-format",
        "jpg",
        imgsrc,
        "-resize",
        outsize_l,
        "-adaptive-sharpen",
        "10",
        "-unsharp",
        "1.3x.8+80+0.1",
        "-quality",
        "100",
        image_dest_l,
        ])

    if re.findall(regex_alt_jpg, imgsrc):
        colorstyle_alt = str(imgsrc.split('/')[-1][:15])
        image_dest_m = os.path.join(imgdestdir, colorstyle_alt + '.jpg')

    subprocess.call([
    "convert",
    "-format",
    "jpg",
    imgsrc,
    "-resize",
    outsize_m,
    "-adaptive-sharpen",
    "5",
    "-unsharp",
    "55",
    "-quality",
    "100",
    image_dest_m,
    ])
    
    
def sub_proc_mogrify_png(tmp_dir):
    import subprocess,re,os
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    os.chdir(tmp_dir)
    subprocess.call([
                "mogrify",
                "-format",
                "png",
                '*.jpg',
#                imgsrc_jpg,
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
                "10",
                "-unsharp",
                "55",
#                imgdestpng_out,
                ])
    print "Done {}".format(tmp_dir)
    return

## Upload to imagedrop via FTP
def upload_to_imagedrop(file):
    import ftplib
    session = ftplib.FTP('file3.bluefly.corp', 'imagedrop', 'imagedrop0')
    fileread = open(file,'rb')
    filename = str(file.split('/')[-1])
    session.cwd("ImageDrop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit()    

########### RUN #################
# def convert_jpg_png(imgsrc_jpg,imgdest_png):
import os, sys, re, shutil, datetime, glob

try:
    rootdir = sys.argv[1]
except IndexError:
    rootdir = '/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly'

regex_CR2 = re.compile(r'.+?\.[CR2cr2]{3}')
regex_jpg = re.compile(r'.+?\.[JPGjpg]{3}')
regex_png = re.compile(r'.+?\.[pngPNG]{3}')
regex_coded = re.compile(r'.+?/[1-9][0-9]{8}_[1-6]\.jpg')
regex_primary_jpg = re.compile(r'.+?/[1-9][0-9]{8}\.jpg') 
regex_alt_jpg = re.compile(r'.+?/[1-9][0-9]{8}_alt0[1-6]\.jpg')
todaysdate = '{:%Y,%m,%d}'.format(datetime.datetime.now())
todaysdatefull = '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())
todaysdatearch = '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())

### Define tmp and archive paths prior to Creating
tmp_processing = os.path.join("/mnt/Post_Complete/Complete_to_Load/.tmp_processing" , "tmp_" + str(todaysdatefull).replace(",", ""))
tmp_loading = os.path.join("/mnt/Post_Complete/Complete_Archive/.tmp_loading" , "tmp_" + str(todaysdatefull).replace(",", ""))

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

###
## Begin Processing and compiling images for Loading
###

## move to tmp_processing from drop folders Then Mogrify to create pngs copy to load and arch dirs
walkedout_tmp = glob.glob(os.path.join(rootdir, '*/*.*g'))
[ shutil.move(file, os.path.join(tmp_processing, os.path.basename(file))) for file in walkedout_tmp ]

walkedout_tmp = glob.glob(os.path.join(tmp_processing, '*.*g'))
[ rename_retouched_file(file) for file in walkedout_tmp ]

##  make png frpm hirez jpg then move copy to losding and orig to archive
sub_proc_mogrify_png(tmp_processing)

tmp_png = glob.glob(os.path.join(tmp_processing, '*.png'))
[ shutil.copy2(file, os.path.join(tmp_loading, os.path.basename(file))) for file in tmp_png ]
[ shutil.move(file, os.path.join(imgdest_png_final, os.path.basename(file))) for file in tmp_png ]

###
## Create _l_m_alt from original jpgs
###
walkedout = glob.glob(os.path.join(tmp_processing, '*.jpg'))
for filepath in walkedout:
### Make _l and _m if not alt
    try:
        subproc_magick_l_m_jpg(filepath, tmp_loading)
        shutil.move(filepath, imgdest_jpg_final)
        print "Success large med plus move {}".format(filepath)
    except:
        print "Error largemed {}".format(filepath)
        pass

upload_tmp_loading = glob.glob(os.path.join(tmp_loading, '*.*g'))
for upload_file in upload_tmp_loading:
    #### TODO
    #### UPLOAD upload_file via ftp to imagedrop
    #upload_ftp_imagedrop(upload_file)
    ## Then rm loading tmp dir
    try:
        upload_to_imagedrop(upload_file)
        print "Uploaded {}".format(upload_file)
        shutil.move(upload_file, archive_uploaded)
    except:
        print "Error moving Finals to Arch {}".format(file)
        
## After completed Process and Load to imagedrop 
###  Finally Remove the 2 tmp folder trees for process and load if Empty
upload_tmp_loading_remainder = glob.glob(os.path.join(tmp_loading, '*.*g'))
if len(upload_tmp_loading_remainder) == 0:
    shutil.rmtree(tmp_loading)

upload_tmp_processing_remainder = glob.glob(os.path.join(tmp_processing, '*.*g'))
if len(upload_tmp_processing_remainder) == 0:
    shutil.rmtree(tmp_processing)