#!/usr/bin/env python
# -*- coding: utf-8 -*-

def batch_load_dated_mozu_jpgs(**kwargs):
    ########## MOZU - Five ##########
    ### Date Defs
    from os import path, renames  # , curdir, chdir
    import datetime, glob # , shutil

    ## Define for Creating Archive dirs
    rootdir = kwargs.get('rootdir', '/mnt/Post_Complete/Complete_Archive/Uploaded')
    delta = kwargs.get('delta', '')
    if delta:
        days_ago = datetime.timedelta(days=int(delta))
        todaysdatefullsecs = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now()-days_ago)
        print todaysdatefullsecs, ' <-- Deltaed'
        todaysdatefull = todaysdatefullsecs[:12]
        todaysdate = todaysdatefull[:8] # '{:%Y,%m,%d}'.format(datetime.datetime.now())
        todaysdate_real = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())[:8]
    else:
        todaysdatefullsecs = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        todaysdatefull = todaysdatefullsecs[:12]
        todaysdate = todaysdatefull[:8] # '{:%Y,%m,%d}'.format(datetime.datetime.now())
        todaysdate_real = todaysdate

    # archive_uploaded = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""), "uploaded_" + str(todaysdatefullsecs).replace(",", ""))
    dated_dir = "dateloaded_" + str(todaysdate)
    dated_search_dir = path.join(rootdir, dated_dir)
    imgdest_jpg_mozu = path.join(todaysdate_real, 'JPG_MOZU_LOAD')
    imgdest_jpg_mozu_loaded = path.join(imgdest_jpg_mozu, 'LOADED')
    # For later pulling production pngs into the batch as well
    #globby_production_png = path.join(dated_search_dir,'PNG', '*.png')
    imgdest_png_stored = path.join(imgdest_jpg_mozu, 'LOADED')

    import mozu_exec  #, mozu_image_util_functions
    ## Compress and convert to jpg and store in separate dir for concurrent xfers
    # if path.isfile(pngout):
    load_collect_batch_mozu_list = glob.glob(path.join(dated_search_dir, '*/JPG_MOZU_LOAD/*.[Jjp][Ppn][gG]'))
    try:
        if load_collect_batch_mozu_list:
            for f in load_collect_batch_mozu_list:
                print '31-->', f, imgdest_jpg_mozu
                # rename(f, imgdest_jpg_mozu)
                renames(f, path.join(imgdest_jpg_mozu, path.basename(f)))
    except IndexError:
        print ' Index Error'
    load_batch_mozu_list = glob.glob(path.join(imgdest_jpg_mozu, '*.[Jjp][Ppn][gG]'))
    print imgdest_jpg_mozu, ' <-- DEST Mozu begin mozu exec'
    if len(load_batch_mozu_list) > 0:
        mozu_exec.main(load_batch_mozu_list)
        for f in load_batch_mozu_list:
            print '37-->', f, imgdest_jpg_mozu_loaded
            try:
                renames(f, path.join(imgdest_jpg_mozu_loaded, path.basename(f)))
            except OSError:
                print 'OS ERROR 45 ', f, imgdest_jpg_mozu_loaded, imgdest_jpg_mozu
        load_batch_mozu_done = glob.glob(path.join(imgdest_jpg_mozu_loaded, '*.[Jj][Pp][gG]'))
        # Store the pngs
        store_png_list =  [ renames(f, path.join(imgdest_png_stored, path.basename(f))) for f in glob.glob(path.join(imgdest_jpg_mozu, '*.[Pp][Nn][gG]')) if f is not None]
        return load_batch_mozu_done
        # for f in load_batch_mozu_list:
        #    print path.abspath(f)
        #    #jpgout = mozu_image_util_functions.magick_convert_to_jpeg(f,destdir=imgdest_jpg_mozu)
    else:
        print imgdest_jpg_mozu, ' <-- DEST Mozu \n<---- ZERO FILES to Process'

if __name__ == '__main__':
    import sys
    try:
        if sys.argv[1].isdigit():
            delta = sys.argv[1]
            batch_load_dated_mozu_jpgs(delta=delta)
        else:
            root = sys.argv[1]
            if len(sys.argv[1:]) > 1:
                if sys.argv[2].isdigit():
                    delta = sys.argv[2]
                    batch_load_dated_mozu_jpgs(rootdir=root,delta=delta)
                else:
                    print ' I dont know how to proceed with "{}" as your 2nd cmd line arg'.format(sya.argv[2])
            else:
                batch_load_dated_mozu_jpgs(rootdir=root)
    except IndexError:
        batch_load_dated_mozu_jpgs()
