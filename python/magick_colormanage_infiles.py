#!/usr/local/env python
# -*- unicode-8 -*-
#=/Users/johnb/Downloads/bella42413/bellaapendix/one/324264801/324264801_1.jpg
import os,sys,re,subprocess,glob

## CMYK Profile Files
cmyk_uswebcoat='/usr/local/color_profiles/standard/USWebCoatedSWOP.icc'
cmyk_ussheetfedcoat='/usr/local/color_profiles/standard/USSheetfedCoated.icc'
cmyk_jpn01coat='/usr/local/color_profiles/standard/JapanColor2001Coated.icc'
cmyk_FOGRA39coat='/usr/local/color_profiles/standard/CoatedFOGRA39.icc'
cmyk_FOGRA27coat='/usr/local/color_profiles/standard/CoatedFOGRA27.icc'

## RGB Profile Files
adobe98='/usr/local/color_profiles/standard/AdobeRGB1998.icc'
srgb_webrdy='/usr/local/color_profiles/standard/sRGB.icm'


def metadata_info_dict(inputfile):
    import os,sys,re,subprocess,glob
    regex_geometry = re.compile(r'^Geometry.+?$')
    metadict = {}
    fileinfo = {}
    fname=os.path.basename(inputfile)
    dname=os.path.dirname(inputfile)
    regex_geometry_attb = re.compile(r'.*?Geometry.*?[0-9,{1,4}]x[0-9,{1,4}].*?$')
    regex_mean   = re.compile(r'.*?mean.*?$')
    regex_colorspace  = re.compile(r'.*?Colorspace.*?$')
    regex_mean  = re.compile(r'.*?Mean.*?$')

    metadata=subprocess.check_output(['identify', 
                                       '-verbose', 
                                        inputfile
                                        ])
            
    metadata_list = metadata.replace(' ','').split('\n')
    
    g_width = [ g.split(':')[-1].split('+')[0].split('x')[0] for g in metadata_list if regex_geometry.findall(g) ]
    g_height = [ g.split(':')[-1].split('+')[0].split('x')[1] for g in metadata_list if regex_geometry.findall(g) ]
    
    metadata_width    = float(g_width[0])
    metadata_height   = float(g_height[0])
    
    dominantclr_list = subprocess.call(['convert', 
                                                inputfile, 
                                                '-posterize',
                                                '3',
                                                '-define',
                                                'histogram:unique-colors=true',
                                                '-format',
                                                '"%c"',
                                                'histogram:info:-'
                                                ])
                    
    dominantclr_list = metadata.replace(' ','').split('\n')
    mean_tot = sorted(dominantclr_list[0].split(' ')[0])#[ borderclr.split(':')[-1][:] for borderclr in dominantclr_list if regex_border_clr.findall(borderclr) ]
    colorspace = [ colorspace.split(':')[-1][:] for colorspace in dominantclr_list if regex_colorspace.findall(colorspace) ]
    print dominantclr_list
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
    metadict[inputfile] = fileinfo
    return metadict


## Image Processing Funx
def subproc_magick_large_jpg(img):
    import subprocess,os,re

    ### Change to Large jpg dir to Mogrify using Glob
    os.chdir(os.path.dirname(img))
    
    # Get avg color intensity then adjust per group
    rgbmean = float(128)
    if float(round(rgbmean,2)) > float(230):
        modval = '90,110'     
    elif float(round(rgbmean,2)) > float(200):    
        modval = '110,100' 
    elif float(round(rgbmean,2)) > float(150):
        modval = '120,105'     
    else: 
        modval = '130,105'

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
    '-extent',
    '500x600',
    '-modulate',
    modval,
    #"-auto-level",
    #"-normalize", 
    '-unsharp',
    '2.0x1.7+0.5+0.0', 
    '-quality', 
    '95',
    os.path.join('.',img.split('/')[-1])
    ])

### Medium Jpeg Mogrfy Dir with _m jpgs
def subproc_magick_medium_jpg(img):
    import subprocess,os,re

    ### Change to Medium jpg dir to Mogrify using Glob
    os.chdir(os.path.dirname(img))
    
    # Get avg color intensity then adjust per group
    rgbmean = float(128)
    if float(round(rgbmean,2)) > float(230):
        modval = '90,110',     
    elif float(round(rgbmean,2)) > float(200):    
        modval = '110,100',
    elif float(round(rgbmean,2)) > float(150):    
        modval = '120,105',
    else:    
        modval = '130,105',

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
    '-extent',
    '500x600',  
    '-modulate',
    modval,
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
    
    rgbmean = float(128)
    if float(round(rgbmean,2)) > float(230):
        modval = '90,110',     
    elif float(round(rgbmean,2)) > float(200):    
        modval = '110,100',
    elif float(round(rgbmean,2)) > float(150):    
        modval = '120,105',
    else:    
        modval = '130,105',
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
    modval,
    '-quality',
    '100',
    '-colorspace',
    'sRGB',
    '-unsharp',
    '2x1.7+0.5+0', 
    '-quality', 
    '95',
    os.path.join('.',img.split('/')[-1])
    ])
    
    print 'Done {}'.format(img)
    return
####### RUN
if __name__ == "__main__":
    import sys
    metadata = metadata_info_dict(sys.argv[1])
    print metadata
    