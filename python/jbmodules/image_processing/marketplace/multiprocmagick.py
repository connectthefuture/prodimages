#!/usr/bin/env python
#-*- coding: utf-8 -*-


def run_multiproccesses_magick2(searchdir=None):
    import multiprocessing
    import Queue
    import subprocess
    import glob,os
    import mongo_tools.mongo_gridfs_insert_file as mongo_gridfs_insert_file
    from mongo_tools.mongo_image_prep import insert_gridfs_extract_metadata
    import magicColorspaceModAspctLoadFaster2 as magickProc
    if not searchdir:
        searchdir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')
    else:
        pass

    pool = multiprocessing.Pool(8)
    img_list = []
    if searchdir.split('/')[-1] == 'SWI':
        [ img_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*/*.*')) if os.path.isfile(g) ]
    else:
        [ img_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*/*/*.*')) if os.path.isfile(g) ]

    

    results = pool.map(magickProc.main,img_list)
    print results

    # close the pool and wait for the work to finish
    pool.close()
    print 'PoolClose'
    pool.join()
    print 'PoolJoin'



def funkRunner(root_img_dir=None):
    import multiprocessing
    import Queue
    import threading
    import glob, os
    from image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import rename_retouched_file, sort_files_by_values
    from image_processing.magick_tweaks import convert_img_srgb as convert_img_srgb
    from mongo_tools import mongo_gridfs_insert_file, mongo_image_prep
    import image_processing.marketplace.magicColorspaceModAspctLoadFaster2 as magickProc
    #from mongo_tools.mongo_image_prep import insert_gridfs_extract_metadata

    imgs_renamed = [rename_retouched_file(f) for f in (glob.glob(os.path.join(root_img_dir,'*.??[gG]')))]
    img_dict = sort_files_by_values(glob.glob(os.path.join(root_img_dir,'*.??[gG]')))

    q = Queue.Queue()
    for k,v in img_dict.items():
        try:
            img_rgbmean = k, v.items()
            q.put(img_rgbmean)
        except AttributeError:
            print 'SOMETHING IS WRONG WITH THE IMAGE Error {}'.format(k)
            pass

    def worker():
        count = 0
        destdir =  '/mnt/Post_Complete/ImageDrop/'
        while True:
            img, rgbmean = q.get()
            convert_img_srgb.main(image_file=img)
            ## Add to Mongo DB
            try:
                mongo_image_prep.update_gridfs_extract_metadata(img, db_name='gridfs_mrktplce')
            except:
                mongo_image_prep.insert_gridfs_extract_metadata(img, db_name='gridfs_mrktplce')
            ## Generate png from source then jpgs from png
            pngout = magickProc.subproc_magick_png(img, rgbmean=dict(rgbmean), destdir=destdir)
            magickProc.subproc_magick_large_jpg(pngout, destdir=destdir)
            magickProc.subproc_magick_medium_jpg(pngout, destdir=destdir)
            count += 1
            print count
            q.task_done()

    cpus=multiprocessing.cpu_count() #detect number of cores
    print("Creating %d threads" % cpus)
    for i in xrange(cpus*2):
         t = threading.Thread(target=worker)
         t.daemon = True
         t.start()

    q.join() #block until all tasks are done



def run_multiproccesses_magick(searchdir=None):
    import multiprocessing
    import glob,os
    import image_processing.marketplace.magicColorspaceModAspctLoadFaster2 as magickProc
    if not searchdir:
        searchdir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE/SWI')
    else:
        pass

    pool = multiprocessing.Pool(4)
    directory_list = []
    if searchdir.split('/')[-1] == 'SWI':
        [ directory_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*')) if os.path.isdir(g) ]
    elif searchdir.split('/')[-1][:3] == '3_L':
        [ directory_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*')) if os.path.isdir(g) ]
        print 'Image Clipping Import', searchdir
    else:
        [ directory_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*/*')) if os.path.isdir(g) ]

    results = pool.map(magickProc.main,directory_list)
    print results

    # close the pool and wait for the work to finish
    pool.close()
    print 'PoolClose'
    pool.join()
    print 'PoolJoin'

if __name__ == '__main__':
    run_multiproccesses_magick()
