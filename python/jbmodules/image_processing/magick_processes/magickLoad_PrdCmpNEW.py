#/usr/bin/env python

def get_aspect_ratio(img):
    from PIL import Image
    im = Image.open(img)
    w,h = im.size
    aspect_ratio = str(round(float(int(h))/float(int(w)),2))
    return aspect_ratio

def get_dimensions(img):
    from PIL import Image
    im = Image.open(img)
    w,h = im.size
    dimensions = "{0}x{1}".format(int(w),int(h))
    return dimensions


def get_exif_metadata_value(image_filepath, exiftag=None):
    #from PIL import Image
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


##### ##### ##### ########## ##### ##### #####
##### ##### ##### ########## ##### ##### #####

def get_image_color_minmax(img):
    import subprocess, os, sys, re
    ret = subprocess.check_output([
    'convert',
    img,
    '-median',
    '5',
    '+dither',
    '-colors',
    '2',
    '-trim',
    '+repage',
    '-gravity',
    'center',
    '-crop',
    '50%',
    '-depth',
    '8',
    '-format',
    '%c',
    'histogram:info:-'])

    ## Prepare cleaned output as list or dict
    colormax = str(ret).split('\n')[0].strip(' ')
    colormax =  re.sub(re.compile(r',\W'),',',colormax).replace(':','',1).split(' ')
    colormin = str(ret).split('\n')[1].strip(' ')
    colormin =  re.sub(re.compile(r',\W'),',',colormin).replace(':','',1).split(' ')

    fields_top =  ['min_thresh', 'max_thresh']
    fields_l2  =  ['mean_avg', 'rgb_vals', 'webcolor_id', 'color_profile_vals']
    # x = { zip(field.split(','),color.split(',')) for color in colormin }
    colormin  = zip(fields_l2,colormin)
    colormax  = zip(fields_l2,colormax)

    coloravgs = colormin,colormax
    colordata = zip(fields_top, coloravgs)

    return colordata

# Return Image data dict
def metadata_info_dict(img):
    import os,sys,re,subprocess,glob
    regex_geometry = re.compile(r'^Geometry.+?$')
    metadict = {}
    fileinfo = {}
    fname=os.path.basename(img)
    dname=os.path.dirname(img)
    regex_geometry_attb = re.compile(r'.*?Geometry.*?[0-9,{1,4}]x[0-9,{1,4}].*?$')

    metadata=subprocess.check_output(['identify', '-verbose', img])

    metadata_list = metadata.replace(' ','').split('\n')

    g_width = [ g.split(':')[-1].split('+')[0].split('x')[0] for g in metadata_list if regex_geometry.findall(g) ]
    g_height = [ g.split(':')[-1].split('+')[0].split('x')[1] for g in metadata_list if regex_geometry.findall(g) ]

    metadata_width    = float(g_width[0])
    metadata_height   = float(g_height[0])

    aspect_ratio =  metadata_height/metadata_width
    aspect_ratio = "{0:.2f}".format(round(aspect_ratio,2))

    fileinfo['width'] = "{0:.0f}".format(round(metadata_width,2))
    fileinfo['height'] = "{0:.0f}".format(round(metadata_height,2))
    fileinfo['aspect'] = aspect_ratio
    orientation        = 'standard'

    if float(round(metadata_height/metadata_width,2)) == float(round(1.00,2)):
        orientation    = 'square'
    elif float(round(metadata_height/metadata_width,2)) > float(round(1.00,2)):
        orientation    = 'portait'
    elif float(round(metadata_height/metadata_width,2)) < float(round(1.00,2)):
        orientation    = 'landscape'

    if float(round(metadata_height/metadata_width,2)) == float(1.2):
        orientation    = 'standard'
        if g_width[0] == '2000' and g_height[0] == '2400':
            orientation = 'bfly'
    if float(round(metadata_height/metadata_width,2)) == float(1.25):
        orientation    = 'bnc'

    fileinfo['orientation'] = orientation
    fileinfo['mean'] = mean_tot[0]
    fileinfo['colorspace'] = colorspace[0]
    metadict[img] = fileinfo
    return metadict

def rename_retouched_file(img):
    import os,re
    regex_coded = re.compile(r'.+?/[1-9][0-9]{8}_[1-6]\.jpg')
    imgfilepath = img
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
                src_img_primary = img.replace('_1.','.')
                os.rename(img, src_img_primary)
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
                    ##except UnboundLocalError:
                    ##print "UnboundLocalError{}".format(imgfilepath)
                if renamed:
                    os.rename(img, renamed)
                    if os.path.isfile(renamed):
                        return renamed
        else:
            return img

