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
    regex_border_clr   = re.compile(r'.*?Bordercolor.*?$')
    regex_colorspace  = re.compile(r'.*?Colorspace.*?$')
    
    metadata=subprocess.check_output(['identify', 
                                       '-verbose', 
                                        inputfile
                                        ])
            
    metadata_list = metadata.replace(' ','').split('\n')
    
    g_width = [ g.split(':')[-1].split('+')[0].split('x')[0] for g in metadata_list if regex_geometry.findall(g) ]
    g_height = [ g.split(':')[-1].split('+')[0].split('x')[1] for g in metadata_list if regex_geometry.findall(g) ]
    
    metadata_width    = float(g_width[0])
    metadata_height   = float(g_height[0])
    
    dominantclr_list = subprocess.check_output(['convert', 
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
    borderclr = [ borderclr.split(':')[-1] for borderclr in dominantclr_list if regex_border_clr.findall(borderclr) ]
    colorspace = [ colorspace.split(':')[-1] for colorspace in dominantclr_list if regex_colorspace.findall(colorspace) ]
    
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
    fileinfo['borderclr'] = borderclr
    fileinfo['colorspace'] = colorspace
    metadict[inputfile] = fileinfo
    return metadict
    
####### RUN
if __name__ == "__main__":
    import sys
    metadata = metadata_info_dict(sys.argv[1])
    print metadata
    