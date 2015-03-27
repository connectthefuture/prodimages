#!/usr/bin/env python

def subproc_multithumbs_8_4_2(filepath,destdir,eight=None):
    import subprocess, os
    
    fname = filepath.split("/")[-1].split('.')[0].lower().replace('_1.','.')
    ext = filepath.split(".")[-1]
    
    if eight:
        outfile_z = os.path.join(destdir, fname + "_z.jpg")    
    outfile_l = os.path.join(destdir, fname + "_l.jpg")    
    outfile_m = os.path.join(destdir, fname + "_m.jpg")

    subprocess.call([
        'convert', 
        filepath, 
        '-format', 
        ext,
        '-write',
        'mpr:copy-of-original',
        '+delete',
            ## Begin generating imgs 
            # --> Large Jpeg
            'mpr:copy-of-original',
            '-format', 
            'jpg',
            'compress', 
            'none',
            '-resize',
            '400x480',
            'compress', 
            'none', 
            '-unsharp',
            '2x0.5+0.5+0', 
            '-quality', 
            '100',
            '-write',
            outfile_l,
            '+delete',
            
            ## Medium Jpeg
            'mpr:copy-of-original',
            '-format', 
            'jpg',
            'compress', 
            'none', 
            '-resize',
            '200x240',
            '-unsharp',
            '2x0.5+0.5+0', 
            '-quality', 
            '100',
            '-write',
            outfile_m,
            '+delete',
            ])
            
            ##'mpr:copy-of-huge-original-crop"3000x2000+0+480"-resize"200x125!>"-writethumb1-extract.jpg+delete',
            #'mpr:copy-of-huge-original-crop"2000x1500+280+220"-resize"75x75!>"-writethumb2-extract.jpg+delete',
            #
                
                ## Eight --> Zoom Largest Jpeg
    #            'mpr:copy-of-original',
    #            '-format', 
    #            'jpg',
    #             #'-colorspace',
    #             #'sRGB',
    #            '-channel', 
    #            'RGBA',
    #            '-resize',
    #            '800x960',
    #            #'compress', 
    #            #'none', 
    #            '-unsharp',
    #            '2x0.5+0.5+0', 
    #            '-quality', 
    #            '100',
    #            '-write',
    #            outfile_z,
    #            '+delete',
               
        #str('mpr:copy-of-huge-original-resize"1000x1200"-writesample-1000x1200_z.jpg+delete'),
        #str('mpr:copy-of-huge-original-resize"800x960"-writesample-800x960_x.jpg+delete'),
        #str('mpr:copy-of-huge-original-resize"400x480"-writesample-400x480_l.jpg+delete'),
        #str('mpr:copy-of-huge-original '-resize', '"200x240"','-writesample','-200x240_m.jpg+delete'),
        ##'mpr:copy-of-huge-original-resize"163x163!>"-writesample-163x163.jpg'
        #])
        
import sys,os, datetime, glob
todaysdirdate = datetime.datetime.strftime(str(datetime.datetime.now(), '%Y-%m-%d_%f' ))

originaldir = os.path.abspath(sys.argv[1])
os.chdir(originaldir)
listeddir = os.listdir(originaldir)

destdir = ''
try:
    destdir = os.path.abspath(sys.argv[2])
except IndexError:
    destdir = os.path.join(originaldir, 'converteddir_' + todaysdirdate)

if not os.path.isdir(destdir):
    try:
        os.makedirs(destdir)
    except:
        print "Failed {}".format(destdir)
        pass

print destdir        
for filepath in listeddir:
    subproc_multithumbs_8_4_2(os.path.abspath(filepath),destdir)

allfiles_list = []
converteddir = glob.glob(os.path.join(destdir, '*[0-9]???????[0-9]_[lmz].jpg'))
pngs_in_originaldir = glob.glob(os.path.join(originaldir, '*[0-9]???????[0-9].png'))

for f in converteddir:
    allfiles_list.append(os.path.abspath(f))

for f in pngs_in_originaldir:
    allfiles_list.append(os.path.abspath(f))


print sorted(allfiles_list)