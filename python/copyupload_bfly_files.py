#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This one move the file while the other copies it and leave an original, moving is better usually
def copy_to_imagedrop_upload(src_filepath, destdir=None):
    import pycurl, os, shutil, re
    regex_colorstyle = re.compile(r'^.*?/[0-9]{9}[_altm0-6]{,6}?\.[jpngJPNG]{3}$')
    if not regex_colorstyle.findall(src_filepath):
        print src_filepath.split('/')[-1], ' Is Not a valid Bluefly Colorstyle File or Alt Out of Range'
        return
    else:
        if not destdir:
            destdir = '/mnt/Post_Complete/ImageDrop'
        imagedrop         = os.path.abspath(destdir)
        localFileName     = src_filepath.split('/')[-1]
        imagedropFilePath = os.path.join(imagedrop, localFileName.lower())
        try:
            if os.path.isfile(imagedropFilePath):
                try:
                    os.remove(imagedropFilePath)
                    os.rename(src_filepath, imagedropFilePath)
                    return True
                except:
                    print 'Error ', imagedropFilePath
                    return False
            else:
                os.rename(src_filepath, imagedropFilePath)
                return True
        except:
            try:
                shutil.copy(src_filepath, imagedrop)
                #os.remove(src_filepath)
                return True
            except:
                print 'Error ', imagedropFilePath
                return False


def copy_to_imagedrop_uploadV2KeepOrig(src_filepath, destdir=None):
    import pycurl, os, shutil, re
    regex_colorstyle = re.compile(r'^.*?/[0-9]{9}[_altm0-6]{,6}?\.[jpngJPNG]{3}$')
    if not regex_colorstyle.findall(src_filepath):
        print src_filepath.split('/')[-1], ' Is Not a valid Bluefly Colorstyle File or Alt Out of Range'
        return
    else:
        if not destdir:
            destdir = '/mnt/Post_Complete/ImageDrop'
        imagedrop         = os.path.abspath(destdir)
        localFileName     = src_filepath.split('/')[-1]
        imagedropFilePath = os.path.join(imagedrop, localFileName.lower())
        try:
            if os.path.isfile(imagedropFilePath):
                try:
                    os.remove(imagedropFilePath)
                    shutil.copyfile(src_filepath, imagedropFilePath)
                    return True
                except:
                    print 'Error ', imagedropFilePath
                    return False
            else:
                shutil.copyfile(src_filepath, imagedropFilePath)
                return True
        except:
            return False


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
