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
        ext = ".{}".format(ext.lower())
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
                #print type(filedir), type(colorstyle), type(alt), type(ext)
                #print filedir, colorstyle, alt, ext
                filename = "{}{}{}".format(colorstyle,alt,ext)
                renamed = os.path.join(filedir, filename)
                print renamed
        except OSError:
            print "OSError"
        #if re.findall(regex_renamed,renamed):
        try:
            print renamed
            os.rename(src_imgfilepath, renamed)
            if os.path.isfile(renamed):
                renamed_img_file = renamed
                return renamed_img_file
        except:
            print "findall rneamed"
            pass
        #else:
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
        "70",
        "-unsharp",
        "50",
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
    "60",
    "-unsharp",
    "40",
    "-quality",
    "100",
    image_dest_m,
    ])
    
    
def sub_proc_mogrify_png(tmp_dir_processing):
    import subprocess
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    subprocess.call(["cd", tmp_dir_processing])
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
                "50",
                "-unsharp",
                "75",
#                imgdestpng_out,
                ])
    return

########### RUN #################
# def convert_jpg_png(imgsrc_jpg,imgdest_png):
import os, sys, re, shutil, datetime, glob


regex_CR2 = re.compile(r'.+?\.[CR2cr2]{3}')
regex_jpg = re.compile(r'.+?\.[JPGjpg]{3}')
regex_png = re.compile(r'.+?\.[pngPNG]{3}')
regex_coded = re.compile(r'.+?/[1-9][0-9]{8}_[1-6]\.jpg')
regex_renamed = re.compile(r'.+?/[1-9][0-9]{8}_?0?[1-6]?\.jpg')
regex_primary_jpg = re.compile(r'.+?/[1-9][0-9]{8}\.jpg') 
regex_alt_jpg = re.compile(r'.+?/[1-9][0-9]{8}_alt0[1-6]\.jpg')
todaysdatefull = '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())
todaysdate = '{:%Y,%m,%d}'.format(datetime.datetime.now())

### Define tmp and archive paths prior to Creating
tmp_processing = os.path.join("/mnt/Post_Complete/Complete_to_Load/.tmp_processing" , "tmp_" + str(todaysdatefull).replace(",", ""))
tmp_loading = os.path.join("/mnt/Post_Complete/Complete_Archive/.tmp_loading" , "tmp_" + str(todaysdatefull).replace(",", ""))

archive = '/mnt/Post_Complete/Complete_Archive/Uploaded'
archive_uploaded = os.path.join(archive, "uploaded_" + str(todaysdate).replace(",", ""))

imgdest_jpg_final = os.path.join(archive_uploaded, 'JPG_RETOUCHED_ORIG')
imgdest_png_final = os.path.join(archive_uploaded, 'PNG')

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


##get all the processed files and move to tmp proccessing dir
#walkedout_tmp = recursive_dirlist(rootdir)
#for file in walkedout_tmp:
#    regex_jpg = re.compile(r'.+?\.[JPGjpg]{3}')
#    #regex_png = re.compile(r'.+?\.[pngPNG]{3}')
#    if re.findall(regex_jpg,file):
#        print "findall"
#        try:
#            shutil.move(file, tmp_processing)
#            print "success {}".format(file)
#        except:
#            print "Error {}".format(file)


            
# walkedout = recursive_dirlist(tmp_processing)

## move to tmp_processing from drop folders Then Mogrify to create pngs copy to load and arch dirs
walkedout_tmp = glob.glob(rootdir, '*/*.*g')
[ shutil.move(file, tmp_processing) for file in walkedout_tmp ]

walkedout_tmp = glob.glob(tmp_processing, '*.*g')
[ rename_retouched_file(file) for file in walkedout_tmp ]


sub_proc_mogrify_png(tmp_processing)

tmp_png = glob.glob(tmp_processing, '*.png')
[ shutil.copy2(file, tmp_loading) for file in tmp_png ]
[ shutil.move(file, archive_uploaded) for file in tmp_png ]


walkedout = glob.glob(tmp_processing, '*.*g')
for filepath in walkedout:
    #try:
#    imgsrc_jpg = rename_retouched_file(filepath)
    print imgsrc_jpg
    
    imgsrc_png_name = str(filepath.split('/')[-1])
    print imgsrc_png
##    ###
    imgsrc_png = imgsrc_png.replace('.jpg','.png').split('/')[-1]
    print imgsrc_png


    img_jpg_final = os.path.join(imgdest_jpg_final, imgsrc_jpg)
    #imgsrc_png = os.path.join(tmp_processing, imgsrc_png_name)
 
    ## Move files to archive then make copies and send to load
#    shutil.move(imgsrc_jpg, imgdest_jpg_final)
#    print "move imgsrc"
#    shutil.move(imgsrc_png, imgdest_png_final)
#    print "moved png to final"
#    shutil.copy2(imgdest_png_final, tmp_loading)
#    print "copied png to upload"
    
    ### Make _l and _m if not alt
    if re.findall(regex_renamed, img_jpg_final):
        subproc_magick_l_m_jpg(img_jpg_final, tmp_loading)

    #except:
    #    print "Error {}".format(filepath)
