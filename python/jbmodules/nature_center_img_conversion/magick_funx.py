#!/usr/bin/env python
# -*- coding: utf-8 -*-



## Create BG image to Composite Primary over inorder to pad BC cutoffs on List page
# def pad_image_to_x480(file):
# from PythonMagick import Image, CompositeOperator
#     fname = file.split(".")[0]
#     ext = file.split(".")[-1]
#     outfile = os.path.join(destdir, fname + "_" + "l" + ".jpg")
#
#     ## Make BG layer
#     bgimg = Image('400x480', 'white')
#
#     ## Open Primary image
#     img = Image(file)
#     img.backgroundColor("white")
#     img.sample('350x432')
#
#     # Composite + Save Primary over bg, padding primary with white of bg
#     type = img.type
#     img.composite(bgimg, 0, 0, CompositeOperator.DstOverCompositeOp)
#     img.magick('JPG')
#     img.type = type
#     img.quality(100)
#     img.write(outfile)


def subproc_pad_to_x480(fpath, destdir):
    import subprocess, os

    fname = fpath.split(".")[0]
    ext = fpath.split(".")[-1]
    if not destdir:
        destdir = os.path.dirname(fpath)
    outfile = os.path.join(destdir, fname + "_" + "l" + ".jpg")

    try:

        subprocess.call([
            "convert",
            fpath,
            "-format",
            ext,
            "-resize",
            "350x432",
            "-background",
            "white",
            "-gravity",
            "center",
            "-extent",
            "400x480",
            "-format",
            "jpg",
            "-quality",
            "100",
            outfile
        ])

    except:
        print "Failed: {0}".format(fpath)
    return outfile



def main(dirname=None):
    import os.path
    dirname = os.path.abspath(dirname)
    destdir = os.path.join(os.path.join(dirname, '../../outfile'))
    if dirname: pass

