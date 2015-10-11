#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,sqlalchemy,glob,io


def import_404_data():
    mysql_engine_data = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/data_imagepaths')
    mysql_engine_www  = sqlalchemy.create_engine('mysql+mysqldb://root:mysql@prodimages.ny.bluefly.com:3301/www_django')

    badurldir = '/mnt/Post_Complete/Complete_Archive/MARKETPLACE/ERRORS/'
    errorfiles = ''
    try:
        errorfiles = [io.open(f,'rbU').read().split('/')[0] for f in glob.glob(os.path.join(os.path.abspath(badurldir), '*.txt'))]
    except:
        pass
    errorstyles = [f.split('/')[-1][:9] for f in glob.glob(os.path.join(os.path.abspath(badurldir), '*.txt'))]
    if errorfiles:
        zipped = zip(errorstyles,errorfiles)
        print errorfiles

    connection_www = mysql_engine_www.connect()
    
    for colorstyle in errorstyles:
        error_code = '404'
        try:

            connection_www.execute("""INSERT INTO supplier_ingest_404 (colorstyle, error_code) VALUES (%s,%s)
                                    ON DUPLICATE KEY UPDATE 
                                    error_code  = VALUES(error_code);""", colorstyle, error_code)
        except AttributeError:
            print colorstyle
            pass

def main():
    import_404_data()


if __name__ == '__main__':
    main()