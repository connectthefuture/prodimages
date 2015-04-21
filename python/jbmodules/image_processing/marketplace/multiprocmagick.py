#!/usr/bin/env python
#-*- coding: utf-8 -*-

import multiprocessing, time

class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
    def run(self):
        proc_name = self.name
        #try:
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                #fnx = dir(self)
                self.task_queue.task_done()
                print self.result_queue, self.task_queue, ' resQ and TaskQ <-- --> pid -- isalive --> ', self.pid, self.is_alive
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()

            self.task_queue.task_done()
            self.result_queue.put(answer)
            print '%s: AnsweredPUT-taskDone in Consumer ' % proc_name
        return
        # except AttributeError:
        #     print ' None Type Error End '
        #     return
        # finally:
        #     return



class Task(object):
    def __init__(self, img, rgbmean, destdir):
        import tempfile, shutil
        # tmpfileobj, tmpfile_path = tempfile.mkstemp(suffix=".png")
        self.img = img
        self.rgbmean = rgbmean
        self.destdir = destdir
        #self.tmppngout = tempfile.mkstemp(suffix=".png")

    def __call__(self):
        #import jbmodules
        import os
        import image_processing
        from image_processing import marketplace, magick_tweaks
        import image_processing.marketplace.magicColorspaceModAspctLoadFaster2 as magickProc2
        #time.sleep(0.1) # pretend to take some time to do the work
        import image_processing.magick_tweaks.convert_img_srgb
        # try:
        image_processing.magick_tweaks.convert_img_srgb.main(image_file=self.img)

        print self.img, ' <-- self.img ', self.rgbmean
        #self.tmppngout(
        pngout = magickProc2.subproc_magick_png(self.img, rgbmean=self.rgbmean, destdir=self.destdir)
        if os.path.isfile(pngout):
            magickProc2.subproc_magick_large_jpg(pngout, destdir=self.destdir)
        if os.path.isfile(pngout):
            ret = magickProc2.subproc_magick_medium_jpg(pngout, destdir=self.destdir)
        
        #os.remove(self.tmppngout[1])
        # except TypeError:
        #         print self.img, ' <-- Type-Error in Task -->', self.destdir
        #         pass
        # except AttributeError:
        #         print self.img, ' <-- AttributeError in Task -->', self.destdir
        #         pass
        # except IndexError:
        #     ' None Type Error End '
        #     pass
            return '-ret- %s \n-path- %s \n-dest- %s \n' % (ret, self.img, self.destdir)
        else: 
            return

    def __str__(self):
        return '%s -- %s' % (self.img, self.destdir)


def run_threaded_imgdict(argslist=None):
    import Queue
    import threading
    import multiprocessing
    import image_processing
    from image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import sort_files_by_values
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


def funkRunner2(root_img_dir=None):
    import multiprocessing
    #import Queue
    import threading
    import glob, os
    #from os import os.path
    #import jbmodules
    import image_processing
    from image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import rename_retouched_file, sort_files_by_values
    destdir = '/mnt/Post_Complete/ImageDrop'
    print 'Starting Funkrunner2 Pools'


    ########## One ##########
    #
    # 1A
    # List of images to run through processing as glob of the root_img_dir
    #print root_img_dir, ' <-- Rootimgdir FunkR2'
    if root_img_dir == '/mnt/Post_Complete/Complete_Archive/MARKETPLACE' or root_img_dir is None:
        imagesGlob = os.path.join(root_img_dir, '*/*/*.??[gG]')
    else:
        imagesGlob = os.path.join(root_img_dir, '*.??[gG]')


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
    #print type(img_list), '\tLen ImageList preThreaded'
    img_dict = run_threaded_imgdict(argslist=(img_list,))


    ########## Three ##########
    #
    # 3A
    # Init Task and Results Queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # 3B
    # Start consumers
    num_consumers = multiprocessing.cpu_count() - 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, results)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()

    # 3C --> Run
    # Tasks Add
    # Add Images and rgb data and dest to tasks
    num_jobs = len(img_dict)
    #print 'jobs -- consumers -- root_img_dir --> ', num_jobs, consumers, root_img_dir
    for item in img_dict:
        img, rgbmean = item.keys()[0], item.values() #.items()
        #print img, 'rgbmean', ' Img -- RGB Mean'
        tasks.put(Task(img, rgbmean, destdir))
    print 'Put Tasks'

    # 3P --> Poinson pill to help stop hanging procs
    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)
        #print i, ' tasks put line 191 mutiroc --><END'

    # 3X --> End
    # Wait for all of the tasks to finish
    tasks.join()



    ########## Four ##########
    #
    # 4 --> Results
    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result Q Results: ', result
        num_jobs -= 1

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




def run_multiproccesses_magick(searchdir=None):
    import multiprocessing
    import glob,os
    #import jbmodules
    import image_processing
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
