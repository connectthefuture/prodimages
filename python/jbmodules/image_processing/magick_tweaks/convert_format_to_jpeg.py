#!/usr/bin/env python
# -*- coding: utf-8 -*-


def magickConvert_to_jpeg(img,destdir=None):
    import subprocess
    ext = img.split('.')[-1]
    if not destdir:
        outfile = img.split('/')[-1].split('.')[0] + ".jpg"
    else:
        outfile = destdir
    subprocess.call([
        'convert',
        '-colorspace',
        'RGB',
        "-format",
        ext,
        img,
        "-depth",
        "16",
        "-density",
        "72x72",
        # "-profile",
        # "/usr/local/color_profiles/AdobeRGB1998.icc",
        # "-colorspace",
        # "RGB",
        "-filter",
        "LanczosSharp",
        "-compress",
        "JPEG",
        # "-profile",
        # '/usr/local/color_profiles/sRGB.icm',
        "-colorspace",
        'sRGB',
        "-depth",
        "8",
        "-format",
        "jpeg",
        "-strip",
        '-quality',
        '95',
        outfile
        ])
    return outfile


if __name__ == '__main__':
    import sys
    res = magickConvert_to_jpeg(sys.argv[1])
    print res
