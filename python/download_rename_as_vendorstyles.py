#!/usr/bin/env python

def sqlQuery_vendstyles_by_stylelist(colorstyles_list_as_string=None):
    import sqlalchemy, sys
    #engine_cnx = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')
    engine_cnx = sqlalchemy.create_engine('oracle+cx_oracle://prod_team_ro:9thfl00r@borac101-vip.l3.bluefly.com:1521/bfyprd11')

    connection = engine_cnx.connect()
    styles_formatted = '{}'.format(colorstyles_list_as_string.split())
    #querymake_styles_bypoMySQL = "SELECT colorstyle FROM product_snapshot_live WHERE colorstyles_list like '{0}' AND image_ready_dt IS NOT NULL ORDER BY colorstyle".format(colorstyles_list)
    querymake_StylesByPO_Oracle="SELECT POMGR.PRODUCT_COLOR.ID AS colorstyle, POMGR.PRODUCT_COLOR.VENDOR_STYLE AS vendor_style FROM POMGR.PRODUCT_COLOR INNER JOIN POMGR.PO_LINE ON POMGR.PRODUCT_COLOR.ID = POMGR.PO_LINE.PRODUCT_COLOR_ID WHERE PRODUCT_COLOR.ID in ({0}) order by POMGR.PRODUCT_COLOR.VENDOR_STYLE asc".format(styles_formatted.replace('[','').replace(']', ''))
    #print querymake_StylesByPO_Oracle
    #result = connection.execute(newQ)
    result = connection.execute(querymake_StylesByPO_Oracle)
    #colorstyles_list = []
    vendor_colorstyle_kv = {}
    
    for row in result:
        vendor_colorstyle_kv[row['colorstyle']] = row['vendor_style'].replace(' ', '').replace('.', '').lower()
        #colorstyles_list.append(row['colorstyle'])
    connection.close()
    #sorted(colorstyles_list), 
    return vendor_colorstyle_kv


def download_server_imgs_rename_vendstyles(colorstyle,vendor_style):
    import ftplib, urllib, shutil
    from os import path, chdir, getcwd
    colorstyle = str(colorstyle)
    ext_PNG     = '.png'    
    netsrv101_mnt = '/mnt/images'
    bfly_png = path.join(netsrv101_mnt, colorstyle[:4], colorstyle + ext_PNG).replace('\n', '').replace('.png.png','.png').replace('.jpg.jpg','.jpg')

    vendor_style_file = path.join(path.abspath(getcwd()), vendor_style + ext_PNG)
    #try:
    shutil.copy(bfly_png, vendor_style_file)    
    alt = 0
    for x in xrange(1,6):
        try:
            alt = x   
            ext_ALT = '_alt0{0}{1}'.format(str(alt),ext_PNG)
            colorstylealt = colorstyle + ext_ALT
            c = vendor_style + ext_ALT
            vendor_style_filealt = path.join(path.abspath(getcwd()), vendor_stylealt)            
            bfly_png_filealt = path.join(netsrv101_mnt, colorstyle[:4], colorstylealt)
            
            if path.isfile(bfly_png_filealt):
                shutil.copy(bfly_png_filealt, vendor_style_filealt)
                print 'Copied {} to {}'.format(bfly_png_filealt, vendor_style_filealt)
            else:
                print 'Not a File {0}'.format(bfly_png_filealt)
        except IOError:
            pass


###################### ##### ########################################
########################################  Run  ########################################
######################################## ##### ########################################

def main(styles_list):
    import sys
    colorvendorstyle_dict= sqlQuery_vendstyles_by_stylelist(styles_list)
    #renamed_dir = path.join(os.path.abspath(os.path.expanduser('~')), new_po)
    #os.makedirs(renamed_dir)
    from os import path, getcwd, chdir, makedirs
    rootdir = path.abspath(getcwd())
    print 'Rootdir is {0}'.format(rootdir)
    for k,v in colorvendorstyle_dict.iteritems():
        chdir(rootdir)
        dload_dir = path.join(rootdir, str(k))
        try:
            makedirs(dload_dir)
        except:
            pass
        chdir(dload_dir)        
        colorstyle = str(k)
        vendor_style = str(v)
        print colorstyle,vendor_style
        download_server_imgs_rename_vendstyles(colorstyle,vendor_style)


###############################

if __name__ == '__main__': 
    styles_list = '360441401 328358901 342891401 353619301 354194001 354194201 354195401 358664401 358664501 376352101 379784801 380706301 380706501 351970101 347676401 347676501 336174901 336175001 345818401 380503401 380504001 380504301 380504901 380505001 380505501 380506001 380506101 359637401 362584001 366479401 366651501 367463001 368968301 368972201 373103401 373103501 373103601 374060401 374060601 374061101 374061301 374061401 374061701 374061801 374061901 374062001 374062101 374062201 374062501 374062701 374062801 374062901 374063001 374063301 343322901 365822401 375170601 375171801 375214301 376854801 363958301 375171101 365822201 376755901 376756501 376757001 376757301 374452201 374452401 374452501 374452601 374452701 374452801 374452901 374453001 342863001 347940801 347940901 347941001 347941101 347941201 347941301 347941501 347941601 347941701 347941801 347941901 347942001 347942101 347942201 347942401 347942501 347942601 347942701 351966001 357510601 357510701 357510901 359244201 359244301 359244401 359244701 359244801 359244901 359245101 359245201 359970501 364541601 364922701 364922901 351998901 357511201 359970301 359970401 364538301 364538401 364538501 364538801 364539401 364539701 364539801 364540001 364540101 364540401 364540501 364540901 364541201 364923001 365344201 365822501 367264101 367264301 367264501 367264601'

    main(styles_list)
    #x = main()
    #print x

