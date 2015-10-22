#!/usr/bin/env python
# -*- coding: utf-8 -*-

## TODO: Replace below copy_to_imagedrop_upload with the Mozu Load/Update process
def copy_to_imagedrop_upload(src_filepath, destdir=None):
    import os, shutil, re
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
        print 'Missing ratio'
        pass


def get_dimensions(img):
    from PIL import Image
    try:
        im = Image.open(img)
        w,h = im.size
        dimensions = "{0}x{1}".format(int(w),int(h))
        return dimensions
    except IOError:
        print 'Missing dimensions'
        pass

## Used only for embedding metadata
def get_exif_metadata_value(img, exiftag=None):
    try:
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
    except ImportError:
        print 'Missing pyexiv2 package. Try and find in apt-get, then pip or easy install or ignore this func'
        pass

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
                print "{0} Files Remaining-TypeError".format(count)
                pass
            except TypeError:
                #print ' PAssing ', f
                pass
        except ZeroDivisionError:
            filevalue_dict[f] = {'ratio_range': 'OutOfRange'}
            count -= 1
            print "{0} Files Remaining-ZeroDivision".format(count)
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
    try:
        if float(str(aspect_ratio)) == float(1.2):
            vert_horiz = '200x240'
        elif float(str(aspect_ratio)) > float(1.2):
            vert_horiz = 'x240'
        elif float(str(aspect_ratio)) < float(1.2):
            vert_horiz = '200x'
    except ValueError:
        print 'ValueError with --> ', img
        vert_horiz = '200x240'

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


def subproc_magick_png(img, rgbmean=None, destdir=None):
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
    if not rgbmean:
        ratio_range = 'OutOfRange'
    else:
        try:
            ratio_range = rgbmean['ratio_range']
        except:
            ratio_range = 'OutOfRange'
            pass

    if ratio_range != 'OutOfRange':
        high        = rgbmean['high']
        low         = rgbmean['low']
        ratio       = rgbmean['ratio']
    #rgbmean = float(128)
    #rgbmean = get_image_color_minmax(img)
    if ratio_range == 'LOW':
        if float(round(high,2)) > float(240):
            modulator = '-modulate'
            modulate = '104,100'
        elif float(round(high,2)) > float(200):
            modulator = '-modulate'
            modulate = '107,110'
        elif float(round(high,2)) > float(150):
            modulator = '-modulate'
            modulate =  '110,110'
        else:
            modulator = '-modulate'
            modulate =  '112,110'

    elif ratio_range == 'HIGH':
        if float(round(high,2)) > float(230):
            modulator = '-modulate'
            modulate = '100,100'
        elif float(round(high,2)) > float(200):
            modulator = '-modulate'
            modulate = '103,100'
        elif float(round(high,2)) > float(150):
            modulator = '-modulate'
            modulate = '105,105'
        else:
            modulator = '-modulate'
            modulate =  '108,107'
    elif ratio_range == 'OutOfRange':
        modulator = '-modulate'
        modulate = '100,100'

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


def upload_imagedrop(root_dir):
    import os, sys, re, csv, shutil, glob
    archive_uploaded = os.path.join(root_dir, 'uploaded')
    tmp_failed = os.path.join(root_dir, 'failed_upload')
    try:
        os.makedirs(archive_uploaded, 16877)
    except OSError:
        try:
            shutil.rmtree(archive_uploaded, ignore_errors = True)
            os.makedirs(archive_uploaded, 16877)
        except:
            pass

    try:
        os.makedirs(tmp_failed, 16877)
    except:
        pass

    import time
    upload_tmp_loading = glob.glob(os.path.join(root_dir, '*.*g'))
    for upload_file in upload_tmp_loading:
        try:
            code = copy_to_imagedrop_upload(upload_file)
            if code == True or code == '200':
                try:
                    shutil.move(upload_file, archive_uploaded)
                    time.sleep(float(.1))
                    print "1stTryOK", upload_file
                except OSError:
                    dst_file = upload_file.replace(root_dir, archive_uploaded)
                    print 'OSError I think...dst_file'
                    try:
                        if os.path.exists(dst_file):
                            os.remove(dst_file)
                        shutil.move(upload_file, archive_uploaded)
                    except AttributeError:
                        print 'AttributeError I think.../'
                        pass
            else:
                print "Uploaded {}".format(upload_file)
                time.sleep(float(.1))
                try:
                    shutil.move(upload_file, archive_uploaded)
                except shutil.Error:
                    print 'shutil line 677 Error I think.../'
                    pass
        except OSError:
            print "Error moving Finals to Arch {}".format(file)
            try:
                shutil.move(upload_file, tmp_failed)
            except shutil.Error:
                pass

    try:
        if os.path.isdir(sys.argv[2]):
            finaldir = os.path.abspath(sys.argv[2])
            for f in glob.glob(os.path.join(archive_uploaded, '*.*g')):
                try:
                    shutil.move(f, finaldir)
                except shutil.Error:
                    pass
    except:
        print 'Failed to Archive {}'.format(upload_tmp_loading)
        pass


