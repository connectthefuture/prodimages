timeconvert\
very-very-large.png\
-quality85\
-writempr:mpc:label\
+delete\
mpr:mpc:label-crop'3000x2001+0+491'-resize'170x116!>'-writepic1.png+delete\
mpr:mpc:label-crop'2981x2883+8+0'-resize'75x75!>'-writepic2.png+delete\
mpr:mpc:label-crop'1100x1983+0+0'-resize'160x160!>'-writepic3.png+delete\
mpr:mpc:label-crop'2000x2883+0+0'-resize'1024x960!>'-writepic4.png+delete\
mpr:mpc:label-crop'1000x2883+0+0'-resize'190x188!>'-writepic5.png+delete\
mpr:mpc:label-crop'3000x2000+0+0'-resize'2048x2047!>'-writepic6.png+delete\
mpr:mpc:label-crop'3000x2883+0+0'-resize'595x421!>'-writepic7.png+delete\
mpr:mpc:label-crop'3000x2883+0+0'-resize'3000x2883!>'-writepic8.png

'-crop',
str(subprocess.call(['convert', file, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
,
'-colorspace',
'RGB',
'-trim', 
'-resize',
rocess.call([


def subproc_pad_to_x480(file,destdir):
    import subprocess, os
    
    fname = file.split("/")[-1].split('.')[0].replace('_LP','_l').lower()
    ext = file.split(".")[-1]
    outfile = os.path.join(destdir, fname + ".jpg")    
    
    #try:            
    subprocess.call([
        "convert", 
        infile, 
        '-format', 
        'png',
        '-quality',
        '85',
        '-colorspace',
        'rgb',
        '+profile"*"',
        '-filter',
        'Lanczos',
        '-writempr:copy-of-huge-original',
        '+delete',
        ##'mpr:copy-of-huge-original-crop"3000x2000+0+480"-resize"200x125!>"-writethumb1-extract.jpg+delete',
        #'mpr:copy-of-huge-original-crop"2000x1500+280+220"-resize"75x75!>"-writethumb2-extract.jpg+delete',
        str('mpr:copy-of-huge-original',
            '-resize',
            '"1000x1200"',
            '-writesample-1000x1200_z.jpg',
            '+delete'),
        
        str('mpr:copy-of-huge-original',
            '-resize',
            '"1000x1200"',
            '-writesample-1000x1200_z.jpg',
            '+delete'),
        #str('mpr:copy-of-huge-original-resize"1000x1200"-writesample-1000x1200_z.jpg+delete'),
        #str('mpr:copy-of-huge-original-resize"800x960"-writesample-800x960_x.jpg+delete'),
        #str('mpr:copy-of-huge-original-resize"400x480"-writesample-400x480_l.jpg+delete'),
        #str('mpr:copy-of-huge-original '-resize', '"200x240"','-writesample','-200x240_m.jpg+delete'),
        ##'mpr:copy-of-huge-original-resize"163x163!>"-writesample-163x163.jpg'
        ])