#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return



class Task(object):
    def __init__(self, img, rgbmean, destdir):
        self.img = img
        self.rgbmean = rgbmean
        self.destdir = destdir
    def __call__(self):
        from image_processing import marketplace, magick_tweaks
        import image_processing.marketplace.magicColorspaceModAspctLoadFaster2 as magickProc2
        import mongo_tools
        #time.sleep(0.1) # pretend to take some time to do the work
        magick_tweaks.convert_img_srgb.main(image_file=self.img)
        ## Add to Mongo DB
        # try:
        #     mongo_tools.mongo_image_prep.update_gridfs_extract_metadata(self.img, db_name='gridfs_mrktplce')
        # except:
        #     mongo_tools.mongo_image_prep.insert_gridfs_extract_metadata(self.img, db_name='gridfs_mrktplce')
        ## Generate png from source then jpgs from png
        pngout = magickProc2.subproc_magick_png(self.img, rgbmean=dict(self.rgbmean), destdir=self.destdir)
        magickProc2.subproc_magick_large_jpg(pngout, destdir=self.destdir)
        magickProc2.subproc_magick_medium_jpg(pngout, destdir=self.destdir)
        return '%s -- %s' % (self.img, self.destdir)
    def __str__(self):
        return '%s -- %s' % (self.img, self.destdir)


def run_threaded_mongo_upsert(argslist=None):
    import Queue
    import threading
    import multiprocessing
    import mongo_tools
    from image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import sort_files_by_values
    from mongo_tools.mongo_image_prep import insert_gridfs_extract_metadata, update_gridfs_extract_metadata
    qmongo = Queue.Queue()
    # print type(argslist), len(argslist), ' type and length argslist \n'
    print type(argslist), type(argslist)
    for i in argslist: #put 30 tasks in the queue
        print i, ' argslist'
        if i:
            qmongo.put([i])


    # img_dict_list = []
    # def worker():
    #     count = 0
    #     while True:
    #         item = q.get()
    #         print item
    #         imgdata = sort_files_by_values([item])
    #         img_dict_list.append(imgdata)
    #         insertres =  mongo_tools.mongo_image_prep.insert_gridfs_extract_metadata(item)
    #         count += 1
    #         print count, ## '\n\t', imgdata
    #         q.task_done()

    def mongoworker():
        count = 0
        while True:
            item = qmongo.get()
            print item
            try:
                insertres =  jbmodules.mongo_image_prep.insert_gridfs_extract_metadata(item)
            except:
                insertres =  jbmodules.mongo_image_prep.update_gridfs_extract_metadata(item)
            count += 1
            print count, insertres ## '\n\t', imgdata
            qmongo.task_done()


    print 'argsMONGO ', argslist[0], type(argslist), ' Type ArgsList RunMONGOThreaded'
    jobcount=len(argslist) #detect number of cores
    print("Creating %d threads for the MongoMachine" % jobcount)
    for i in xrange(jobcount):
        t = threading.Thread(target=worker)
        tmongo.daemon = True
        tmongo.start()

    qmongo.join() #block until all tasks are done
    return



def run_threaded(argslist=None):
    import Queue
    import threading
    import multiprocessing
    import mongo_tools
    from image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import sort_files_by_values
    from mongo_tools.mongo_image_prep import insert_gridfs_extract_metadata, update_gridfs_extract_metadata
    q = Queue.Queue()
    # print type(argslist), len(argslist), ' type and length argslist \n'
    print type(argslist), type(argslist)
    for i in argslist: #put 30 tasks in the queue
        print i, ' argslist'
        if i:
            q.put([i])


    #qmongo = q
    img_dict_list = []
    def worker():
        count = 0
        while True:
            item = q.get()
            print item
            imgdata = sort_files_by_values([item])
            img_dict_list.append(imgdata)
            insertres =  mongo_tools.mongo_image_prep.insert_gridfs_extract_metadata(item)
            count += 1
            print count, ## '\n\t', imgdata
            q.task_done()

    #     def mongoworker():
    #         count = 0
    #         while True:
    #             item = qmongo.get()

    #             print item
    #             insertres =  jbmodules.mongo_image_prep.insert_gridfs_extract_metadata(item)
    #             count += 1
    #             print count, insertres ## '\n\t', imgdata
    #             qmongo.task_done()

    print 'argsL ', argslist[0], type(argslist), ' Type ArgsList RunThreaded'
    jobcount=len(argslist) #detect number of cores
    print("Creating %d threads" % jobcount)
    for i in xrange(jobcount):
        t = threading.Thread(target=worker)
        #tmongo = threading.Thread(target=mongoworker)

        t.daemon = True
        t.start()
        #tmongo.daemon = True
        #tmongo.start()

    q.join() #block until all tasks are done
    return img_dict_list


def funkRunner(root_img_dir=None):
    import multiprocessing
    #import Queue
    import threading
    import glob, os.path
    import image_processing
    from image_processing.marketplace.magicColorspaceModAspctLoadFaster2 import rename_retouched_file, sort_files_by_values
    destdir = '/mnt/Post_Comnplete/ImageDrop'

    # Enqueue jobs
    poolRename = multiprocessing.Pool(8)
    images = [ f for f in (glob.glob(os.path.join(root_img_dir,'*.??[gG]')))]
    resrename = poolRename.map(rename_retouched_file, images)
    poolRename.close()
    poolRename.join()
    print 'Images Renamed'
    #poolDict = multiprocessing.Pool(num_consumers)
    #images_renamed = [ f for f in (glob.glob(os.path.join(root_img_dir,'*.??[gG]')))]

    img_list =  glob.glob(os.path.join(root_img_dir,'*.??[gG]'))
    print type(img_list)
    print '\tLen ImageList preThreaded'

    img_dict = run_threaded(argslist=(img_list,))
    mongo_res = run_threaded_mongo_upsert(argslist=(img_list,))  


    print len(img_list)
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [ Consumer(tasks, results)
                  for i in xrange(num_consumers) ]
    for w in consumers:
        w.start()

    print 'RGB MEan Info', type(img_dict), ' len ', len(img_dict)
    num_jobs = len(img_dict)
    print num_jobs, consumers, root_img_dir
    for item in img_dict:
        for img, rgbmean in item.items():
            print img, rgbmean, ' Img -- RGB Mean'
            tasks.put(Task(img, rgbmean.values(), destdir))
    print 'Put Tasks'

    # Add a poison pill for each consumer
    for i in xrange(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1
    #return


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
