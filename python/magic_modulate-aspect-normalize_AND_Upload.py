#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re, csv
##### Upload tmp_loading dir to imagedrop via FTP using Pycurl  #####
def pycurl_upload_imagedrop(img):
    import pycurl, os
    #import FileReader
    localFilePath = os.path.abspath(img)
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

################# Begin Image functions

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


def get_exif_metadata_value(img, exiftag=None):
    #from PIL import Image
    import pyexiv2
    # Read EXIF data to initialize
    image_metadata = pyexiv2.ImageMetadata(img)
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

def get_image_color_minmax(img):
    import subprocess, os, sys, re
    ret = subprocess.check_output(['convert', img, '-median', '3', '+dither', '-colors', '2', '-trim', '+repage', '-gravity', 'center', '-crop', '50%', '-depth', '8', '-format', '%c','histogram:info:-'])    
    ## Prepare cleaned output as list or dict
    colorlow = str(ret).split('\n')[0].strip(' ')
    colorlow =  re.sub(re.compile(r',\W'),',',colorlow).replace(':','',1).replace('(','').replace(')','').replace('  ',' ').split(' ')
    colorhigh = str(ret).split('\n')[1].strip(' ')
    colorhigh =  re.sub(re.compile(r',\W'),',',colorhigh).replace(':','',1).replace('(','').replace(')','').replace('  ',' ').split(' ') 
    fields_top =  ['low_rgb_avg', 'high_rgb_avg']
    fields_level2  =  ['total_pixels', 'rgb_vals', 'webcolor_id', 'color_profile_vals']
    # x = { zip(field.split(','),color.split(',')) for color in colormin }
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
            #print low_range_pixels, high_range_pixels
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
            #print low_range_pixels, high_range_pixels
            ratio   =  round(float(float(low_range_pixels)/float(high_range_pixels)),2)
            print low_avg/(high_avg*ratio)
            return high_avg,low_avg,ratio, 'HIGH' 
    except TypeError:
        print "Type Error"
        pass
    except ValueError:
            print "Value Error", colordata
            pass

def sort_files_by_values(directory):
    import os,glob    
    filevalue_dict = {}
    # if type(directory) == 'list':
    fileslist = directory
    # elif os.path.isdir(directory):
    #    fileslist = glob.glob(os.path.join(os.path.abspath(directory), '*.??g'))
    count = len(fileslist)
    for f in fileslist: 
        values = {}
        colordata = get_image_color_minmax(f)
        try: 
            high,low,ratio, ratio_range = evaluate_color_values(colordata)
            values['ratio'] = ratio
            values['ratio_range'] = ratio_range
            if ratio_range == 'LOW':
                values['low'] = low #*ratio
                values['high'] = high 
            if ratio_range  == 'HIGH':
                values['high'] = high #*ratio
                values['low'] = low
                
            filevalue_dict[f] = values
            count -= 1
            print "{0} Files Remaining".format(count)
        except TypeError:
            filevalue_dict[f] = {'ratio_range': 'OutOfRange'}
            count -= 1
            print "{0} Files Remaining-TypeError".format(count)
            pass
        except ZeroDivisionError:
            filevalue_dict[f] = {'ratio_range': 'OutOfRange'}
            count -= 1
            print "{0} Files Remaining-ZeroDivision".format(count)
            pass
    return filevalue_dict


##### ##### ##### ########## ##### ##### #####
##### ##### ##### ########## ##### ##### #####

### End Data extract Funx, below processors
#

