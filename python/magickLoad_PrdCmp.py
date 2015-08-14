#!/usr/bin/env python
# -*- coding: utf-8 -*-


def copy_to_imagedrop_upload(src_filepath, destdir=None):
    import pycurl, os, shutil, re
    regex_colorstyle = re.compile(r'^.*?/[0-9]{9}[_altm0-6]{,6}?\.[jpngJPNG]{3}$')
    if not regex_colorstyle.findall(src_filepath):
        print src_filepath.split('/')[-1], ' Is Not a valid Bluefly Colorstyle File or Alt Out of Range'
        return
    else:
        if not destdir:
            destdir = '/mnt/Post_Complete/ImageDrop'
        imagedrop         = os.path.abspath(destdir)
        localFileName     = src_filepath.split('/')[-1]
        imagedropFilePath = os.path.join(imagedrop, localFileName.lower())
        try:
            if os.path.isfile(imagedropFilePath):
                try:
                    os.remove(imagedropFilePath)
                    #os.rename(src_filepath, imagedropFilePath)
                    shutil.copyfile(src_filepath, imagedropFilePath)
                    return True
                except:
                    print 'Error ', imagedropFilePath
                    return False
                    #shutil.copyfile(src_filepath, imagedropFilePath
            else:
                ##os.rename(src_filepath, imagedropFilePath)
                shutil.copyfile(src_filepath, imagedropFilePath)
                return True
        except:
            return False


def rename_retouched_file(img):
    import os,re
    regex_coded = re.compile(r'.+?/[1-9][0-9]{8}_[1-6]\.[jJpPnNgG]{3}')
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
                    filename = "{}{}{}".format(colorstyle,alt,ext)
                    renamed = os.path.join(filedir, filename)
                    print renamed
                if renamed:
                    os.rename(img, renamed)
                    if os.path.isfile(renamed):
                        return renamed
        else:
            return img


def get_aspect_ratio(img):
    from PIL import Image
    try:
        im = Image.open(img)
        w,h = im.size
        aspect_ratio = str(round(float(int(h))/float(int(w)),2))
        return aspect_ratio
    except IOError:
        pass


def get_dimensions(img):
    from PIL import Image
    try:
        im = Image.open(img)
        w,h = im.size
        dimensions = "{0}x{1}".format(int(w),int(h))
        return dimensions
    except IOError:
        pass


def get_exif_metadata_value(img, exiftag=None):
    import pyexiv2
    image_metadata = pyexiv2.ImageMetadata(img)
    metadata = image_metadata.read()
    if exiftag:
        exifvalue = metadata[exiftag]
        return (exiftag, exifvalue)

    else:
        metadict = {}
        for mtag, mvalue in metadata.iteritems():
            metadict[mtag] = mvalue
        return metadict


def get_image_color_minmax(img):
    import subprocess, os, sys, re
    try:
        ret = subprocess.check_output(['convert', img, '-median', '3', '+dither', '-colors', '2', '-trim', '+repage', '-gravity', 'center', '-crop', "50%", '-depth', '8', '-format', '%c',"histogram:info:-"])
    except:
        return ''
    colorlow = str(ret).split('\n')[0].strip(' ')
    colorlow =  re.sub(re.compile(r',\W'),',',colorlow).replace(':','',1).replace('(','').replace(')','').replace('  ',' ').split(' ')
    colorhigh = str(ret).split('\n')[1].strip(' ')
    colorhigh =  re.sub(re.compile(r',\W'),',',colorhigh).replace(':','',1).replace('(','').replace(')','').replace('  ',' ').split(' ')
    fields_top =  ['low_rgb_avg', 'high_rgb_avg']
    fields_level2  =  ['total_pixels', 'rgb_vals', 'webcolor_id', 'color_profile_vals']

    colorlow  = zip(fields_level2,colorlow)
    colorhigh  = zip(fields_level2,colorhigh)
    if len(colorhigh) == len(colorlow):
        coloravgs = dict(colorlow),dict(colorhigh)
        colordata = zip(fields_top, coloravgs)
        colordata = dict(colordata)
        colordata['comp_level'] = 'InRange'
        return colordata

    elif len(colorhigh) < len(colorlow):
        coloravgs = dict(colorlow)
        colordata = {}
        colordata[fields_top[0]] = coloravgs
        colordata[fields_top[1]] = {'total_pixels': 0}
        colordata['comp_level'] = 'Bright'
        return colordata

    elif len(colorhigh) > len(colorlow):
        coloravgs = dict(colorhigh)
        colordata = {}
        colordata[fields_top[1]] = coloravgs
        colordata[fields_top[0]] == {'total_pixels': 0}
        colordata['comp_level'] = 'Dark'
        return colordata


