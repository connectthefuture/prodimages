#!/usr/bin/env python
#-*- coding: utf-8 -*-

# import multiprocessing, time
# class Consumer(multiprocessing.Process):
#     def __init__(self, task_queue, result_queue):
#         multiprocessing.Process.__init__(self)
#         self.task_queue = task_queue
#         self.result_queue = result_queue
#     def run(self):
#         proc_name = self.name
#         #try:
#         while True:
#             next_task = self.task_queue.get()
#             if next_task is None:
#                 # Poison pill means shutdown
#                 print '%s: Exiting' % proc_name
#                 #fnx = dir(self)
#                 self.task_queue.task_done()
#                 print self.result_queue, self.task_queue, ' resQ and TaskQ <-- --> pid -- isalive --> ', self.pid, self.is_alive
#                 break
#             print '%s: %s' % (proc_name, next_task)
#             answer = next_task()
#
#             self.task_queue.task_done()
#             self.result_queue.put(answer)
#             print '%s: AnsweredPUT-taskDone in Consumer ' % proc_name
#         return
#         # except AttributeError:
#         #     print ' None Type Error End '
#         #     return
#         # finally:
#         #     return
#
#
#
# class Task(object):
#     def __init__(self, img, rgbmean, destdir):
#         import tempfile, shutil
#         # tmpfileobj, tmpfile_path = tempfile.mkstemp(suffix=".png")
#         self.img = img
#         self.rgbmean = rgbmean
#         self.destdir = destdir
#         #self.tmppngout = tempfile.mkstemp(suffix=".png")
#
#     def __call__(self):
#         import jbmodules
#         import os
#         from jbmodules import image_processing
#         from jbmodules.image_processing import marketplace, magick_tweaks
#         import jbmodules.image_processing.marketplace.magicColorspaceModAspctLoadFaster2 as magickProc2
#         #time.sleep(0.1) # pretend to take some time to do the work
#         import jbmodules.image_processing.magick_tweaks.convert_img_srgb
#         from mozu import *
#         # try:
#         jbmodules.image_processing.magick_tweaks.convert_img_srgb.main(image_file=self.img)
#
#         print self.img, ' <-- self.img ', self.rgbmean
#         #self.tmppngout(
#         pngout = magickProc2.subproc_magick_png(self.img, rgbmean=self.rgbmean, destdir=self.destdir)
#         if os.path.isfile(pngout):
#             magickProc2.subproc_magick_large_jpg(pngout, destdir=self.destdir)
#             ret = magickProc2.subproc_magick_medium_jpg(pngout, destdir=self.destdir)
#             try:
#                 ############################
#                 ###### mozu
#                 ############################
#                 import sys, datetime
#                 from os import chdir, path, makedirs
#                 todaysdatefullsecs = '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now())
#                 tmp_mozu_loading = os.path.join("/mnt/Post_Complete/Complete_Archive/.tmp_mozu_loading" , "tmp_" + str(todaysdatefullsecs).replace(",", ""))
#                 if path.isdir(tmp_mozu_loading):
#                     pass
#                 else:
#                     try:
#                         os.makedirs(tmp_mozu_loading, 16877)
#                     except:
#                         print " Error", tmp_mozu_loading
#                 chdir('/usr/local/batchRunScripts/mozu')
#                 import mozu_exec, mozu_image_util_functions
#                 ## Compress and convert to jpg
#                 if path.isfile(pngout):
#                     print ' Is file PNGOUT', pngout, img
#                     jpgout = mozu_image_util_functions.magick_convert_to_jpeg(pngout,destdir=tmp_mozu_loading)
#                 else:
#                     #pass
#                     jpgout = mozu_image_util_functions.magick_convert_to_jpeg(self.img,destdir=tmp_mozu_loading)
#                 mozu_exec.main(jpgout)
#                 ############################
#             except ImportError:
#                 print 'Import Error multiprocmagick2:69'
#         #os.remove(self.tmppngout[1])
#         # except TypeError:
#         #         print self.img, ' <-- Type-Error in Task -->', self.destdir
#         #         pass
#         # except AttributeError:
#         #         print self.img, ' <-- AttributeError in Task -->', self.destdir
#         #         pass
#         # except IndexError:
#         #     ' None Type Error End '
#         #     pass
#             return '-ret- %s \n-path- %s \n-dest- %s \n' % (ret, self.img, self.destdir)
#         else:
#             return
#
#     def __str__(self):
#         return '%s -- %s' % (self.img, self.destdir)


def run_threaded_imgdict(argslist=None):
    import Queue
    import threading
    import multiprocessing
    import jbmodules
    from jbmodules.image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import sort_files_by_values
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


def funkRunner3(root_img_dir=None, single_flag=None):
    import multiprocessing
    #import Queue
    import threading
    import glob, os
    #from os import os.path
    import jbmodules
    from jbmodules import image_processing
    from jbmodules.image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import rename_retouched_file, sort_files_by_values
    destdir = '/mnt/Post_Complete/ImageDrop'
    print 'Starting Funkrunner2 Pools'


    ########## One ##########
    #
    # 1A
    # List of images to run through processing as glob of the root_img_dir
    #print root_img_dir, ' <-- Rootimgdir FunkR2'
    if root_img_dir == '/mnt/Post_Complete/Complete_Archive/MARKETPLACE' or root_img_dir is None:
        if not single_flag:
            imagesGlob = os.path.join(root_img_dir, '*/*/*.??[gG]')
        else:
            imagesGlob = os.path.join(root_img_dir, '*/*/*/{0}_[1-6].??[gG]'.format(single_flag))

    else:
        imagesGlob = os.path.join(root_img_dir, '*.??[gG]')

    print imagesGlob, "GLOBB"
    # 1B
    # Rename files using Multiproc pool
    poolRename = multiprocessing.Pool(8)
    images = [ f for f in glob.glob(imagesGlob) if f is not None ]
    while len(images) == 0:
        print len(images), '  <-- Length of the Images to Rename,Process etc. Now the Renamer'
        break

    resrename = poolRename.map(rename_retouched_file, images)
    poolRename.close()
    poolRename.join()
    print 'Images Renamed'


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


    if single_flag and len(imagesGlob) <= 7:
        settest = list(set([ f.split('/')[:9] for f in glob.glob(imagesGlob) if f is not None ] ))
        print settest, len(settest), ' <=====END FLAG TEST'
        for img in imagesGlob:
            os.remove(img)
            print 'Deleted {0} after uploading'.format(img)
    else:
        print 'multproc2', single_flag, len(imagesGlob), '<-- LENGlob'
    ########## Five ##########
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
