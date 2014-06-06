#/usr/bin/env python

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
def metadata_info_dict(inputfile):
    import os,sys,re,subprocess,glob
    regex_geometry = re.compile(r'^Geometry.+?$')
    metadict = {}
    fileinfo = {}
    fname=os.path.basename(inputfile)
    dname=os.path.dirname(inputfile)
    regex_geometry_attb = re.compile(r'.*?Geometry.*?[0-9,{1,4}]x[0-9,{1,4}].*?$')
    
    metadata=subprocess.check_output(['identify', '-verbose', inputfile])

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
    #fileinfo['mean'] = mean_tot[0]
    #fileinfo['colorspace'] = colorspace[0]
    metadict[inputfile] = fileinfo
    return metadict


# return image demensions and vert_hoiz variables only
def get_image_dimensions(img):
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
    if int(dimensions.split('x')[1]) <= int(dimensions.split('x')[-1]):
        if int(dimensions.split('x')[1]) < 2000:
            vert_horiz = "x2400"
            dimensions = "2000x2400"
        elif int(dimensions.split('x')[1]) < 2000 and int(dimensions.split('x')[1]) > 1400:
            vert_horiz = "x1680"
            dimensions = "1400x1680"
        elif int(dimensions.split('x')[1]) < 1400 and int(dimensions.split('x')[1]) > 1000:
            vert_horiz = "x1200"
            dimensions = "1000x1200"
        elif int(dimensions.split('x')[1]) < 1000 and int(dimensions.split('x')[1]) > 600:
            vert_horiz = "x720"
            dimensions = "600x720"
        else:
            vert_horiz = "x480"
            dimensions = "400x480"
    
    ## Landscape Orientation for wider images  
    elif int(dimensions.split('x')[1]) > int(dimensions.split('x')[-1]):
        if int(dimensions.split('x')[-1]) < 2400:
            vert_horiz = "2000x"
            dimensions = "2000x2400"

        elif int(dimensions.split('x')[-1]) < 2400 and int(dimensions.split('x')[-1]) > 1680:
            vert_horiz = "1400x"
            dimensions = "1400x1680"
        
        elif int(dimensions.split('x')[-1]) < 1680 and int(dimensions.split('x')[-1]) > 1200:
            vert_horiz = "1000x"
            dimensions = "1000x1200"

        elif int(dimensions.split('x')[-1]) < 1200 and int(dimensions.split('x')[-1]) > 720:
            vert_horiz = "600x"
            dimensions = "600x720"
        else:
            vert_horiz = "400x"
            dimensions = "400x480"
    return vert_horiz, dimensions

#
### End Data extract Funx, below processors
#

### Large Jpeg Convert to  _l jpgs
def subproc_magick_large_jpg(img, destdir=None):
    import subprocess,os,re

    os.chdir(os.path.dirname(img))
    
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)
        
    dimensions = ''
    ## Get variable values for processing
    vert_horiz, dimensions = get_image_dimensions(img)

    if not dimensions:
        vert_horiz = 'x480'
        dimensions = "400x480"
    
    subprocess.call([
    'convert',
    '-colorspace',
    'RGB',
    img,
    '-crop',
    str(
    subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
    ,
    '-trim', 
    "-filter",
    "Cosine",
    "-define",
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
    '2x2.3+0.5+0', 
    '-quality', 
    '95',
    os.path.join(destdir, img.split('/')[-1])
    #os.path.join(destdir, img.split('/')[-1][:9] + '_l.jpg')
    ])


### Medium Jpeg Convert to  _l jpgs
def subproc_magick_medium_jpg(img, destdir=None):
    import subprocess,os,re

    os.chdir(os.path.dirname(img))
    #rgbmean = get_image_color_minmax(img)
    
    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    dimensions = ''
    ## Get variable values for processing
    vert_horiz, dimensions = get_image_dimensions(img)

    if not dimensions:
        vert_horiz = 'x360'
        dimensions = "300x360"
    
    subprocess.call([
        'convert',
        '-colorspace',
        'RGB',
        img,
        '-crop',
        str(
        subprocess.call(['convert', img, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:-'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
        ,
        #+repage
        '-trim', 
        "-filter",
        "Cosine",
        "-define",
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
        '2x2.2+0.5+0', 
        '-quality', 
        '95',
        os.path.join(destdir, img.split('/')[-1])
        #os.path.join(destdir, img.split('/')[-1][:9] + '_m.jpg')
        ])


### Png Create with Convert and aspect 
def subproc_magick_png(img, destdir=None):
    import subprocess,re,os

    if not destdir:
        destdir = os.path.abspath('.')
    else:
        destdir = os.path.abspath(destdir)

    dimensions = ''
    ## Get variable values for processing
    vert_horiz, dimensions = get_image_dimensions(img)

    if not dimensions:
        dimensions = '100%'
        vert_horiz = '100%'

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
        '-define',
        'png:compression-level=N',
        '-define',
        'png:compression-strategy=N',
        '-define',
        'png:compression-filter=N',
        "-filter",
        "Spline",
        "-define",
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
        '2x2.4+0.5+0', 
        '-quality', 
        '100',
        os.path.join(destdir, img.split('/')[-1])
        ])
    
    print 'Done {}'.format(img)
    return


import sys,glob,shutil,os
#root_img_dir = os.path.abspath(sys.argv[1])
root_img_dir = '/Users/johnb/Dropbox/DEVROOT/DROP/testfragrancecopy/newsettest/312467701.png'
destdir = '/Users/johnb/Pictures'

if os.path.isdir(root_img_dir):
    for img in glob.glob(os.path.join(root_img_dir,'*.??g')):
        subproc_magick_large_jpg(img, destdir=destdir)
        #subproc_magick_medium_jpg(imgdir)
        #subproc_magick_png(root_img_dir)
else:
    img = root_img_dir
    
    subproc_magick_large_jpg(img, destdir=destdir)
    subproc_magick_medium_jpg(img, destdir=destdir)
    subproc_magick_png(img, destdir=destdir)
    metadict = metadata_info_dict(img)
    dimens = get_image_dimensions(img)
    test_img = get_image_color_minmax(img)
    