def evaluate_color_values(colordata):
    high_range_pixels = ''
    low_range_pixels  = ''
    high_range_pixels = float((colordata['high_rgb_avg']['total_pixels']))
    low_range_pixels   = float((colordata['low_rgb_avg']['total_pixels']))
    try:

        if low_range_pixels >= high_range_pixels and high_range_pixels != 0:
            r,g,b = colordata['high_rgb_avg']['rgb_vals'].split(',')
            r,g,b = float(r),float(g),float(b)
            high_avg = float(round((r+b+g)/3,2))
            r,g,b = colordata['low_rgb_avg']['rgb_vals'].split(',')
            r,g,b = float(r),float(g),float(b)
            low_avg = float(round((r+b+g)/3,2))

            ratio   =  round(float(float(low_range_pixels)/float(high_range_pixels)),2)
            print high_avg/(low_avg*ratio)
            return high_avg,low_avg,ratio, 'LOW'

        elif low_range_pixels < high_range_pixels and low_range_pixels != 0:
            r,g,b = colordata['high_rgb_avg']['rgb_vals'].split(',')
            r,g,b = float(r),float(g),float(b)
            high_avg = float(round((r+b+g)/3,2))
            r,g,b = colordata['low_rgb_avg']['rgb_vals'].split(',')
            r,g,b = float(r),float(g),float(b)
            low_avg = float(round((r+b+g)/3,2))

            ratio   =  round(float(float(low_range_pixels)/float(high_range_pixels)),2)
            print low_avg/(high_avg*ratio)
            return high_avg,low_avg,ratio, 'HIGH'
    except TypeError:
        print "Type Error"
        pass
    except ValueError:
        print "Value Error", colordata
        pass


def sort_files_by_values(fileslist):
    import os,glob
    filevalue_dict = {}
    count = len(fileslist)
    for f in fileslist:
        values = {}
        colordata = get_image_color_minmax(f)
        try:
            high,low,ratio, ratio_range = evaluate_color_values(colordata)
            values['ratio'] = ratio
            values['ratio_range'] = ratio_range
            if ratio_range == 'LOW':
                values['low'] = low ##

                values['high'] = high
            if ratio_range  == 'HIGH':
                values['high'] = high ##

                values['low'] = low

            filevalue_dict[f] = values
            count -= 1
            print "{0} Files Remaining".format(count)
        except TypeError:
            try:
                filevalue_dict[f] = {'ratio_range': 'OutOfRange'}
                count -= 1
                #print "{0} Files Remaining-TypeError".format(count)
                pass
            except TypeError:
                #print ' PAssing ', f
                pass
        except ZeroDivisionError:
            filevalue_dict[f] = {'ratio_range': 'OutOfRange'}
            count -= 1
            #print "{0} Files Remaining-ZeroDivision".format(count)
            pass
    return filevalue_dict


def subproc_magick_large_jpg(img, destdir=None):
    import subprocess,os,re
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')
    regex_valid_style_PNG = re.compile(r'^.+?/[1-9][0-9]{8}.[JjPpNnGg]{3}$')

    os.chdir(os.path.dirname(img))

    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    # if not regex_alt.findall(img):
    if regex_valid_style_PNG.findall(img):
        outfile = os.path.join(destdir, img.split('/')[-1][:9] + '_l.jpg')

        # dimensions = get_dimensions(img)
        # width  = dimensions.split('x')[0]
        # height = dimensions.split('x')[1]
        # if aspect_ratio == '1.2':

        aspect_ratio = get_aspect_ratio(img)
        if float(str(aspect_ratio)) == float(1.2):
            vert_horiz = '400x480'
        elif float(str(aspect_ratio)) > float(1.2):
            vert_horiz = 'x480'
        elif float(str(aspect_ratio)) < float(1.2):
            vert_horiz = '400x'

        dimensions = "400x480"
        #print dimensions, vert_horiz

        ext = img.split('.')[-1]

        if regex_valid_style_PNG.findall(img):
            subprocess.call([
            'convert',
            '-colorspace',
            'sRGB',
            img,
            '-format',
            ext,
            '-background',
            'white',
            "-filter",
            "Spline",
            "-filter",
            "Cosine",
            "-define",
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
            # '-strip',
            '-quality',
            '95',
            outfile
            ])
            return outfile
        else:
            return img
    else:
        pass


