#!/usr/bin/env python
 
def subproc_pad_to_x480(file,destdir):
    import subprocess, os
    
    fname = file.split("/")[-1].split('.')[0].replace('_LP','_l').lower()
    ext = file.split(".")[-1]
    outfile = os.path.join(destdir, fname + ".jpg")    
    
    #try:            
    subprocess.call([
        "convert", 
        file, 
        '-format', 
        'jpg',
        '-crop',
        str(subprocess.call(['convert', file, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
        ,
        '-colorspace',
        'RGB',
        '-trim', 
        '-resize',
        "x480",
        '-background',
        'white',
        '-gravity',
        'center',
#        '-trim', 
        '-extent', 
        "400x480",
#        '-trim',
#        '+repage', 
#        '-background',
#        'white',
#        '+repage',  
        '-colorspace',
        'sRGB',
        '-unsharp',
        '.7x2.8', 
        '-quality',
        '100',
        #'-strip', 
        outfile,
    ])
    #except IOError:
    #    print "Failed: {0}".format(outfile)
    return outfile


def subproc_pad_to_x1200(file,destdir):
    import subprocess, os
    
    fname = file.split("/")[-1].split('.')[0].replace('_LP','_l').lower()
    ext = file.split(".")[-1]
    outfile = os.path.join(destdir, fname + ".jpg")    
    
    #try:            
    subprocess.call([
        "convert", 
        file, 
        '-format', 
        'jpg',
        '-crop',
        str(
        subprocess.call(['convert', file, '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '1%', '-trim', '-format', '%wx%h%O', 'info:'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False))
        ,
        '-colorspace',
        'RGB',
        '-background',
        'white',
        ##'-trim',
        '+repage', 
        '-resize',
        "900x1080",
        '-gravity',
        'center',
        ##'-trim', 
        '-extent', 
        "1000x1200",
#        '+repage', 
#        '-background',
#        'white',
#        '+repage',  
        '-colorspace',
        'sRGB',
        "-unsharp",
        "2x0.5+0.5+0",
        '-quality',
        '100',
        #'-strip', 
        outfile,
    ])
    #except IOError:
    #    print "Failed: {0}".format(outfile)
    return outfile


if __name__ == '__main__':
    import sys,os
    try:
        if sys.argv[2]:
            file    = sys.argv[1]
            destdir = sys.argv[2]
            subproc_pad_to_x480(file,destdir)
    except:
        try:
            if sys.argv[1]:
                file    = sys.argv[1]
                destdir = os.path.pardir(os.path.abspath(file))
                subproc_pad_to_x480(file,destdir)
        except:
            pass