def main(root_img_dir=None):
    import sys,glob,shutil,os,re
    from image_processing.magick_tweaks import convert_img_srgb
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.[JjPpNnGg]{3}$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    if not root_img_dir:
        try:
            root_img_dir = sys.argv[1]
            if root_img_dir == 'jblocal':
                root_img_dir = os.path.abspath('/mnt/Post_Ready/Retouchers/JohnBragato/MARKETPLACE_LOCAL')
            else:
                root_img_dir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')
        except IndexError:
            root_img_dir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')
            pass
    else:
        pass

    try:
        destdir = os.path.abspath(sys.argv[2])

        if not os.path.isdir(destdir):
            os.makedirs(destdir, 16877)
    except IndexError:
        destdir =  '/mnt/Post_Complete/ImageDrop/' ##os.path.join(root_img_dir, 'output')
        # try:
        #     os.makedirs(destdir, 16877)
        # except OSError:
        #     pass

    if not type(root_img_dir) == list and os.path.isdir(root_img_dir):
        #import md5_unique_dup_files
        #duplicates = md5_unique_dup_files.find_duplicate_imgs(root_img_dir)[1]
        #[ os.remove(f) for f in duplicates if f ]
        imgs_renamed = [rename_retouched_file(f) for f in (glob.glob(os.path.join(root_img_dir,'*.??[gG]')))]
        img_dict = sort_files_by_values(glob.glob(os.path.join(root_img_dir,'*.??[gG]')))

        for k,v in img_dict.items():
            try:
                img = k
                ## Convert profile of source img if CMYK ignores if RGB
                convert_img_srgb.main(image_file=img)
                ## Get color pixel values from source img
                rgbmean     = v.items()
                ## Generate png from source then jpgs from png

                pngout = subproc_magick_png(img, rgbmean=dict(rgbmean), destdir=destdir)
                ## TODO: pngout will be the image to POST to mozu returned from mozu
                #  ie. response = send_to_mozu(pngout)  then save response in postgres --> and push the id to mozu again

                from mozu import mozu_exec
                mz_res = mozu_exec.main(pngout)
                print mz_res, ' <-- MOZU-Done'
                subproc_magick_large_jpg(pngout, destdir=destdir)
                subproc_magick_medium_jpg(pngout, destdir=destdir)
            except AttributeError:
                print 'SOMETHING IS WRONG WITH THE IMAGE Error {}'.format(img)
                pass

    else:
        'Image is ', root_img_dir
        img = root_img_dir
        if regex_coded.findall(img):
            img = rename_retouched_file(img)
        pngout = subproc_magick_png(img, destdir=destdir)
        from mozu import mozu_exec as mozu_exec
        mz_res = mozu_exec.main(pngout)
        print mz_res, ' <-- MOZU-Done'
        subproc_magick_large_jpg(pngout, destdir=destdir)
        subproc_magick_medium_jpg(pngout, destdir=destdir)


    #try:
    #    upload_imagedrop(destdir)
    #    failed_dir = os.path.join(destdir,'failed_upload','*.??[gG]')
    #except:
    #    print 'PrintUploadFailed'
    #    pass
    # while True:
    #     if glob.glob(failed_dir):
    #         destdir = failed_dir
    #         failed_dir = os.path.join(destdir,'failed_upload','*.??[gG]')
    #         upload_imagedrop(destdir)
    #print 'NOT UPLOADING YET'

if __name__ == '__main__':
    main()