def subproc_magick_medium_jpg(img, destdir=None):
    import subprocess,os,re
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    os.chdir(os.path.dirname(img))
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    if regex_alt.findall(img):
        outfile = os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.jpg')
    else:
        outfile = os.path.join(destdir, img.split('/')[-1][:9] + '_m.jpg')


    # dimensions = get_dimensions(img)
    # width  = dimensions.split('x')[0]
    # height = dimensions.split('x')[1]
    #if aspect_ratio == '1.2':

    aspect_ratio = get_aspect_ratio(img)
    print img, aspect_ratio, ' <--X '

    if float(str(aspect_ratio)) == float(1.2):
        vert_horiz = '200x240'
    elif float(str(aspect_ratio)) > float(1.2):
        vert_horiz = 'x240'
    elif float(str(aspect_ratio)) < float(1.2):
        vert_horiz = '200x'

    dimensions = '200x240'
    #print dimensions,vert_horiz, ' _m.jpg '

    ext = img.split('.')[-1]

    if regex_valid_style.findall(img):

        subprocess.call([
            'convert',
            '-colorspace',
            'sRGB',
            img,
            '-format',
            ext,
            '-background',
            'white',
            "-filter",
            "Spline",
            "-filter",
            "Cosine",
            "-define",
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
            '-strip',
            '-quality',
            '95',
            outfile
            ])
        return outfile
    else:
        return img