# return image demensions and vert_hoiz variables only
def get_imagesize_variables(img):
    import os,sys,re,subprocess,glob
    dimensions = ''
    regex_geometry = re.compile(r'^Geometry.+?$')
    regex_geometry_attb = re.compile(r'.*?Geometry.*?[0-9,{1,4}]x[0-9,{1,4}].*?$')

    metadata=subprocess.check_output(['identify','-verbose', img])

    metadata_list = metadata.replace(' ','').split('\n')

    g_width = [ g.split(':')[-1].split('+')[0].split('x')[0] for g in metadata_list if regex_geometry.findall(g) ]
    g_height = [ g.split(':')[-1].split('+')[0].split('x')[1] for g in metadata_list if regex_geometry.findall(g) ]

    dimensions = '{0}x{1}'.format(g_width[0],g_height[0])

    ## Vertical Portrait orientation or exact Square for taller images
    xdelim = 'x'
    if int(dimensions.split(xdelim)[1]) <= int(dimensions.split(xdelim)[-1]):
        if int(dimensions.split(xdelim)[1]) > 2000:
            vert_horiz = "x2400"
            dimensions = "2000x2400"
        elif int(dimensions.split(xdelim)[1]) < 2000 and int(dimensions.split(xdelim)[1]) > 1400:
            vert_horiz = "x1680"
            dimensions = "1400x1680"
        elif int(dimensions.split(xdelim)[1]) < 1400 and int(dimensions.split(xdelim)[1]) > 1000:
            vert_horiz = "x1200"
            dimensions = "1000x1200"
        elif int(dimensions.split(xdelim)[1]) < 1000 and int(dimensions.split(xdelim)[1]) > 600:
            vert_horiz = "x720"
            dimensions = "600x720"
        else:
            vert_horiz = "x480"
            dimensions = "400x480"

    ## Landscape Orientation for wider images
    elif int(dimensions.split(xdelim)[1]) > int(dimensions.split(xdelim)[-1]):
        if int(dimensions.split(xdelim)[-1]) > 2400:
            vert_horiz = "2000x"
            dimensions = "2000x2400"

        elif int(dimensions.split(xdelim)[-1]) < 2400 and int(dimensions.split(xdelim)[-1]) > 1680:
            vert_horiz = "1400x"
            dimensions = "1400x1680"

        elif int(dimensions.split(xdelim)[-1]) < 1680 and int(dimensions.split(xdelim)[-1]) > 1200:
            vert_horiz = "1000x"
            dimensions = "1000x1200"

        elif int(dimensions.split(xdelim)[-1]) < 1200 and int(dimensions.split(xdelim)[-1]) > 720:
            vert_horiz = "600x"
            dimensions = "600x720"
        else:
            vert_horiz = "400x"
            dimensions = "400x480"
    print vert_horiz, dimensions
    return vert_horiz, dimensions

#
### End Data extract Funx, below processors
#