### Large Jpeg Convert to  _l ??[gG]s
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
            'sRGB',
            img,
            # '-crop',
            # str(
            # subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
            # ,
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
        outfile = os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.jpg')
    else:
        outfile = os.path.join(destdir, img.split('/')[-1][:9] + '_m.jpg')

    dimensions = ''
    ## Get variable values for processing
    aspect_ratio = get_aspect_ratio(img)
    dimensions = get_dimensions(img)
    width  = dimensions.split('x')[0]
    height = dimensions.split('x')[1]
    
    if aspect_ratio == '1.2':
        vert_horiz = '300x360'
    elif float(aspect_ratio) > float(1.2):
        vert_horiz = 'x360'
    elif float(aspect_ratio) < float(1.2):
        vert_horiz = '300x'
    
    dimensions = '300x360'
    print dimensions,vert_horiz
    if regex_valid_style.findall(img):

        subprocess.call([
            'convert',
            '-colorspace',
            'sRGB',
            img,
            # '-crop',
            # str(
            # subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
            # ,
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
def subproc_magick_png(img, rgbmean=None, destdir=None):
    import subprocess,re,os
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.jpg$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')
    modulater = ''
    modulate = ''
    ratio_range = ''
    #imgdestpng_out = os.path.join(root_img_dir, os.path.basename(imgsrc_jpg))
    os.chdir(os.path.dirname(img))
    if not rgbmean:
        ratio_range = 'OutOfRange'
    
    if ratio_range != 'OutOfRange':
        try:
            high        = rgbmean['high']
        except KeyError:
            pass    
        try:
            low         = rgbmean['low']
        except KeyError:
            pass
        try:
            ratio       = rgbmean['ratio']
        except KeyError:
            pass

    #rgbmean = float(128)
    #rgbmean = get_image_color_minmax(img)
    if ratio_range == 'LOW':
        if float(round(high,2)) > float(240):
            modulater = '-modulate'
            modulate = '105,100'  
        elif float(round(high,2)) > float(200):    
            modulater = '-modulate'
            modulate = '110,110'
        elif float(round(high,2)) > float(150):    
            modulater = '-modulate'
            modulate =  '115,110'    
        else:    
            modulater = '-modulate'
            modulate =  '120,110' 

    elif ratio_range == 'HIGH':
        if float(round(high,2)) > float(230):
            modulater = '-modulate'
            modulate = '100,100'  
        elif float(round(high,2)) > float(200):    
            modulater = '-modulate'
            modulate = '105,100'
        elif float(round(high,2)) > float(150):    
            modulater = '-modulate'
            modulate = '110,105'      
    elif ratio_range == 'OutOfRange':
        modulater = '-modulate'
        modulate = '100,100'
    
    format = img.split('.')[-1]
    os.chdir(os.path.dirname(img))

    ## Destination name
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    outfile = os.path.join(destdir, img.split('/')[-1].split('.')[0] + '.png')

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
        print os.path.abspath(img), outfile        
        subprocess.call([
            'convert',
            "-colorspace",
            "RGB",
            '-format',
            'png',
            img,
            # '-crop',
            # str(
            # subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
            # ,
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
            modulater,
            modulate,
            "-filter",
            "Spline",
            #"-filter",
            #"Catrom",
            #"-filter",
            #"Mitchell",
            #"-define",
            #"filter:filter=QuadraticJinc",
            #"-define", 
            #"filter:win-support=12",
            #"-define",
            #"filter:support=8",
            "-define",
            #"filter:blur=0.625",
            "filter:blur=0.88549061701764",
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
#############################

def upload_imagedrop(root_dir):
    import os, sys, re, csv, shutil, glob
    ## Make the success and fail dirs
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
    #### UPLOAD upload_file via ftp to imagedrop using Pycurl
    upload_tmp_loading = glob.glob(os.path.join(root_dir, '*.*g'))
    for upload_file in upload_tmp_loading:
        #### UPLOAD upload_file via ftp to imagedrop using Pycurl
        ## Then rm loading tmp dir
        try:
            code = pycurl_upload_imagedrop(upload_file)
            if code == '200':
                try:
                    shutil.move(upload_file, archive_uploaded)
                    time.sleep(float(.3))
                    print "1stTryOK"
                except:
                    dst_file = upload_file.replace(root_dir, archive_uploaded)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    shutil.move(upload_file, archive_uploaded)
                    pass
            elif code:
                print code, upload_file
                time.sleep(float(.3))
                try:
                    ftpload_to_imagedrop(upload_file)
                    print "Uploaded {}".format(upload_file)
                    time.sleep(float(.3))
                    shutil.move(upload_file, archive_uploaded)
                except:
                    shutil.move(upload_file, tmp_failed)
                    pass
            else:
                print "Uploaded {}".format(upload_file)
                time.sleep(float(.3))
                shutil.move(upload_file, archive_uploaded)
        except OSError:
            print "Error moving Finals to Arch {}".format(file)
            shutil.move(upload_file, tmp_failed)
            pass

    try:
        if os.path.isdir(sys.argv[2]):
            finaldir = os.path.abspath(sys.argv[2])
            for f in glob.glob(os.path.join(archive_uploaded, '*.*g')):
                shutil.move(f, finaldir)
    except:
        print 'Failed to Archive {}'.format(upload_tmp_loading)
        pass

#############################
#############################
def main():
    import sys,glob,shutil,os,re
    regex_coded = re.compile(r'^.+?/[1-9][0-9]{8}_[1-6]\.[JjPpNnGg]{3}$')
    regex_alt = re.compile(r'^.+?/[1-9][0-9]{8}_\w+?0[1-6]\.[JjPpNnGg]{3}$')
    regex_valid_style = re.compile(r'^.+?/[1-9][0-9]{8}_?.*?\.[JjPpNnGg]{3}$')

    #root_img_dir = '/Users/johnb/Dropbox/DEVROOT/DROP/testfragrancecopy/newsettest/312467701.png'
    root_img_dir = '/mnt/Post_Ready/zProd_Server/imageServer7/var/consignment/vendor_dropoff/marketplace/137550/' #/mnt/Post_Complete/Complete_Archive/MARKETPLACE/vendor_dropoff/marketplace/137550/'# os.path.abspath(sys.argv[1])

    try:
        destdir = os.path.abspath(sys.argv[2]) #'/Users/johnb/Pictures'
        if not os.path.isdir(destdir):
            os.makedirs(destdir)
    except IndexError:
        destdir = os.path.join(root_img_dir, 'output')
        try:
            os.makedirs(destdir)
        except OSError:
            pass

    ##For separating by vendor
    # walkedout_renamed_special = glob.glob(os.path.join(root_img_dir, '*.??g'))
    # #fragrancenet_styles = query_vendors_styles('Fragrancenet')
    # #fragrancenet_imgs = [ f for f in walkedout_renamed_special if fragrancenet_styles.get(os.path.basename(f)[:9]) ]

    # ## Process only fragrance net images to enhance low Rez photo then archive orig
    # img_dict = sort_files_by_values(walkedout_renamed_special)
    # for k,v in img_dict.items():
          #special_img = k
          #rgbmean     = v.items()
          #pngout = subproc_magick_png(special_img, rgbmean=dict(rgbmean), destdir=destdir)
          #subproc_magick_large_jpg(pngout, destdir=destdir)
          #subproc_magick_medium_jpg(pngout, destdir=destdir)

          #magick_fragrance_proc_lrg(pngout, rgbmean=dict(rgbmean), destdir=destdir)
          #magick_fragrance_proc_med(pngout, rgbmean=dict(rgbmean), destdir=destdir)
        
          ## special processed original files move to archive dir making only standard processing files in proc dir
          #shutil.move(special_img, os.path.join(imgdest_jpg_final, os.path.basename(special_img)))


    # all process special files move to upload dir
    # special_processed = glob.glob(os.path.join(root_img_dir, '*.??g'))
    #[ shutil.move(file, os.path.join(tmp_loading, os.path.basename(file))) for file in special_processed ]


    # Process Directory of images as sysarg 1, Dest sysarg 2
    if os.path.isdir(root_img_dir):
        imgs_renamed = [rename_retouched_file(f) for f in (glob.glob(os.path.join(root_img_dir,'*.??[gG]')))]
        img_dict = sort_files_by_values(glob.glob(os.path.join(root_img_dir,'*.??[gG]')))

        for k,v in img_dict.items():
            try:
                img = k
                rgbmean     = v.items()
                pngout = subproc_magick_png(img, rgbmean=dict(rgbmean), destdir=destdir)
                subproc_magick_large_jpg(pngout, destdir=destdir)
                subproc_magick_medium_jpg(pngout, destdir=destdir)
            except AttributeError:
                pass
            
            #subproc_magick_large_jpg(img, destdir=destdir)
            #subproc_magick_medium_jpg(img, destdir=destdir)

    # Process Single images as sysarg 1, Dest sysarg 2
    else:
        img = root_img_dir
        if regex_coded.findall(img):
            img = rename_retouched_file(img)
        pngout = subproc_magick_png(img, destdir=destdir)
        subproc_magick_large_jpg(pngout, destdir=destdir)
        subproc_magick_medium_jpg(pngout, destdir=destdir)
        #metadict = metadata_info_dict(img)
        #dimens = get_imagesize_variables(img)
        #test_img = get_image_color_minmax(img)


    ###### Uploader separate
    ## UPLOAD FTP with PyCurl everything in tmp_loading
    # [ shutil.move(file, os.path.join(tmp_loading, os.path.basename(file))) for file in load_jpgs ]
    
    upload_imagedrop(destdir)


if __name__ == '__main__':
    main()
