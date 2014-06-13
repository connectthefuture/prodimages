#!/usr/bin/env python
import os, sys, re, csv


def sqlQuery_styles_bypo(po_number):
    import sqlalchemy, sys
    #engine_cnx = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
    engine_cnx = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')

    connection = engine_cnx.connect()

    #querymake_styles_bypoMySQL = "SELECT colorstyle FROM product_snapshot_live WHERE po_number like '{0}' AND image_ready_dt IS NOT NULL ORDER BY colorstyle".format(po_number)
    querymake_StylesByPO_Oracle="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style, POMGR.PO_LINE.PO_HDR_ID AS po_hdr_id FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE POMGR.PRODUCT_COLOR.IMAGE_READY_DT is not null AND POMGR.PO_LINE.PO_HDR_ID = '" + ponum + "'"

    result = connection.execute(querymake_StylesByPO_Oracle)
    colorstyles_list = []
    for row in result:
        colorstyles_list.append(row['colorstyle'])
    connection.close()

    return set(sorted(colorstyles_list))
    


def readxl_outputdict(workbk=None):         
    import csv,xlrd,sys
#    workbk = sys.argv[1]
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
#                    if len(value) == 9:
#                        print "Style {0}".format(value)
#                    else:
#                        print "PO# {0}".format(value)
                        
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
    

def download_imgsrv_png(styles_list, alts=None):
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



###############################