### Large Jpeg Convert to  _l jpgs
def subproc_magick_large_jpg(img, destdir=None):
    import subprocess,os,re
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    os.chdir(os.path.dirname(img))

    ## Destination name if Alt or Not
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    if not regex_alt.findall(img):
        outfile = os.path.join(destdir, img.split('/')[-1][:9] + '_l.jpg')

        dimensions = ''
        ## Get variable values for processing
        aspect_ratio = get_aspect_ratio(img)
        dimensions = get_dimensions(img)
        width  = dimensions.split('x')[0]
        height = dimensions.split('x')[1]

        if aspect_ratio == '1.2':
            vert_horiz = '400x480'
        elif float(aspect_ratio) > float(1.2):
            vert_horiz = 'x480'
        elif float(aspect_ratio) < float(1.2):
            vert_horiz = '400x'

        dimensions = "400x480"
        print dimensions,vert_horiz
        if regex_valid_style.findall(img):
            subprocess.call([
            'convert',
            '-colorspace',
            'RGB',
            img,
            '-crop',
            str(
            subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
            ,
            # CENTERING & Trim
            '-background',
            'white',
            #'-gravity',
            #'center',
            #'-trim',
            #'+repage',
            "-filter",
            "Spline",
            "-filter",
            #"Catrom",
            "Cosine",
            "-define",
            #"filter:blur=0.88549061701764", # SHARPER
            "filter:blur=0.9891028367558475",
            "-distort",
            "Resize",
            vert_horiz,
            '-extent',
            dimensions,
            "-colorspace",
            "sRGB",
            "-format",
            "jpeg",
            '-unsharp',
            '2x1.24+0.5+0',
            '-quality',
            '95',
            outfile
            ])
            return outfile
        else:
            return img
    ## No alt _L size needed
    else:
        pass

#
###
### Medium Jpeg Convert to  _m jpgs
def subproc_magick_medium_jpg(img, destdir=None):
    import subprocess,os,re
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    os.chdir(os.path.dirname(img))
    #rgbmean = get_image_color_minmax(img)

    ## Destination name if Alt or Not
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    if regex_alt.findall(img):
        outfile = os.path.join(destdir, img.split('/')[-1])
    else:
        outfile = os.path.join(destdir, img.split('/')[-1][:9] + '_m.jpg')

    dimensions = ''
    ## Get variable values for processing
    aspect_ratio = get_aspect_ratio(img)
    dimensions = get_dimensions(img)
    width  = dimensions.split('x')[0]
    height = dimensions.split('x')[1]

    if aspect_ratio == '1.2':
        vert_horiz = '200x240'
    elif float(aspect_ratio) > float(1.2):
        vert_horiz = 'x240'
    elif float(aspect_ratio) < float(1.2):
        vert_horiz = '200x'

    dimensions = '200x240'
    print dimensions,vert_horiz
    if regex_valid_style.findall(img):

        subprocess.call([
            'convert',
            '-colorspace',
            'RGB',
            img,
            '-crop',
            str(
            subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
            ,
            # CENTERING & Trim
            '-background',
            'white',
            #'-gravity',
            #'center',
            #'-trim',
            #'+repage',
            #"-filter",
            #"Mitchell",
            "-filter",
            "Spline",
            #"-filter",
            #"Catrom",
            "-filter",
            "Cosine",
            "-define",
            #"filter:blur=0.88549061701764", # SHARPER
            "fliter:blur=0.9891028367558475",
            "-distort",
            "Resize",
            vert_horiz,
            '-extent',
            dimensions,
            "-colorspace",
            "sRGB",
            "-format",
            "jpeg",
            '-unsharp',
            '2x1.1+0.5+0',
            '-quality',
            '95',
            #os.path.join(destdir, img.split('/')[-1])
            outfile
            ])
        return outfile
    else:
        return img

### Png Create with Convert and aspect
def subproc_magick_png(img, destdir=None):
    import subprocess,re,os
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    os.chdir(os.path.dirname(img))

    ## Destination name
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    outfile = os.path.join(destdir, img.split('/')[-1])

    dimensions = ''
    ## Get variable values for processing
    aspect_ratio = get_aspect_ratio(img)
    dimensions = get_dimensions(img)
    width  = dimensions.split('x')[0]
    height = dimensions.split('x')[1]

    if aspect_ratio == '1.2':
        vert_horiz = '{0}x{1}'.format(width,height)
        dimensions = '{0}x{1}'.format(int(width),int(height))
    elif float(aspect_ratio) > float(int(1.2)):
        vert_horiz = 'x{0}'.format(height)
        w = float(0.8) * float(height)
        #w = float(round(w,2)*float(aspect_ratio))
        dimensions = '{0}x{1}'.format(int(w),int(height))
        print "W",w, aspect_ratio
    elif float(aspect_ratio) < float(1.2):
        vert_horiz = '{0}x'.format(width)
        h = float(1.2) * float(width)
        #h = float(round(h,2)*float(aspect_ratio))
        dimensions = '{0}x{1}'.format(int(width),int(h))
        print "H",h, aspect_ratio

    if not dimensions:
        dimensions = '100%'
        vert_horiz = '100%'

    print dimensions,vert_horiz, width, height, aspect_ratio
    #imgformat = img.split('.')[-1]
    if regex_valid_style.findall(img):
        subprocess.call([
            'convert',
            "-colorspace",
            "RGB",
            '-format',
            'png',
            img,
            '-crop',
            str(
            subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
            ,
            '-define',
            'png:preserve-colormap',
            '-define',
            'png:format=png24',
            # '-define',
            # 'png:compression-level=N',
            # '-define',
            # 'png:compression-strategy=N',
            # '-define',
            # 'png:compression-filter=N',
            "-filter",
            "Spline",
            #"-filter",
            #"Catrom",
            #"-filter",
            #"Mitchell",
            #"-define",
            #"filter:filter=QuadraticJinc",
            "-define",
            "filter:win-support=12",
            "-define",
            "filter:support=8",
            "-define",
            "filter:blur=0.625",
            #"filter:blur=0.88549061701764",
            "-distort",
            "Resize",
            vert_horiz,
            '-background',
            'white',
            '-gravity',
            'center',
            '-extent',
            dimensions,
            "-colorspace",
            "sRGB",
            '-unsharp',
            '2x2.7+0.5+0',
            '-quality',
            '100',
            outfile
            ])

        print 'Done {}'.format(outfile)
        return outfile
    else:
        return img

#############################

##### Upload tmp_loading dir to imagedrop via FTP using Pycurl  #####
def pycurl_upload_imagedrop(img):
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
        #c.setopt(pycurl.PORT , 21)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
        #c.setopt(pycurl.FORBID_REUSE, 1)
        #c.setopt(pycurl.FRESH_CONNECT, 1)
        f = open(localFilePath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
        #c.setopt(pycurl.READFUNCTION, f.read());
        #c.setopt(pycurl.READDATA, f.read());
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

#####
###
## backup for 56 then 7 curl err
def upload_to_imagedrop(img):
    import ftplib
    session = ftplib.FTP('file3.bluefly.corp', 'imagedrop', 'imagedrop0')
    fileread = open(file, 'rb')
    filename = str(file.split('/')[-1])
    session.cwd("ImageDrop/")
    session.storbinary('STOR ' + filename, fileread, 8*1024)
    fileread.close()
    session.quit()

#############################
import sys,glob,shutil,os,re,datetime
regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')


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

###################
## Create Lock File
###################
#locker = os.path.join(rootdir, 'LOCKED.lock')
#if os.path.isfile(locker):
#    break
#else:
#    with open(locker, 'wb') as f:
#        f.write(todaysdatefull)
#        f.close()

try:
    root_img_dir = os.path.abspath(sys.argv[1])
    destdir = os.path.abspath(sys.argv[2]) #'/Users/johnb/Pictures'
    tmp_processing = root_img_dir
    tmp_loading = destdir
except:
    root_img_dir =  '/mnt/Post_Complete/Complete_to_Load/DropFinalFiles_Only'
    destdir      =  tmp_loading

###########
## Test for ex
#root_img_dir =  tmp_processing
walkedout_tmp = glob.glob(os.path.join(root_img_dir, '*/*.*g'))
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
walkedout_tmp = glob.glob(os.path.join(root_img_dir, '*/*.*g'))
[ shutil.move(file, os.path.join(tmp_processing, os.path.basename(file))) for file in walkedout_tmp ]


### Rename Files moved into Temp Processing Floder
walkedout_tmp = glob.glob(os.path.join(tmp_processing, '*.jpg'))
[ rename_retouched_file(file) for file in walkedout_tmp ]

if os.path.isdir(tmp_processing):
    for img in glob.glob(os.path.join(tmp_processing,'*.??g')):
        if regex_coded.findall(img):
            img = rename_retouched_file(img)
        pngout = subproc_magick_png(img, destdir=tmp_processing)
        subproc_magick_large_jpg(pngout, destdir=tmp_loading)
        subproc_magick_medium_jpg(pngout, destdir=tmp_loading)
        #subproc_magick_large_jpg(img, destdir=destdir)
        #subproc_magick_medium_jpg(img, destdir=destdir)


    #metadict = metadata_info_dict(img)
    #dimens = get_imagesize_variables(img)
    #test_img = get_image_color_minmax(img)


### Glob created PNGs and copy to Load Dir then Store in Arch dir
tmp_png = glob.glob(os.path.join(tmp_processing, '*.png'))
[ shutil.copy2(file, os.path.join(tmp_loading, os.path.basename(file))) for file in tmp_png ]
[ shutil.move(file, os.path.join(imgdest_png_final, os.path.basename(file))) for file in tmp_png ]

## ARCHIVED Backup
## All JPGs in Root dir Only of tmp_processing will be now Archived as all Conversions are completed

###### All PNGs Created and moved to Archive plus Copy sent to Load Directory
###
######
#### All Files Converted for Upload, Now glob search and move large and medium named jpgs to tmp loading
###
#load_jpgs = glob.glob(os.path.join(tmp_processing, '*/*.jpg'))
#[ shutil.move(file, os.path.join(tmp_loading, os.path.basename(file))) for file in load_jpgs ]

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
            time.sleep(float(3))
            try:
                ftpload_to_imagedrop(upload_file)
                print "Uploaded {}".format(upload_file)
                time.sleep(float(.3))
                shutil.move(upload_file, archive_uploaded)
            except:
                pass
        else:
            print "Uploaded {}".format(upload_file)
            time.sleep(float(.3))
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
