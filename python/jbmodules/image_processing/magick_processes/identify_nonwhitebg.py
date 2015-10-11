#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_images_mkdirs(filesdir):
    import os, glob
    gjpg = ''
    gpng = ''
    if os.path.isfile(filesdir):
        gjpg = [filesdir] 
        gpng = [filesdir] 
        pngout=os.path.join(os.path.dirname(filesdir),'pngnonwhitebg')
        if filesdir.split('.')[-1] == 'png':
            try:
                os.makedirs(pngout, 16877)
            except:
                pass
        jpgout=os.path.join(os.path.dirname(filesdir),'jpgnonwhitebg')
        if filesdir.split('.')[-1] == 'jpg':
            try:
                os.makedirs(jpgout, 16877)
            except:
                pass

    elif os.path.isdir(filesdir):
        gjpg = glob.glob(os.path.join(filesdir,'*.jpg'))
        gpng = glob.glob(os.path.join(filesdir,'*.png'))
        if gpng:
            pngout=os.path.join(os.path.dirname(filesdir),'pngnonwhitebg')
            try:
                os.makedirs(pngout, 16877)
            except:
                pass

        if gjpg:
            jpgout=os.path.join(os.path.dirname(filesdir),'jpgnonwhitebg')
            try:
                os.makedirs(jpgout, 16877)
            except:
                pass
    return gjpg, jpgout, gpng, pngout


def identify_grey(images_list, outdir=None):
    import subprocess, shutil, os
    ongrey = []
    for f in images_list:
        try:
            if not outdir:
                outdir = os.path.join(os.path.dirname(f), 'output')
                if os.path.isdir(outdir):
                    pass
                else:
                    try:
                        os.makedirs(outdir)
                    except OSError:
                        print 'OSError'
                        pass
        except AttributeError:
            print 'AttributeError'
            pass

        try:
            # newf = f.replace('_l','_n')
            cmd=['convert', f, '-resize', 'x480', '-virtual-pixel', 'edge', '-blur', '0x15', '-fuzz', '2%', '-bordercolor', 'white', '-border', '10x10', '-trim','-format', '%@', 'info:-']
            ret = subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=False)
            not_white = "400x480+0+0"
            oldimg = '{}'.format(ret.split('__')[-1])

            if str(oldimg) == str(not_white):
                ongrey.append(f)
                try:
                    shutil.move(f,outdir)
                except KeyError:
                    print 'KeyError'
                    pass
        except KeyError:
            print 'KeyError'
            pass
    return ongrey


def main(filesdir=None):
    import os, sys, re, glob
    from multiproc_tools import MultiprocessingModule
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    BASE_PATH = os.path.abspath(__file__)
    identify_grey_func =  identify_grey 
    if not filesdir:
        filesdir = sys.argv[1]
    
    MultiprocessingModule.run_multiproccesses_magick(searchdir=filesdir, magickProc=identify_grey_func)
    gjpg, jpgout, gpng, pngout = get_images_mkdirs(filesdir)
    
    if gjpg:
        # magickProc = identify_grey(images_list, outdir)
        ongreyjpg  = identify_grey(gjpg, jpgout)

    if gpng:
        ongreypng = identify_grey(gpng, pngout)

    return

if __name__ == '__main__':
    main()