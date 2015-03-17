#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
import os, sys, re, csv


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
    

######## Make Images For Upload to Website ##########

# Upload to usr:imagedrop pwd:imagedrop0
def pycurl_upload_imagedrop(localFilePath):
    import pycurl, os
    localFileName = localFilePath.split('/')[-1]

    mediaType = "8"
    ftpURL = "ftp://file3.bluefly.corp/ImageDrop/"
    ftpFilePath = os.path.join(ftpURL, localFileName)
    ftpUSERPWD = "imagedrop:imagedrop0"

    if localFilePath != "" and ftpFilePath != "":
        c = pycurl.Curl()
        c.setopt(pycurl.URL, ftpFilePath)
        c.setopt(pycurl.USERPWD, ftpUSERPWD)
        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(c.CONNECTTIMEOUT, 5)
        c.setopt(c.TIMEOUT, 8)
        c.setopt(c.FAILONERROR, True)
        f = open(localFilePath, 'rb')
        c.setopt(pycurl.INFILE, f)
        c.setopt(pycurl.INFILESIZE, os.path.getsize(localFilePath))
        c.setopt(pycurl.INFILESIZE_LARGE, os.path.getsize(localFilePath))
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
import os, sys, re, shutil, datetime, glob

### Can pass as sys.argv a direcectory with nested directories containing jpgs. Must have nested dirs
try:
    testdir = sys.argv[1]
    if os.path.isdir(testdir):
       rootdir = testdir
    #else:
    #    rootdir = '/mnt/Post_Complete/Complete_to_Load/Drop_FinalFilesOnly'
except IndexError:
    rootdir = '/mnt/Post_Complete/.Vendor_to_Load/upload_drop/VAULT_test'

    

vendorname = rootdir.split('/')[-1].split('_')[0]
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
tmp_processing = os.path.join("/mnt/Post_Complete/.Vendor_to_Load/.tmp_processing" , "tmp_" + str(todaysdatefull).replace(",", ""))
tmp_processing_l = os.path.join(tmp_processing, "largejpg")
tmp_processing_m = os.path.join(tmp_processing, "mediumjpg")
tmp_processing_special = os.path.join(tmp_processing, "special")
tmp_loading = os.path.join("/mnt/Post_Complete/.Vendor_to_Load/.tmp_loading" , "tmp_" + str(todaysdatefull).replace(",", ""))

## Define for Creating Archive dirs
archive = '/mnt/Post_Complete/.Vendor_to_Load/upload_complete/original_by_vendor'
archive_uploaded = os.path.join(archive, "uploaded_" + str(todaysdate).replace(",", ""), vendorname.lower() + str(todaysdatearch).replace(",", ""))

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
############
## Test for existing files to load or kill entire process prior to dir creation
###########
walkedout_tmp = glob.glob(os.path.join(rootdir, '*.*g'))
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
        os.makedirs(tmp_processing_special, 16877)
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
walkedout_tmp = glob.glob(os.path.join(rootdir, '*.*g'))
[ shutil.move(file, os.path.join(tmp_processing, os.path.basename(file))) for file in walkedout_tmp ]

### Rename Files moved into Temp Processing Floder
walkedout_tmp = glob.glob(os.path.join(tmp_processing, '*.jpg'))
[ rename_retouched_file(file) for file in walkedout_tmp ]

### Image Processing BEGIN ####

