#/usr/bin/env python
### Large Jpeg Mogrfy Dir with _l jpgs
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
        except ZeroDivisionError:
            filevalue_dict[f] = {'ratio_range': 'OutOfRange'}
            pass
    return filevalue_dict

### Png Create with Mogrify globbing png directories
def subproc_magick_png(img, rgbmean=None, destdir=None):
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
            modulate = '104,100'  
        elif float(round(high,2)) > float(200):    
            modulater = '-modulate'
            modulate = '107,110'
        elif float(round(high,2)) > float(150):    
            modulater = '-modulate'
            modulate =  '110,110'    
        else:    
            modulater = '-modulate'
            modulate =  '112,110' 

    elif ratio_range == 'HIGH':
        if float(round(high,2)) > float(230):
            modulater = '-modulate'
            modulate = '100,100'  
        elif float(round(high,2)) > float(200):    
            modulater = '-modulate'
            modulate = '103,100'
        elif float(round(high,2)) > float(150):    
            modulater = '-modulate'
            modulate = '105,105'     
        else:    
            modulater = '-modulate'
            modulate =  '108,107'  
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
        '-define',
        'png:format=png24',
        '-define',
        'png:compression-level=N',
        '-define',
        'png:compression-strategy=N',
        '-define',
        'png:compression-filter=N',
        '-format',
        'png',
        '-modulate',
        modulate,
        '-quality',
        '100',
        '-colorspace',
        'sRGB',
        #'-unsharp',
        #'2x1.7+0.5+0', 
        '-quality', 
        '95',
        os.path.join('.',img.split('/')[-1])
        ])
    
    print 'Done {}'.format(img)
    return

import sys,glob,shutil,os
root_img_dir = os.path.abspath(sys.argv[1])
##root_img_dir = '/Users/JCut/Dropbox/DEVROOT/DROP/testfragrancecopy/newsettest/312467701.png'
#if os.path.isdir(root_img_dir):
#    for img in glob.glob(os.path.join(root_img_dir,'*.??g')):
#        #subproc_magick_large_jpg(img)
#        #subproc_magick_medium_jpg(img)
#        subproc_magick_png(img)
#else:
#    img = root_img_dir
#    test_img = get_image_color_minmax(img)
#    print test_img
#    
    

imgs = [ f for f in glob.glob(os.path.join(root_img_dir, '*.??g')) ]
#walkedout_renamed_special = glob.glob(os.path.join(tmp_processing, '*.jpg'))
#fragrancenet_styles = query_vendors_styles('Fragrancenet')
#imgsfrag = [ f for f in imgs if fragrancenet_styles.get(os.path.basename(f)[:9]) ]

## Process only fragrance net images to enhance low Rez photo then archive orig
img_dict = sort_files_by_values(imgs)
for k,v in img_dict.items():
    img = k
    rgbmean     = v.items()
    subproc_magick_png(img, rgbmean=dict(rgbmean), destdir=root_img_dir)
    #magick_fragrance_proc_lrg(special_img, rgbmean=dict(rgbmean), destdir=tmp_processing_special)
    #magick_fragrance_proc_med(special_img, rgbmean=dict(rgbmean), destdir=tmp_processing_special)
    
    ## special processed original files move to archive dir making only standard processing files in proc dir
    #shutil.move(special_img, os.path.join(imgdest_jpg_final, os.path.basename(special_img)))


## all process special files move to upload dir
#special_processed = glob.glob(os.path.join(tmp_processing_special, '*.??g'))
#[ shutil.move(file, os.path.join(tmp_loading, os.path.basename(file))) for file in special_processed ]