def subproc_magick_png(img, destdir=None):
    import subprocess,re,os
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')
    modulator = ''
    modulate = ''
    if not destdir:
        destdir = '.'
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    os.chdir(os.path.dirname(img))
    # if not rgbmean:
    #     ratio_range = 'OutOfRange'
    # else:
    #     try:
    #         ratio_range = rgbmean['ratio_range']
    #     except:
    #         ratio_range = 'OutOfRange'
    #         pass

    # if ratio_range != 'OutOfRange':
    #     high        = rgbmean['high']
    #     low         = rgbmean['low']
    #     ratio       = rgbmean['ratio']
    # #rgbmean = float(128)
    # #rgbmean = get_image_color_minmax(img)
    # if ratio_range == 'LOW':
    #     if float(round(high,2)) > float(240):
    #         modulator = '-modulate'
    #         modulate = '104,100'
    #     elif float(round(high,2)) > float(200):
    #         modulator = '-modulate'
    #         modulate = '107,110'
    #     elif float(round(high,2)) > float(150):
    #         modulator = '-modulate'
    #         modulate =  '110,110'
    #     else:
    #         modulator = '-modulate'
    #         modulate =  '112,110'

    # elif ratio_range == 'HIGH':
    #     if float(round(high,2)) > float(230):
    #         modulator = '-modulate'
    #         modulate = '100,100'
    #     elif float(round(high,2)) > float(200):
    #         modulator = '-modulate'
    #         modulate = '103,100'
    #     elif float(round(high,2)) > float(150):
    #         modulator = '-modulate'
    #         modulate = '105,105'
    #     else:
    #         modulator = '-modulate'
    #         modulate =  '108,107'
    # elif ratio_range == 'OutOfRange':
    #     modulator = '-modulate'
    #     modulate = '100,100'

    format = img.split('.')[-1]

    os.chdir(os.path.dirname(img))

    ## Destination name
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    outfile = os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')

    h=''
    w=''
    dimensions = ''
    ## Get variable values for processing
    aspect_ratio = get_aspect_ratio(img)
    dimensions = get_dimensions(img)
    width = dimensions.split('x')[0]
    height = dimensions.split('x')[1]
    vert_horiz = ''

    print '', '==> InitiaDims widXheight == --> ', dimensions, width, height
    if str(aspect_ratio) == '1.0':
        vert_horiz = '{0}x!'.format(width)
        h = float(1.2) * float(width)
        dimensions = '{0}x{1}'.format(int(width), int(h))
        print '2', dimensions
        if width > 2000:
            vert_horiz = '2000x'
            dimensions = '2000x2400'
            print 'xxxxxxxxxxx', h, height, width

    elif str(aspect_ratio) == '1.2':
        vert_horiz = '{0}x{1}'.format(width, height)
        dimensions = '{0}x{1}'.format(int(width), int(height))
        print '1'
    elif int(height) > int(width): #float(str(aspect_ratio)) > float(1.2):
        vert_horiz = 'x{0}'.format(height)
        w = float(0.833) * float(height)
        # w = float(round(w,2)*float(aspect_ratio))
        dimensions = '{0}x{1}'.format(int(w), int(height))
        print '3', w, dimensions, vert_horiz
    elif int(height) < int(width): #float(str(aspect_ratio)) < float(1.2):
        vert_horiz = '{0}x'.format(width)
        h = float(1.2) * float(width)
        # h = float(round(h,2)*float(aspect_ratio))
        dimensions = '{0}x{1}'.format(int(width), int(h))
        print '4', h, dimensions, vert_horiz

    print '\nwidth={}\nheight={}\nw={}\th={}\naspect={}\ndimension={}'.format(width,height,w,h,aspect_ratio,dimensions)

    if not dimensions:
        dimensions = '100%'
        vert_horiz = '100%'
        print ' Not Dimensions PNG faster2-->', img

    if dimensions and dimensions != '100%' or not vert_horiz:
        
        if not dimensions == '2000x2400':
            try:
                del h
                del w
            except:
                pass
            h = int(dimensions.split('x')[-1])
            w = int(dimensions.split('x')[0])
            print 'width={}\nheight={}\nw={}\th={}\naspect={}\ndimension={}'.format(width,height,w,h,aspect_ratio,dimensions)
            if w > 2000 or h > 2400:
                print 'xxxxxxxxxxx', h, w
                if int(height) >= int(width):
                    if int(height) > int(width):
                        vert_horiz = 'x2400'
                        dimensions = '2000x2400'
                        print 'AUX2',  #height, 'hite<---->witth', width
                    elif h > 2400:
                        vert_horiz = 'x{0}'.format(h)
                        w = float(0.833) * float(h)
                        dimensions = '{0}x{1}'.format(int(w), int(h))
                        print 'AUX3',  height, 'hite<---->witth', width
                elif int(width) > int(height):
                    if w > 2000:
                        vert_horiz = '2000x'
                        dimensions = '2000x2400'
                        print 'AUX4',  #height, 'hite<---->witth', width
                    else:
                        vert_horiz = '{0}x'.format(w)
                        h = float(1.2) * float(width)
                        dimensions = '{0}x{1}'.format(int(w), int(h))
                        print 'AUX5',  #height, 'hite<---->witth', width


    #print dimensions, ' VERT PNG Fin ', vert_horiz, aspect_ratio


    # Create a safe png then copy it and reuse tmp in following procs
    #import tempfile, shutil
    #tmpfileobj, tmpfile_path = tempfile.mkstemp(suffix=".png")

    subprocess.call([
        'convert',
        '-format',
        format,
        img,
        # "-define",
        #                    "stream:buffer-size\=0",
        '-define',
        'png:preserve-colormap\=true',
        '-define',
        'png:preserve-iCCP\=true',
        '-define',
        'png:format\=png24',
        '-define',
        'png:compression-level\=N',
        '-define',
        'png:compression-strategy\=N',
        '-define',
        'png:compression-filter\=N',
        '-format',
        'png',
        '-modulate',
        modulate,
        '-depth',
        '8',

        "-density",
        "72",
        "-units",
        "pixelsperinch",

        # '-bordercolor',
        # 'white',
        # '-border',
        # '1x1',

        '-background',
        'white',

        "-define",
        "filter:blur=0.625",
        #"filter:blur=0.88549061701764",

        # '-crop',
        # str(subprocess.call(["convert", img, "-virtual-pixel", "edge", "-blur", "0x15", "-fuzz", "1%", "-trim", "-format", "%wx%h%O", "info:"], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
        # ,

        #"-fuzz",
        #"10%",
        #"-trim",
        #'-gravity',
        #'center',
        #'+repage',
        #"-gamma",
        #".45455",

        "-distort",
        "Resize",
        #"-resample",
        vert_horiz,

        #"-gamma",
        #"2.2",

        '-background',
        'white',
        '-gravity',
        'center',
        '-extent',
        dimensions,  ## +">",

        "-colorspace",
        "sRGB",
        #"-strip",
        '-unsharp',
        '2x2.7+0.5+0',
        '-quality',
        '95',
        outfile
    ])


    #tmpfileobj.close()
    #shutil.copy2(tmpfile_path,outfile)
    #print 'Done {}'.format(img)
    return outfile #open(outfile).read() # tmpfile_path  #os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')

