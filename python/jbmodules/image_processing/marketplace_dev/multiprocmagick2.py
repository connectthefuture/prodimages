#!/usr/bin/env python
#-*- coding: utf-8 -*-

def run_threaded_imgdict(argslist=None):
    import Queue
    import threading
    import multiprocessing
    import jbmodules
    from jbmodules.image_processing.marketplace_dev.magicColorspaceModAspctLoadFaster2 import sort_files_by_values
    q = Queue.Queue()
    # print type(argslist), len(argslist), ' type and length argslist \n'
    #print type(argslist), type(argslist)
    for i in argslist[0]: #put 30 tasks in the queue
        #print 'i ', ' argslist'
        if i:
            q.put([i])


    img_dict_list = []
    def worker():
        count = 0
        while True:
            item = q.get()
            #print item[0]
            imgdata = sort_files_by_values(item)
            #print imgdata
            img_dict_list.append(imgdata)
            # Can add functions to adjust based on imgdict params or store image data or delete etc.
            # insertres =  insert_gridfs_extract_metadata(item[0])
            count += 1
            print count, '\n\t ImageDict Threade'#, imgdata
            q.task_done()


    #print 'argsL --> len arglist', len(argslist[0]), type(argslist), ' Type ArgsList RunThreaded'
    jobcount = multiprocessing.cpu_count() - 2 #len(argslist[0]) #detect number of cores
    print("Creating %d threads" % jobcount)
    for i in xrange(jobcount):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    q.join() #block until all tasks are done
    return img_dict_list


def funkRunner3(root_img_dir='', single_style='', update=''):
    import multiprocessing
    #import Queue
    import threading
    import glob, os
    #from os import os.path
    import jbmodules
    from jbmodules import image_processing
    from jbmodules.image_processing.marketplace_dev.magicColorspaceModAspctLoadFaster2 import rename_retouched_file, sort_files_by_values
    destdir = os.environ.get('DESTDIR', '/mnt/Post_Complete/ImageDrop')
    print 'Starting Funkrunner2 Pools'

    ## Get all modules on poython exec path
    import sys
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules/image_processing/magick_tweaks')
    sys.path.append('/usr/local/batchRunScripts/mozu')
    sys.path.append('/usr/local/batchRunScripts/python')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules/mongo_tools')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules/image_processing')
    sys.path.append('/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace_dev')

    ########## One ##########
    #
    # 1A
    # List of images to run through processing as glob of the root_img_dir
    #print root_img_dir, ' <-- Rootimgdir FunkR2'

    if update:
        root_img_dir = '/mnt/Post_Complete/Complete_Archive/MARKETPLACE'
        imagesGlob = os.path.join(root_img_dir, '*/999999/*.??[gG]')
        images = [f for f in glob.glob(imagesGlob) if f is not None]
    elif single_style:
        imagesGlob = glob.glob(os.path.join(root_img_dir, '*/*/{0}*.??g'.format(single_style))) + glob.glob(os.path.join(root_img_dir, '*/*/*/{0}*.??g'.format(single_style)))
        images = [f for f in imagesGlob if f is not None]
    elif os.environ.get('ROOT_IMG_DIR') or root_img_dir:
        root_img_dir = os.environ.get('ROOT_IMG_DIR', root_img_dir)
        imagesGlob = os.path.join(root_img_dir, '*/*/*.??[gG]')
        images = [f for f in glob.glob(imagesGlob) if f is not None]
    else:
        root_img_dir = '/mnt/Post_Complete/Complete_Archive/MARKETPLACE'
        imagesGlob = os.path.join(root_img_dir, '*/*/*.??[gG]')
        images = [f for f in glob.glob(imagesGlob) if f is not None]

    print imagesGlob, "GLOBB11"
    # 1B
    # Rename files using Multiproc pool
    poolRename = multiprocessing.Pool(8)

    while len(images) == 0:
        print len(images), '  <-- Length of the Images to Rename,Process etc. Now the Renamer'
        break

    resrename = poolRename.map(rename_retouched_file, images)
    poolRename.close()
    poolRename.join()
    print 'Images Renamed'

    ## replace the glob pattern for single styles after the rename
    #imagesGlob = imagesGlob.replace('_[1-6]', '*')
    print imagesGlob, "GLOBB22"
    ########## Two ##########
    #
    # 2
    # Extract image pixel data for enhancements. As list of tuples, [<url>, {rgbdata} ].. ithink
    img_list =  [ f for f in glob.glob(imagesGlob) if f is not None ]
    print type(img_list), '\tLen ImageList preThreaded', destdir
    img_dict = run_threaded_imgdict(argslist=(img_list,))
    print type(img_dict), '\tLen ImageDict postThreaded', destdir

    ########## Three ##########
    #
    # 3A
    # Init Task and Results Queues
    from ConsumerManager import Starter

    s = Starter()
    s.img_dict = img_dict
    s.destdir  = destdir
    s.start()

    #
    # if single_style and len(imagesGlob) <= 7:
    #     settest = list(set([ f.split('/')[:9] for f in glob.glob(imagesGlob) if f is not None ] ))
    #     print settest, len(settest), ' <=====END FLAG TEST'
    #     for img in imagesGlob:
    #         os.remove(img)
    #         print 'Deleted {0} after uploading'.format(img)
    # else:
    print 'DUNNNN --> multproc2', single_style, len(imagesGlob), '<-- LENGlob'

    if img_dict and type(img_dict) == dict:
        return img_dict
    ########## SIX ##########
    # Delete em all
    # if root_img_dir == '/mnt/Post_Complete/Complete_Archive/MARKETPLACE':
    #     poolDelete = multiprocessing.Pool(8)
    #     import os
    #     poolDelete.map(os.remove, img_list)
    #     poolDelete.close()
    #     poolDelete.join()
    #     print' And now they are Gone'

    #return



if __name__ == '__main__':
    print 'Dont call this separately '
