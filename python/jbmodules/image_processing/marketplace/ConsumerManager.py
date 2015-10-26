#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import multiprocessing
from Queue import Empty

### Date Defs
from os import chdir, path, curdir
import datetime, glob, shutil

######
todaysdatefullsecs = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
todaysdatefull = todaysdatefullsecs[:12]
todaysdate = todaysdatefull[:8] # '{:%Y,%m,%d}'.format(datetime.datetime.now())
todaysdatearch = todaysdatefull # '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())
archive_uploaded_day = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""))
globals imgdest_jpg_mozu
imgdest_jpg_mozu = path.join(archive_uploaded_day, 'JPG_MOZU_LOAD')

try:
    os.makedirs(imgdest_jpg_mozu, 16877)
except:
    pass


class Consumer(multiprocessing.Process):

    def __init__(self, tasks, results, consumers_finished):
        # self.process_data =
        multiprocessing.Process.__init__(self)
        self.tasks = tasks
        self.results = results
        self.consumers_finished = consumers_finished
        #self.process_data = self.process_data()

    def run(self):
        while not all(flag for flag in self.consumers_finished.values()):
            try:
                task = self.tasks.get(False)
                self.consumers_finished[self.name] = False
            except Empty:
                self.results.put("STOP")
                self.consumers_finished[self.name] = True
            else:
                task_result = self.process_data(task)
                self.results.put(task_result)

    def process_data(self, task):
        print "Processing %s" % task
        res = task()
        return res


class Task(object):
    def __init__(self, img, rgbmean, destdir):
        import tempfile, shutil
        self.img = img
        self.rgbmean = rgbmean
        self.destdir = destdir

    def __call__(self):
        import jbmodules
        import os, shutil
        from jbmodules import image_processing
        from jbmodules.image_processing import marketplace, magick_tweaks
        import jbmodules.image_processing.marketplace.magicColorspaceModAspctLoadFaster2 as magickProc2
        import jbmodules.image_processing.magick_tweaks.convert_img_srgb
        jbmodules.image_processing.magick_tweaks.convert_img_srgb.main(image_file=self.img)
        print self.img, ' <-- self.img ', self.rgbmean
        pngout = magickProc2.subproc_magick_png(self.img, rgbmean=self.rgbmean, destdir=self.destdir)
        ## TODO: Possible insertion of Mozu and/or GoogleDrive upload and key exchange
        ## COPY TO MOZU DAILY DIR DEFINED AS GLOBAL ABOVE
        shutil.copy2(pngout, imgdest_jpg_mozu)
        magickProc2.subproc_magick_large_jpg(pngout, destdir=self.destdir)
        ret = magickProc2.subproc_magick_medium_jpg(pngout, destdir=self.destdir)
        # try:
        #     ############################
        #     ###### mozu
        #     ############################
        #     import sys, datetime
        #     from os import chdir, path, makedirs
        #     todaysdatefullsecs = '{:%Y%m%d_%H%M%S}'.format(datetime.datetime.now())
        #     tmp_mozu_loading = os.path.join("/mnt/Post_Complete/Complete_Archive/.tmp_mozu_loading" , "tmp_" + str(todaysdatefullsecs).replace(",", ""))
        #     if path.isdir(tmp_mozu_loading):
        #         pass
        #     else:
        #         try:
        #             os.makedirs(tmp_mozu_loading, 16877)
        #         except:
        #             print " Error", tmp_mozu_loading
        #     chdir('/usr/local/batchRunScripts/mozu')
        #     import mozu_exec, mozu_image_util_functions
        #     ## Compress and convert to jpg
        #     if path.isfile(pngout):
        #         print ' Is file PNGOUT', pngout, img
        #         jpgout = mozu_image_util_functions.magick_convert_to_jpeg(pngout,destdir=tmp_mozu_loading)
        #     else:
        #         #pass
        #         jpgout = mozu_image_util_functions.magick_convert_to_jpeg(self.img,destdir=tmp_mozu_loading)
        #     mozu_exec.main(jpgout)
        #     ############################
        # except ImportError:
        #     print 'Import Error multiprocmagick2:69'
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
        #except TypeError:
        #    print 'TypeError in __call__'
        #    pass

    def __str__(self):
        return '%s -- %s' % (self.img, self.destdir)




class Starter(object):

    def __init__(self, **kwargs):
        self.img_dict = kwargs.get('img_dict')
        self.destdir = kwargs.get('destdir')

    def start(self):
        manager = multiprocessing.Manager()

        tasks = manager.Queue()
        results = manager.Queue()
        consumers_finished = manager.dict()
        num_consumers = multiprocessing.cpu_count() - 2
        consumers = [Consumer(tasks, results, consumers_finished) for i in xrange(num_consumers)]

        # Tasks Add
        # Add Images and rgb data and dest to tasks
        num_jobs = len(self.img_dict)
        # print 'jobs -- consumers -- root_img_dir --> ', num_jobs, consumers, root_img_dir
        for item in self.img_dict:
            img, rgbmean = item.keys()[0], item.values()  #.items()
            #print img, 'rgbmean', ' Img -- RGB Mean'
            tasks.put(Task(img, rgbmean, self.destdir))

        for consumer in consumers:
            consumers_finished[consumer.name] = False
            consumer.start()

        for consumer in consumers:
            consumer.join()

        for r in iter(results.get, "STOP"):
            print r

if __name__ == "__main__":
    s = Starter()
    s.start()
