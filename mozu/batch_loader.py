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
    if not rootdir:
        rootdir = archive
    else:
        archive = '/mnt/Post_Complete/Complete_Archive/Uploaded'

    # archive_uploaded = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""), "uploaded_" + str(todaysdatefullsecs).replace(",", ""))
    dated_dir = "dateloaded_" + str(todaysdate).replace(",", "")
    archive_uploaded_day = path.join(archive, dated_dir)
    imgdest_jpg_mozu = path.join(archive_uploaded_day, 'JPG_MOZU_LOAD')
    imgdest_jpg_mozu_loaded = path.join(imgdest_jpg_mozu, 'LOADED')


    # try:
    #     os.makedirs(imgdest_jpg_mozu, 16877)
    # except:
    #     pass
    #
    # for f in img_list:
    #     shutil.copy2(f, imgdest_jpg_mozu)

    import mozu_exec, mozu_image_util_functions
    ## Compress and convert to jpg and store in separate dir for concurrent xfers
    #if path.isfile(pngout):
    load_collect_batch_mozu_list = glob.glob(path.join(archive_uploaded_day, '*/JPG_MOZU_LOAD/*.??[gG]'))
    for f in load_collect_batch_mozu_list:
        shutil.move(f, imgdest_jpg_mozu)

    load_batch_mozu_list = glob.glob(path.join(imgdest_jpg_mozu, '*.??[gG]'))
    mozu_exec.main(load_batch_mozu_list)
    for f in load_collect_batch_mozu_list:
        shutil.move(f, imgdest_jpg_mozu_loaded)
    load_batch_mozu_done = glob.glob(path.join(imgdest_jpg_mozu_loaded, '*.*[gG]'))

    return load_batch_mozu_done
    #for f in load_batch_mozu_list:
    #    print path.abspath(f)
    #    #jpgout = mozu_image_util_functions.magick_convert_to_jpeg(f,destdir=imgdest_jpg_mozu)



if __name__ == '__main__':
    import sys
    try:
        rootdir = sys.argv[1]
        batch_load_dated_mozu_jpgs(rootdir)
    except IndexError:
        batch_load_dated_mozu_jpgs()
