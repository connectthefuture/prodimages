#!/usr/bin/env python
# -*- coding: utf-8 -*-

def batch_load_dated_mozu_jpgs(rootdir=None):
    ########## MOZU - Five ##########
    ### Date Defs
    from os import chdir, path, curdir
    import datetime, glob, shutil

    todaysdatefullsecs = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    todaysdatefull = todaysdatefullsecs[:12]
    todaysdate = todaysdatefull[:8] # '{:%Y,%m,%d}'.format(datetime.datetime.now())
    todaysdatearch = todaysdatefull # '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())

    ## Define for Creating Archive dirs
    archive = '/mnt/Post_Complete/Complete_Archive/Uploaded'
    #archive_uploaded = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""), "uploaded_" + str(todaysdatefullsecs).replace(",", ""))
    archive_uploaded_day = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""))
    imgdest_jpg_mozu = path.join(archive_uploaded_day, 'JPG_MOZU_LOAD')
    imgdest_jpg_mozu_loaded = path.join(imgdest_jpg_mozu, 'LOADED')


    # try:
    #     os.makedirs(imgdest_jpg_mozu, 16877)
    # except:
    #     pass
    #
    # for f in img_list:
    #     shutil.copy2(f, imgdest_jpg_mozu)

    final_mozu_list = glob.glob(path.join(imgdest_jpg_mozu, '*/*/*.??[gG]'))
