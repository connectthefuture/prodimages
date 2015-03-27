#!/usr/bin/env python
import os, sys, re, csv


def url_download_file(url,filepath):
    import urllib, subprocess
    #error_check = urllib.urlopen(url)
    #urlcode_value = error_check.getcode()
    #print urlcode_value

    #if urlcode_value == 200:
    try:
        urllib.urlretrieve(url, os.path.join(filepath))
        print "Retrieved: " + url + " ---> " + filepath
        return filepath
    except:
        print  'FAILED ', url, filepath
        pass
    #    return urlcode_value
    #elif urlcode_value == 404:
    #    return urlcode_value

def get_exif_imagesize_data(image_filepath):
    import exiftool
    with exiftool.ExifTool() as et:
        try:
            mwidth = et.get_metadata(image_filepath)['File:ImageWidth']
            mheight = et.get_metadata(image_filepath)['File:ImageHeight']
            imagesize="{0}x{1}".format(mwidth,mheight)
        except KeyError:
            imagesize="NA"
    return imagesize

#### Run ###
def main(styleslist=None, root_dir=None, primary_only=None, incl_jpgs=None, verbosity=None):
    import os,sys, urllib, datetime
    todaysdate = '{:%Y%m%d}'.format(datetime.datetime.now())
    username = os.path.expanduser('~').split('/')[-1].split('.')[0].lower()
    if not root_dir:
        root_dir = os.path.join(os.path.abspath(os.path.expanduser('~')), 'Pictures', todaysdate + '_files_for_' + username )
        if not os.path.isdir(root_dir):
            try:
                os.makedirs(root_dir)
            except:
                print 'Error creating ', root_dir
                pass
    if not styleslist:
        styleslist = sys.argv[1:]
    else:
        pass
    # print 'Args ', sys.argv[0]
    regex_r = re.compile(r'.*?\r.*?')
    regex_n = re.compile(r'.*?\n.*?')
    regex_Space = re.compile(r'.*?\s.*?')
    #print styleslist

    # styleslist1 = styleslist[0].split('\n')   #(','.join(str(arg) for arg in styleslist)).split('\n')
    # try:
    #     styleslist1 = styleslist[0].split(' ')   #(','.join(str(arg) for arg in styleslist)).split('\n')
    # except KeyError:
    #     pass
    # print styleslist1
    countOne = 0
    countAlt = 0
    for style in styleslist:

        netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
        colorstyle = str(style)
        ext_PNG     = '.png'
        ext_JPG     = '_m.jpg'
        if not incl_jpgs:
            ext = ext_PNG
        elif incl_jpgs == 'l':
            ext_JPG     = '_l.jpg'
            ext = ext_JPG
            primary_only = True
        else:
            ext = ext_JPG
            primary_only = True
        netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext)
        #try:
        #error_check = urllib.urlopen(netsrv101_url_file)
        #urlcode_value = error_check.getcode()
        #print urlcode_value
        #try: #if urlcode_value == 200:
        colorstyle_file = os.path.join(root_dir, colorstyle + ext)
        print netsrv101_url_file, colorstyle_file
        try:
            url_download_file(netsrv101_url_file, colorstyle_file)
            if verbosity:
                imageSize = get_exif_imagesize_data(colorstyle_file)
                colorstyle_fileOld = os.path.join(root_dir, colorstyle + ext)
                colorstyle_fileNew = os.path.join(root_dir, colorstyle + '_' + imageSize + ext)
                try:
                    os.rename(colorstyle_fileOld, colorstyle_fileNew)
                except:
                    pass
            else:
                pass
            countOne += 1
            alt = 0
            if not primary_only:
                for x in range(1,6):
                    try:
                        alt = x
                        ext_ALT = '_alt0{0}{1}'.format(str(alt),ext)
                        colorstylealt = colorstyle + ext_ALT
                        colorstyle_filealt = os.path.join(root_dir, 'ALT', colorstylealt)

                        netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)

                        #error_check = urllib.urlopen(netsrv101_url_filealt)
                        #urlcode_value = error_check.getcode()
                        #if urlcode_value == 200:
                        colorstyle_filealt_root = os.path.join(root_dir, 'ALT')
                        if os.path.isdir(colorstyle_filealt_root):
                            pass
                        else:
                            os.makedirs(colorstyle_filealt_root)

                        if url_download_file(netsrv101_url_filealt, colorstyle_filealt):
                            url_download_file(netsrv101_url_filealt, colorstyle_filealt)
                            countAlt += 1
                    except IOError:
                        pass
            else:
                pass
        except IOError:
            pass

    perStyle = 'NA'
    countAll = countAlt + countOne
    try:
        perStyle = round((float(countAll)/float(countOne)),2)
        print '{0} Styles Found\n\t{1} Files Downloaded\n{2} Files Per Style Avg'.format(str(countOne), str(countAll), str(perStyle))
        return root_dir
    except ZeroDivisionError:
        print 'Sorry, Nothing was Found\n\n\...This time. Try Again'


if __name__ == '__main__':
    main()
