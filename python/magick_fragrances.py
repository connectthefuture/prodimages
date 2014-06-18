#/usr/bin/env python
### Large Jpeg Mogrfy Dir with _l jpgs
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

def subproc_magick_large_jpg(img):
    import subprocess,os,re

    ### Change to Large jpg dir to Mogrify using Glob
    os.chdir(os.path.dirname(img))
    rgbmean = get_image_color_minmax(img)
    
    if float(round(rgbmean,2)) > float(230):
        modulate = '90,110'  
    elif float(round(rgbmean,2)) > float(200):    
        modulate = '110,100'
    elif float(round(rgbmean,2)) > float(150):    
        modulate = '120,105'    
    else:    
        modulate =' 130,105'
    
    subprocess.call([
    'convert',
    '-colorspace',
    'RGB',
    img,
    '-crop',
    str(
    subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
    ,
    '+repage',
    '-gravity',
    'center',
    '-background',
    'white',
    #'-extent',
    #'500x600',
    '-modulate',
    modulate,
    #"-auto-level",
    #"-normalize", 
    #'-unsharp',
    #'2.0x1.7+0.5+0.0', 
    '-quality', 
    '95',
    os.path.join('.',img.split('/')[-1])
    ])

### Medium Jpeg Mogrfy Dir with _m jpgs
def subproc_magick_medium_jpg(img):
    import subprocess,os,re

    ### Change to Medium jpg dir to Mogrify using Glob
    os.chdir(os.path.dirname(img))
    rgbmean = get_image_color_minmax(img)
    
    if float(round(rgbmean,2)) > float(230):
        modulate = '90,110'  
    elif float(round(rgbmean,2)) > float(200):    
        modulate = '110,100'
    elif float(round(rgbmean,2)) > float(150):    
        modulate = '120,105'    
    else:    
        modulate =' 130,105'
    
    subprocess.call([
        'convert',
        '-colorspace',
        'RGB',
        img,
        '-crop',
        str(
        subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
        ,
        '+repage',
        '-gravity',
        'center',
        '-background',
        'white',
        #'-extent',
        #'500x600',
        '-modulate',
        modulate,
        #"-auto-level",
        #"-normalize", 
        '-unsharp',
        '2.0x1.7+0.5+0.0', 
        '-quality', 
        '95',
        os.path.join('.',img.split('/')[-1])
        ])


### Png Create with Mogrify globbing png directories
def subproc_magick_png(img):
    import subprocess,re,os
    #imgdestpng_out = os.path.join(tmp_processing, os.path.basename(imgsrc_jpg))
    os.chdir(os.path.dirname(img))
    
    #rgbmean = float(128)
    rgbmean = get_image_color_minmax(img)
    
    if float(round(rgbmean,2)) > float(230):
        modulate = '90,110'  
    elif float(round(rgbmean,2)) > float(200):    
        modulate = '110,100'
    elif float(round(rgbmean,2)) > float(150):    
        modulate = '120,105'    
    else:    
        modulate =' 130,105'
    
    subprocess.call([
        'convert',
        '-format',
        'png',
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
#root_img_dir = '/Users/JCut/Dropbox/DEVROOT/DROP/testfragrancecopy/newsettest/312467701.png'
if os.path.isdir(root_img_dir):
    for img in glob.glob(os.path.join(root_img_dir,'*.??g')):
        subproc_magick_large_jpg(img)
        subproc_magick_medium_jpg(img)
        subproc_magick_png(img)
else:
    img = root_img_dir
    test_img = get_image_color_minmax(img)
    print test_img