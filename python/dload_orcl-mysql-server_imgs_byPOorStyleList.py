#!/usr/bin/env python

import os, sys, re, csv





def readxl_outputdict(workbk=None):         
    import csv,xlrd,sys
    #workbk = sys.argv[1]
    book = xlrd.open_workbook(workbk)##sys.argv[1])
    sh = book.sheet_by_index(0)

    #convWriter = csv.writer(sys.stdout,delimiter=',', dialect='excel')
    numcols=sh.ncols
    outdict = {}
    for rx in xrange(sh.nrows):
        rowdict = {}    
        for cx in xrange(sh.ncols):
            rowhead = sh.cell_value(rowx=0,colx=cx)
            rowval = sh.cell_value(rowx=rx,colx=cx)
            rowdict[rowhead] = rowval
            outdict[rx] = rowdict
    return outdict

def compile_outdict_by_rowkeys(outdict):
    from collections import defaultdict
    d = defaultdict(list)
    for r in outdict.items():
        dd = defaultdict(dict)
        for val in r[1].items():
            try:
                if type(val[1]) == float:
                    value = str(int(val[1]))#"{0:.0}".format(val[1])
                    #if len(value) == 9:
                    #   print "Style {0}".format(value)
                    #else:
                        #print "PO# {0}".format(value)
                else:
                    value = val[1]
                #print type(val[1])
                #print r[0],val[0],value
                dd[val[0]]=value
                d[r[0]] = dd
                #print dd
                #csv_write_datedOutfile(lines.encode('ascii', 'replace'))
            except AttributeError:
                pass
    return d

def getbinary_ftp_netsrv101(remote_pathtofile, outfile=None):
    # fetch a binary file
    import ftplib
    session = ftplib.FTP("netsrv101.l3.bluefly.com", "imagedrop", "imagedrop0")
    if outfile is None:
        outfile = sys.stdout
    destfile = open(outfile, "wb")
    print remote_pathtofile
    session.retrbinary("RETR " + remote_pathtofile, destfile.write, 8*1024)
    destfile.close()
    session.quit()
    

def download_imgsrv_png_force(styles_list, alts=None):
    styles_list = []

    for style in styles_list:
        images = []
        colorstyle = style
        hashdir = colorstyle[:4]
        colorstyle_img = colorstyle + ".png"
        
        remotedir = "/mnt/images/images"
        images.append(colorstyle_imgs)
        
        for alt in alts:
            colorstyle_img = colorstyle_img.replace('.png','_alt0' + alt + '.png')
            images.append(colorstyle_img)
            
        for colorstyle_file in images:
            remotepath = os.path.join(remotedir, hashdir, colorstyle_file)
            destpath = os.path.join(rootdir, colorstyle_file)

            try:
                getbinary_ftp_netsrv101(remotepath, outfile=destpath)
                print "Got File via FTP", colorstyle
                return destpath
            except ftplib.error_temp:
                print "Failed FTP Lib error", colorstyle
                #time.sleep(.5)
                try:
                    getbinary_ftp_netsrv101(remotepath, outfile=destpath)
                    print "Second Try Got File via FTP", colorstyle
                    return destpath
                except:
                    return None
            except EOFError:
                print "Failed EOF error", colorstyle
                time.sleep(1)
                try:
                    getbinary_ftp_netsrv101(remotepath, outfile=destpath)
                    print "Second Try Got File via FTP", colorstyle
                    return destpath
                except:
                    return None
            except:
                print "Failed Connect error", colorstyle
                time.sleep(1)
                try:
                    getbinary_ftp_netsrv101(remotepath, outfile=destpath)
                    print "Second Try Got File via FTP", colorstyle
                    return destpath
                except:
                    return None

######################################## ##### ########################################
######################################## Order ########################################
######################################## ##### ########################################

def arg_parser_simple():
    import os,sys, urllib

    args = sys.argv[1:]

    regex_r = re.compile(r'.*?\r.*?')
    regex_n = re.compile(r'.*?\n.*?')

    args1 = args[0].split('\n')   #(','.join(str(arg) for arg in args)).split('\n')
    return args1


def sqlQuery_styles_bypo(po_number):
    import sqlalchemy, sys
    #engine_cnx = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
    engine_cnx = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')

    connection = engine_cnx.connect()
    #querymake_styles_bypoMySQL = "SELECT colorstyle FROM product_snapshot_live WHERE po_number like '{0}' AND image_ready_dt IS NOT NULL ORDER BY colorstyle".format(po_number)
    querymake_StylesByPO_Oracle="SELECT DISTINCT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PO_HDR_ID in ('{0}') order by POMGR.PRODUCT_COLOR.VENDOR_STYLE asc".format(po_number)

    result = connection.execute(querymake_StylesByPO_Oracle)
    colorstyles_list = []
    vendor_colorstyle_kv = {}
    
    for row in result:
        vendor_colorstyle_kv['vendor_style'] = row['colorstyle']
        colorstyles_list.append(row['colorstyle'])
    connection.close()

    return list(set(sorted(colorstyles_list))), vendor_colorstyle_kv


def url_download_file(url,filepath):
    import urllib
    error_check = urllib.urlopen(url)
    urlcode_value = error_check.getcode()
    print urlcode_value
    
    if urlcode_value == 200:
        urllib.urlretrieve(url, filepath)
        print "Retrieved: " + url + " ---> " + filepath


def download_server_imgs(style):
    netsrv101_url = 'ftp://imagedrop:imagedrop0@netsrv101.l3.bluefly.com//mnt/images/images/'
    colorstyle = str(style)
    ext_PNG     = '.png'
    ext_JPG     = '.jpg'

    netsrv101_url_file = os.path.join(netsrv101_url, colorstyle[:4], colorstyle + ext_PNG)
    colorstyle_file = os.path.join(os.path.abspath(os.curdir), colorstyle + ext_PNG)
    try:
        url_download_file(netsrv101_url_file, colorstyle_file)    
        alt = 0   
        for x in range(1,6):
            try:
                alt = x   
                ext_ALT = '_alt0{0}{1}'.format(str(alt),ext_PNG)
                colorstylealt = colorstyle + ext_ALT
                colorstyle_filealt = os.path.join(os.path.abspath(os.curdir), colorstylealt)
                
                netsrv101_url_filealt = os.path.join(netsrv101_url, colorstyle[:4], colorstylealt)
                
                if url_download_file(netsrv101_url_filealt, colorstyle_filealt):
                    url_download_file(netsrv101_url_filealt, colorstyle_filealt)
                    return True
                else:
                    return
            except IOError:
                pass
                return False
    except IOError:
        pass

 
######################################## ##### ########################################
########################################  Run  ########################################
######################################## ##### ########################################

def main():
    import os,sys
    old_po = ''        
    new_po = ''
    styles_list = ''
    po_number = ''

    args = arg_parser_simple()

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
            styles_list = sqlQuery_GetStyleVendor_ByPO(po_number)
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
        
        for oldnum in oldstyles_list:
            returned_files = download_server_imgs(oldnum)
            newnum = newstyles_dict[oldstyles_dict.get(oldnum))]
            for returned_file in returned_files:
                os.rename = (returned_file, returned_file.replace(oldnum,newnum))
                
###############################

if __name__ == '__main__': 
    main()
    #x = main()
    #print x

