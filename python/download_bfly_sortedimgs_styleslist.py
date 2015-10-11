#!/usr/bin/env python
import os
import sys
import re
import csv


def url_download_file(url, filepath):
    import urllib
    import subprocess
    #error_check = urllib.urlopen(url)
    #urlcode_value = error_check.getcode()
    # print urlcode_value

    # if urlcode_value == 200:
    try:
        urllib.urlretrieve(url, os.path.join(filepath))
        print "Retrieved: " + url + " ---> " + filepath
        return filepath
    except:
        print 'FAILED ', url, filepath
        pass
    #    return urlcode_value
    # elif urlcode_value == 404:
    #    return urlcode_value


#### Run ###
def main(styleslist=None, dest_dir=None, primary_only=None, out_dir_structure=None, file_format=None, recipient=None):
    import os
    import sys
    import urllib
    import datetime
    import re
    regex_r = re.compile(r'.*?\r.*?')
    regex_n = re.compile(r'.*?\n.*?')
    regex_Space = re.compile(r'.*?\s.*?')

    ## Get list from command line args or pass list as stylesList variable
    if not styleslist:
        styleslist = sys.argv[1:]

    ## Define the root dest_dir or redefine using current dest_dir as the root
    todaysdate = '{:%Y%m%d}'.format(datetime.datetime.now())
    if not dest_dir:
        username = os.path.expanduser('~').split('/')[-1].split('.')[0].lower()
        dest_dir = os.path.join(os.path.abspath(os.path.expanduser('~')), 'Pictures', todaysdate + '_BflyImgExport_' + username)
    else:
        if recipient:
            dest_dir = os.path.join(dest_dir, todaysdate + '_BflyImgExport_' + recipient)
        else:
            dest_dir = os.path.join(dest_dir, todaysdate + '_BflyImgExport')

    ## Now make the destination root dir if not exists
    dest_dir_root = os.path.abspath(dest_dir)
    if os.path.isdir(dest_dir_root):
        pass
    else:
        os.makedirs(dest_dir_root)

    # Define the output directory structure of the downloaded files
    if not out_dir_structure:
        out_dir_structure = 'groupByStyle'
    elif out_dir_structure == 'allSeparateAlt':
        out_dir_structure = 'allSeparateAlt'
    else:
        pass

    countOne = 0
    countAlt = 0
    for style in styleslist:
        netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
        colorstyle = str(style)
        dest_dir = dest_dir_root
        if not file_format:
            ext = '.png'
        else:
            ext = '.' + file_format.lower().lstrip('.')

        ## 1 Change the dest dir then create it if necessary for this file based on out_dir_structure parameter
        if out_dir_structure == 'groupByStyle':
            dest_dir = os.path.join(dest_dir, colorstyle)
            dest_dir_style = dest_dir
        ## Create the dest dir if not exists
        if os.path.isdir(dest_dir):
            pass
        else:
            os.makedirs(dest_dir)

        netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext)
        colorstyle_file = os.path.join(dest_dir, colorstyle + ext)
        print netsrv101_url_file, colorstyle_file
        try:
            url_download_file(netsrv101_url_file, colorstyle_file)
            countOne += 1
            alt = 0
            if not primary_only:
                for x in range(1, 6):
                    if out_dir_structure == 'groupByStyle':
                        dest_dir = dest_dir_style
                    else:
                        dest_dir = dest_dir_root
                    try:
                        alt = x
                        ext_ALT = '_alt0{0}{1}'.format(str(alt), ext)
                        colorstylealt = colorstyle + ext_ALT
                        netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)

                        ## 2 Redefine the dest dir if separating ALT
                        ##  then create it if necessary for this file based on out_dir_structure parameter
                        if out_dir_structure == 'allSeparateAlt':
                            dest_dir = os.path.join(dest_dir, 'ALT')
                            if os.path.isdir(dest_dir):
                                pass
                            else:
                                os.makedirs(dest_dir)
                        else:
                            pass

                        ## Try and download all alts 01-06 if any exist on server
                        colorstyle_filealt = os.path.join(dest_dir, colorstylealt)
                        if url_download_file(netsrv101_url_filealt, colorstyle_filealt):
                            url_download_file(netsrv101_url_filealt, colorstyle_filealt)
                            countAlt += 1
                        else: 
                            pass

                    except IOError:
                        pass
            else:
                pass
        except IOError:
            pass

    perStyle = 'NA'
    countAll = countAlt + countOne
    try:
        perStyle = round((float(countAll) / float(countOne)), 2)
        print '{0} Styles Found\n\t{1} Files Downloaded\n{2} Files Per Style Avg'.format(str(countOne), str(countAll), str(perStyle))
        return dest_dir_root
    except ZeroDivisionError:
        print 'Sorry, Nothing was Found\n\n\...This time. Try Again'


if __name__ == '__main__':
    main()