####### FRAGRANCENET ALT PROCESS DETOUR ####
def query_vendors_styles(vendorname):
    import sqlalchemy
    orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')    
    connection = orcl_engine.connect()

    querymake_vendors_product_details = "SELECT DISTINCT POMGR.PO_LINE.PRODUCT_COLOR_ID as colorstyle, POMGR.PO_LINE.PO_HDR_ID as po_hdr_id, POMGR.VENDOR.NAME AS vendor_name, POMGR.PRODUCT_COLOR.COPY_READY_DT as copy_ready_dt, POMGR.PRODUCT_COLOR.IMAGE_READY_DT as image_ready_dt, POMGR.PRODUCT_COLOR.PRODUCTION_COMPLETE_DT, POMGR.PRODUCT_COLOR.ACTIVE, POMGR.VENDOR.THIRD_SUPPLIER_ID, POMGR.LK_PO_TYPE.NAME AS po_type, POMGR.PRODUCT_COLOR.CREATED_DATE as create_dt, POMGR.PRODUCT_COLOR.MODIFIED_DATE as modify_dt, POMGR.PRODUCT_DETAIL.MATERIAL as material, POMGR.PRODUCT_COLOR_DETAIL.SHORT_NAME as short_name, POMGR.PRODUCT_DETAIL.LONG_DESCRIPTION as description, POMGR.PRODUCT_COLOR_DETAIL.BULLET_1 as bullet1, POMGR.PRODUCT_COLOR_DETAIL.BULLET_2 as bullet2, POMGR.PRODUCT_COLOR_DETAIL.BULLET_3 as bullet3, POMGR.PRODUCT_COLOR_DETAIL.BULLET_4 as bullet4, POMGR.PRODUCT_COLOR_DETAIL.BULLET_5 as bullet5, POMGR.PRODUCT_COLOR_DETAIL.BULLET_6 as bullet6, POMGR.PRODUCT_COLOR_DETAIL.BULLET_7 as bullet7, POMGR.PRODUCT_COLOR_DETAIL.BULLET_8 as bullet8, POMGR.PRODUCT_COLOR_DETAIL.BULLET_9 as bullet9, POMGR.PRODUCT_COLOR.VERSION as version FROM POMGR.PRODUCT_COLOR RIGHT JOIN POMGR.PO_LINE ON POMGR.PO_LINE.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID RIGHT JOIN POMGR.PO_HDR ON POMGR.PO_HDR.ID = POMGR.PO_LINE.PO_HDR_ID RIGHT JOIN POMGR.VENDOR ON POMGR.VENDOR.ID = POMGR.PO_HDR.VENDOR_ID INNER JOIN POMGR.LK_PO_TYPE ON POMGR.LK_PO_TYPE.ID = POMGR.PO_HDR.PO_TYPE_ID LEFT JOIN POMGR.INVENTORY ON POMGR.INVENTORY.PRODUCT_COLOR_ID = POMGR.PRODUCT_COLOR.ID LEFT JOIN POMGR.PRODUCT_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_DETAIL.PRODUCT_ID LEFT JOIN POMGR.PRODUCT_COLOR_DETAIL ON POMGR.PRODUCT_COLOR.PRODUCT_ID = POMGR.PRODUCT_COLOR_DETAIL.PRODUCT_COLOR_ID WHERE POMGR.VENDOR.NAME LIKE '%{0}%' ORDER BY POMGR.PO_LINE.PRODUCT_COLOR_ID DESC Nulls Last, POMGR.PRODUCT_COLOR.IMAGE_READY_DT DESC Nulls Last".format(vendorname)

    result = connection.execute(querymake_vendors_product_details)
    styles = {}
    for row in result:
        style_info = {}
        style_info['vendor_name'] = row['vendor_name']
        style_info['short_name'] = row['short_name']
        style_info['version'] = row['version']
        # Convert Colorstyle to string then set as KEY
        styles[str(row['colorstyle'])] = style_info
        
    #print consigstyles
    connection.close()
    return styles