#############################

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
    root_img_dir =  '/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly'
    destdir      =  tmp_loading
if os.path.isdir(root_img_dir): pass
else:
    root_img_dir =  '/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly'
    destdir      =  tmp_loading


###########
## Test for ex
#root_img_dir =  tmp_processing
walkedout_tmp = glob.glob(os.path.join(root_img_dir, '*/*.*g'))
image_ct = len(walkedout_tmp)
starttime = todaysdatefull
if image_ct == 0:
    print "Nothing to Process"
else:
### Make Tmp Folders for Processing And Uploading -- tmp_dirs are dated with time(hr:min)to prevent collisions
    print 'Processing -- %s Files \nStarted --> %s \n' % (image_ct, starttime)
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
    for img in glob.glob(os.path.join(tmp_processing,'*.??[gG]')):
        if regex_coded.findall(img):
            img = rename_retouched_file(img)
        pngout = subproc_magick_png(img, destdir=tmp_processing)
        subproc_magick_large_jpg(pngout, destdir=tmp_loading)
        subproc_magick_medium_jpg(pngout, destdir=tmp_loading)
        #os.rename(pngout,os.path.join())
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

## UPLOAD NFS with PyCurl everything in tmp_loading
###
import time
upload_tmp_loading = glob.glob(os.path.join(tmp_loading, '*.*g'))
for upload_file in upload_tmp_loading:
    #### UPLOAD upload_file via NFS to imagedrop
    ## Then rm loading tmp dir
    try:
        result = copy_to_imagedrop_upload(upload_file, destdir='/mnt/Post_Complete/ImageDrop')
        if result:
            print "Uploaded {}".format(upload_file)
            time.sleep(float(.1))
            shutil.move(upload_file, archive_uploaded)
        else:
            print result, upload_file
            pass
            ##time.sleep(float(3))
            # try:
            #     ftpload_to_imagedrop(upload_file)
            #     print "Uploaded {}".format(upload_file)
            #     time.sleep(float(.3))
            #     shutil.move(upload_file, archive_uploaded)
            # except:
            #     pass

    except:
        print "Error moving Finals to Arch {}".format(file)

### Check for okb files and send to Uploader via email
zerobytefiles = glob.glob(os.path.join('/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly/zero_byte_errors', '*/*.*g'))
# if zerobytefiles:
#     import jbmodules.mailing_funcs
#     for f in zerobytefiles:
#         groupeddict = jbmodules.mailing_funcs.failed_upload_alerts(f)
#         send_email_zerobyte_alerts(groupeddict=groupeddict)

## After completed Process and Load to imagedrop
###  Finally Remove the 2 tmp folder trees for process and load if Empty
try:
    upload_tmp_loading_remainder = glob.glob(os.path.join(tmp_loading, '*.*g'))
    if len(upload_tmp_loading_remainder) == 0:
        shutil.rmtree(tmp_loading)

except:
    pass

## remove the processing tmp folder
shutil.rmtree(tmp_processing)

# try:
#     upload_tmp_processing_png_remainder = glob.glob(os.path.join(tmp_processing, '*.*g'))
#     upload_tmp_processing_jpg_remainder = glob.glob(os.path.join(tmp_processing, '*/*.*g'))
#     if len(upload_tmp_processing_png_remainder) == 0 and len(upload_tmp_processing_jpg_remainder) == 0:
       
# except:
#     pass

###################
## Remove Lock file
###################
#if os.path.isfile(locker):
#    os.remove(locker)
