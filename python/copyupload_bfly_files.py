#!/usr/bin/env python
# -*- coding: utf-8 -*-

def copy_to_imagedrop_upload(src_filepath, destdir=None):
    import pycurl, os, shutil, re
    regex_colorstyle = re.compile(r'^.*?[0-9]{9}[_alt0-6]{6}?\.[jpngJPNG]{3}$')
    if regex_colorstyle.findall(src_filepath):
        if not destdir:
            '/mnt/Post_Complete/ImageDrop'
        localFileName = src_filepath.split('/')[-1]

        imagedrop         = os.path.abspath(destdir)
        imagedropFilePath = os.path.join(imagedrop, localFileName.lower())
            try:
                if os.path.isfile(imagedropFilePath):
                    try:
                        os.remove(imagedropFilePath)
                        os.rename(src_filepath, imagedropFilePath)
                    except:
                        print 'Error ', imagedropFilePath
                        pass
                else:
                    os.rename(src_filepath, imagedropFilePath)
                return True
            except:
                try:
                    shutil.copy(src_filepath, imagedrop)
                    #os.remove(src_filepath)
                    return True
                except:
                    pass
                    return False
    else:
        pass


if __name__ == '__main__':
    import sys
    src_filepath = ''
    destdir      = ''
    try:
        src_filepath = sys.argv[1]
        try:
            destdir = sys.argv[2]
        except:
            pass
    except:
        print 'No Source File was Added'
        pass

    if src_filepath:
        copy_to_imagedrop_upload(src_filepath, destdir=destdir)