## fragrance mean color for processing levels 
def get_image_color_minmax(img):
    import subprocess, os, sys, re
    ret = subprocess.check_output([
    'convert',
    img, 
    '-median',
    '3', 
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
    #if type(directory) == 'list':
    fileslist = directory
    #elif os.path.isdir(directory):
    #    fileslist = glob.glob(os.path.join(os.path.abspath(directory), '*.??g'))

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
        except TypeError:
            filevalue_dict[f] = {'ratio_range': 'OutOfRange'}
            pass
    return filevalue_dict
        

def magick_fragrance_proc_lrg(img, rgbmean=None, destdir=None):
    import subprocess,os,re
    modulater = ''
    modulate = ''
    if not destdir:
        destdir = '.'
    ### Change to Large jpg dir to Mogrify using Glob
    os.chdir(os.path.dirname(img))
    ratio_range = rgbmean['ratio_range']
    if ratio_range != 'OutOfRange':
        high        = rgbmean['high']
        low         = rgbmean['low']
        ratio       = rgbmean['ratio']
    #rgbmean = float(128)
    #rgbmean = get_image_color_minmax(img)
    if ratio_range == 'LOW':
        if float(round(high,2)) > float(240):
            modulater = '-modulate'
            modulate = '105,100'  
        elif float(round(high,2)) > float(200):    
            modulater = '-modulate'
            modulate = '115,110'
        elif float(round(high,2)) > float(150):    
            modulater = '-modulate'
            modulate =  '120,110'    
        else:    
            modulater = '-gamma'
            modulate =  '1.4' #'120,110'    
    
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
    
    subprocess.call([
    'convert',
    '-colorspace',
    'RGB',
    img,
    '-crop',
    str(
    subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
    ,
    #'+repage',
    '-gravity',
    'center',
    '-background',
    'white',
    '-extent',
    '500x600',
    modulater,
    modulate,
    #"-auto-level",
    #"-normalize",
    "-colorspace",
    "RGB",
    "-filter",
    "Cosine",
    "-define",
    "filter:blur=0.88549061701764",
    "-distort",
    "Resize",
    '400x480',
    "-colorspace",
    "sRGB",
    '-unsharp',
    '2x2.3+0.5+0', 
    '-quality', 
    '95',
    os.path.join(destdir,img.split('/')[-1][:9] + '_l.jpg')
    ])

### Medium Jpeg conver Dir with _m jpgs
def magick_fragrance_proc_med(img, rgbmean=None, destdir=None):
    import subprocess,os,re
    modulater = ''
    modulate = ''
    
    if not destdir:
        destdir = '.'

    ### Change to Medium jpg dir to Mogrify using Glob
    os.chdir(os.path.dirname(img))
    ratio_range = rgbmean['ratio_range']
    if ratio_range != 'OutOfRange':
        high        = rgbmean['high']
        low         = rgbmean['low']
        ratio       = rgbmean['ratio']
    #rgbmean = float(128)
    #rgbmean = get_image_color_minmax(img)
    if ratio_range == 'LOW':
        if float(round(high,2)) > float(240):
            modulater = '-modulate'
            modulate = '105,100'  
        elif float(round(high,2)) > float(200):    
            modulater = '-modulate'
            modulate = '115,110'
        elif float(round(high,2)) > float(150):    
            modulater = '-gamma'
            modulate =  '1.15' #'120,110'    
        else:    
            modulater = '-gamma'
            modulate =  '1.2' #'120,110'    

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
    
        
    
    subprocess.call([
        'convert',
        '-colorspace',
        'RGB',
        img,
        '-crop',
        str(
        subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
        ,
        #'+repage',
        '-gravity',
        'center',
        '-background',
        'white',
        '-extent',
        '500x600',
        modulater,
        modulate,
        
        #"-normalize",
        "-colorspace",
        "RGB",
        "-filter",
        "Cosine",
        "-define",
        "filter:blur=0.88549061701764",
        "-distort",
        "Resize",
        '200x240',
        "-colorspace",
        "sRGB",
        '-unsharp',
        '2x2.2+0.5+0', 
        '-quality', 
        '95',
        os.path.join(destdir,img.split('/')[-1][:9] + '_m.jpg')
        ])


### Png Create with convert 
def magick_fragrance_proc_png(img, rgbmean=None, destdir=None):
    import subprocess,os,re
    modulater = ''
    modulate = ''
    if not destdir:
        destdir = '.'
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    os.chdir(os.path.dirname(img))
    ratio_range = rgbmean['ratio_range']
    if ratio_range != 'OutOfRange':
        high        = rgbmean['high']
        low         = rgbmean['low']
        ratio       = rgbmean['ratio']
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
    subprocess.call([
        'convert',
        '-format',
        format,
        img,
        '-define',
        'png:preserve-colormap',
#        '-define',
#        'png:format=png24',
#        '-define',
#        'png:compression-level=N',
#        '-define',
#        'png:compression-strategy=N',
#        '-define',
#        'png:compression-filter=N',
        '-format',
        'png',
        modulater,
        modulate,
        "-colorspace",
        "RGB",
        "-filter",
        "Spline",
        "-define",
        "filter:blur=0.88549061701764",
        '-unsharp',
        '2x2.6+0.5+0', 
        "-colorspace",
        "sRGB",
        '-quality', 
        '100',
        os.path.join(destdir,img.split('/')[-1][:9] + '.png')
        ])
    
    print 'Done {}'.format(img)
    return
    
####### END FRAGRANCENET DETOUR  FUNC DESCS############

## Move Fragrance net images to special location leaving basic processing on the remainder
walkedout_renamed_special = glob.glob(os.path.join(tmp_processing, '*.jpg'))
fragrancenet_styles = query_vendors_styles('Fragrancenet')
fragrancenet_imgs = [ f for f in walkedout_renamed_special if fragrancenet_styles.get(os.path.basename(f)[:9]) ]

## Process only fragrance net images to enhance low Rez photo then archive orig
img_dict = sort_files_by_values(fragrancenet_imgs)
for k,v in img_dict.items():
    special_img = k
    rgbmean     = v.items()
    magick_fragrance_proc_png(special_img, rgbmean=dict(rgbmean), destdir=tmp_processing_special)
    magick_fragrance_proc_lrg(special_img, rgbmean=dict(rgbmean), destdir=tmp_processing_special)
    magick_fragrance_proc_med(special_img, rgbmean=dict(rgbmean), destdir=tmp_processing_special)
    
    ## special processed original files move to archive dir making only standard processing files in proc dir
    shutil.move(special_img, os.path.join(imgdest_jpg_final, os.path.basename(special_img)))


## all process special files move to upload dir
special_processed = glob.glob(os.path.join(tmp_processing_special, '*.??g'))
[ shutil.move(file, os.path.join(tmp_loading, os.path.basename(file))) for file in special_processed ]


####
#### Detour Ends fairly uneventfully
###########   END DETOUR ###############################

## Copy Full Size Retouched Jpg to tmp Large and Med jpg folders for Glob Mogrify AND to Final Archive JPG_RETOUCHED_ORIG
walkedout_renamed_wout_special = glob.glob(os.path.join(tmp_processing, '*.jpg'))


## Large Without Special Processing needed 
[ shutil.copy2(file, os.path.join(tmp_processing_l, os.path.basename(file))) for file in walkedout_renamed_wout_special ]
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
        if sys.argv[2] == str('DEV'):
            print "Definately Not Uploaded {}".format(upload_file)
            time.sleep(float(.3))
            shutil.move(upload_file, archive_uploaded)
            pass
        elif sys.argv[2] == str('PRD'):
            
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
        
### Delete redundant PNGs in upload dir
del_extra_png = os.listdir(imgdest_png_final)
loaded_png = os.listdir(archive_uploaded)
for f in del_extra_png:
    if f in loaded_png:
        os.chdir(imgdest_png_final)
        os.remove(f)

### delete empty upload dir
del_extra_png = os.listdir(imgdest_png_final)
if len(del_extra_png) == 0:
    os.rmdir(imgdest_png_final)

## After completed Process and Load to imagedrop
###  Finally Remove the 2 tmp folder trees for process and load if Empty
upload_tmp_loading_remainder = glob.glob(os.path.join(tmp_loading, '*.*g'))
if len(upload_tmp_loading_remainder) == 0:
    shutil.rmtree(tmp_loading)

## upload_tmp_processing_png_remainder = glob.glob(os.path.join(tmp_processing, '*/*.png'))
upload_tmp_processing_jpg_remainder = glob.glob(os.path.join(tmp_processing, '*/*.jpg'))
if len(upload_tmp_processing_jpg_remainder) == 0:
    shutil.rmtree(tmp_processing)

##### Remove Lock file
#if os.path.isfile(locker):
#    os.remove(locker)
