#!/usr/bin/env python

import os, sys, re, csv

######################################## ##### ########################################
######################################## Order ########################################
######################################## ##### ########################################

def arg_parser_simple():
    import os,sys, urllib

    args = sys.argv[1:]

    regex_r = re.compile(r'.*?\r.*?')
    regex_n = re.compile(r'.*?\n.*?')

    args1 = args[0].split(' ') #('\n')   #(','.join(str(arg) for arg in args)).split('\n')
    return args1


def sqlQuery_styles_bypo(po_number):
    import sqlalchemy, sys
    #engine_cnx = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
    engine_cnx = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@«-vip.l3.bluefly.com:1521/bfyprd11')

    connection = engine_cnx.connect()
    #querymake_styles_bypoMySQL = "SELECT colorstyle FROM product_snapshot_live WHERE po_number like '{0}' AND image_ready_dt IS NOT NULL ORDER BY colorstyle".format(po_number)
    querymake_StylesByPO_Oracle="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PO_LINE.PO_HDR_ID = '{0}' order by POMGR.PRODUCT_COLOR.VENDOR_STYLE asc".format(po_number)

    result = connection.execute(querymake_StylesByPO_Oracle)
    
    colorstyles_list = []
    vendor_colorstyle_kv = {}
    
    for row in result:
        vendor_colorstyle_kv[row['vendor_style']] = row['colorstyle']
        colorstyles_list.append(row['colorstyle'])
    connection.close()

    return sorted(colorstyles_list), vendor_colorstyle_kv


def url_download_file(url,filepath):
    import urllib
    #error_check = urllib.urlopen(url)
    #urlcode_value = error_check.getcode()
    #print urlcode_value    
    if urllib.urlretrieve(url, filepath):
        print "Retrieved: " + url + " ---> " + filepath


def download_server_imgs(style):
    import ftplib, urllib
    netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
    colorstyle = str(style)
    ext_PNG     = '.png'
    ext_JPG     = '.jpg'

    netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext_PNG)
    colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle + ext_PNG)
    #try:
    url_download_file(netsrv101_url_file, colorstyle_file)    
    alt = 0
    imgs = []   
    for x in range(1,6):
        try:
            alt = x   
            ext_ALT = '_alt0{0}{1}'.format(str(alt),ext_PNG)
            colorstylealt = colorstyle + ext_ALT
            colorstyle_filealt = os.path.join(os.path.abspath(os.curdir), colorstylealt)
            
            netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)
            
            if urllib.urlretrieve(netsrv101_url_filealt, colorstyle_filealt) == None:
                xf = url_download_file(netsrv101_url_filealt, colorstyle_filealt)
                imgs.append(xf)
                #return True
            else:
                pass
        except IOError:
            pass
            return None
    if imgs:
        return imgs
#    except IOError:
#        pass

 
######################################## ##### ########################################
########################################  Run  ########################################
######################################## ##### ########################################

def main():
    import os,sys,shutil
    old_po = ''        
    new_po = ''
    styles_list = ''
    po_number = ''

    args = arg_parser_simple()
    args = ['135330', '135810']
    try:
        if len(args) > 2:
            styles_list = args
            print len(styles_list)
        elif len(args) == 2:
            old_po = args[0]        
            new_po = args[1]
        elif len(args) == 1:
            po_number = args[0]
            print po_number
            styles_list = sqlQuery_styles_bypo(po_number)
    except OSError:
        print "Enter at least PO Number as 1st Arg or Nothing will Happen"

    if styles_list:
        for style in styles_list:
            download_server_imgs(style)

    elif po_number:
        styles_list = sqlQuery_styles_bypo(po_number)
        for style in styles_list:
            download_server_imgs(style)

    elif new_po:
        newstyles_list, newstyles_dict = sqlQuery_styles_bypo(new_po)
        oldstyles_list, oldstyles_dict = sqlQuery_styles_bypo(old_po)
        
        #renamed_dir = os.path.join(os.path.abspath(os.path.expanduser('~')), new_po)
        #os.makedirs(renamed_dir)
                
        for k,v in oldstyles_dict.iteritems():
            oldstyle = str(oldstyles_dict.get(k))
            newstyle = str(newstyles_dict.get(k))
            print oldstyle,newstyle
            oldstylepng = oldstyle + '.png'
            newstylepng = newstyle + '.png'
            returned_files = ''
            download_server_imgs(oldstyle)
            shutil.copy(oldstylepng, newstylepng)
#
#            print returned_files
#            if returned_files:
#                for returned_file in returned_files:
#                    os.rename = (returned_file, returned_file.replace(oldstyle,newstyle))
#                    print "Renamed: " + returned_file + " ---> " + returned_file.replace(oldstyle,newstyle)
#            else:
#                try:
#                    oldstylepng = oldstyle + '.png'
#                    os.rename = (oldstylepng, oldstylepng.replace(oldstyle,newstyle))
#                    print "Renamed: " + returned_file + " ---> " + returned_file.replace(oldstyle,newstyle)
#                except TypeE:
#                    pass
#
###############################

if __name__ == '__main__': 
    main()
    #x = main()
    #print x

