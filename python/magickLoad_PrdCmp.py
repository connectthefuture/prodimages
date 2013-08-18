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
    regex_renamed= re.compile(r'.+?/[1-9][0-9]{8}_?0?[1-6]?\.jpg')
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
        ext = '.' + ext.lower()
        # if its 1
        if str.isdigit(alttest) & len(alttest) == 1:
            if alttest == 1:
                alt = ''
            else:
                alttest = int(alttest)
                alttest = alttest + 1
                alt = '_alt0{}'.format(str(alttest))
        try:
            if alt:
                print type(filedir), type(colorstyle), type(alt), type(ext)
                print filedir, colorstyle, alt, ext
                renamed = os.path.join(filedir, colorstyle, alt + ext)
                print renamed
        except OSError:
            print "OSError"
        if re.findall(regex_renamed,renamed):
            try:
                print renamed
                os.rename(src_imgfilepath, renamed)
                if os.path.isfile(renamed):
                    renamed_img_file = renamed
                    return renamed_img_file
            except:
                print "findall rneamed"
                pass
        else:
            try:
                os.rename(src_imgfilepath,imgfilepath)
                if os.path.isfile(renamed):
                    return imgfilepath
            except:
                print "finad renameSSSS"
                pass
    else:
        try:
            os.rename(src_imgfilepath,imgfilepath)
        except:
            print "Error{}".format(src_imgfilepath)
        return imgfilepath
        
        
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
def subproc_magick_l_m_jpg(imgsrc, imgdest):
    import subprocess,os
    outsize_l = '400x480'
    outsize_m = '200x240'
    outsize_png = '2000x2400'
    outsize = outsize
    image_dest_l = imgdest.replace('.jpg', '_l.jpg')
    image_dest_m = imgdest.replace('.jpg', '_m.jpg')

    subprocess.call([
    "convert",
    imgsrc,
    "-colorspace",
    "rgb",
    "-compress",
    "none",
    "-format",
    "jpeg",
    "-colorspace",
    "srgb",
    "-resample",
    outsize_l,
    "-adaptive-sharpen",
    70,
    "-unsharp",
    50,
    "-quality",
    100,
    image_dest_l
    ])

    subprocess.call([
    "convert",
    imgsrc,
    "-colorspace",
    "rgb",
    "-compress",
    "none",
    "-format",
    "jpeg",
    "-colorspace",
    "srgb",
    "-resample",
    outsize_m,
    "-adaptive-sharpen",
    60,
    "-unsharp",
    40,
    "-quality",
    100,
    image_dest_m
    ])

def sub_proc_convert_png(imgsrc_jpg,imgdest_png, tmp_processing):
    import subprocess
    imgdestpng = os.path.join(tmp_processing, os.path.basename(imgdestpng))
    subprocess.call([
                "convert",
                "-format",
                "png",
                imgsrc_jpg,
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
                "-quality",
                100,
                "-adaptive-sharpen",
                50,
                "-unsharp",
                75,
                imgdest_png
                ])
    return


# def convert_jpg_png(imgsrc_jpg,imgdest_png):
import os, sys, re, shutil, datetime

try:
    rootdir = sys.argv[1]
except:
    rootdir = '/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly'

regex_CR2 = re.compile(r'.+?\.[CR2cr2]{3}')
regex_jpg = re.compile(r'.+?\.[JPGjpg]{3}')
regex_png = re.compile(r'.+?\.[pngPNG]{3}')
regex_coded = re.compile(r'.+?/[1-9][0-9]{8}_[1-6]\.jpg')
regex_renamed= re.compile(r'.+?/[1-9][0-9]{8}_?0?[1-6]?\.jpg')
todaysdatefull = '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())
todaysdate = '{:%Y,%m,%d}'.format(datetime.datetime.now())


tmp_processing = os.path.join("/mnt/Post_Complete/Complete_to_Load/.tmp_processing" , "tmp_" + str(todaysdatefull).replace(",", ""))
tmp_loading = os.path.join("/mnt/Post_Complete/Complete_Archive/.tmp_loading" , "tmp_" + str(todaysdatefull).replace(",", ""))

archive = '/mnt/Post_Complete/Complete_Archive/Uploaded'
archive_uploaded = os.path.join(archive , "uploaded_" + str(todaysdate))

imgdest_jpg_final = os.path.join(archive_uploaded, str(todaysdate).replace(",", ""), 'JPG_RETOUCHED_ORIG')
imgdest_png_final = os.path.join(archive_uploaded, str(todaysdate).replace(",", ""), 'PNG')

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
##get all the processed files
walkedout_tmp = recursive_dirlist(rootdir)
for file in walkedout_tmp:
    regex_jpg = re.compile(r'.+?\.[JPGjpg]{3}')
    #regex_png = re.compile(r'.+?\.[pngPNG]{3}')
    if re.findall(regex_jpg,file):
        print "findall"
        try:
            shutil.move(file, tmp_processing)
            print "success {}".format(file)
        except:
            print "Error {}".format(file)
            
walkedout = recursive_dirlist(tmp_processing)

for filepath in walkedout:
    try:
        imgsrc_jpg = rename_retouched_file(filepath)
        imgsrc_png = imgsrc_jpg.split('/')[-1]
        imgsrc_png = imgsrc_png.replace('.jpg','.png')
        sub_proc_convert_png(imgsrc_jpg, imgsrc_png, tmp_processing)
        img_jpg_final = os.path.join(imgdest_jpg_final, imgsrc_jpg)
        img_png_path = os.path.join(tmp_processing, imgsrc_png)
        shutil.move(imgsrc_jpg, imgdest_jpg_final)
        shutil.move(img_png_path, imgdest_png_final)
        shutil.copy2(imgdest_png_final, tmp_loading)
        subproc_magick_l_m_jpg(imgdest_jpg_final, os.path.join(tmp_loading, imgsrc_jpg.split('/')[-1]))
    except:
        print "Error {}".format(filepath)
