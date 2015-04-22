#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import multiprocessing
from Queue import Empty

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
        import os
        from jbmodules import image_processing
        from jbmodules.image_processing import marketplace, magick_tweaks
        import jbmodules.image_processing.marketplace.magicColorspaceModAspctLoadFaster2 as magickProc2
        import jbmodules.image_processing.magick_tweaks.convert_img_srgb
        ret = ''
        jbmodules.image_processing.magick_tweaks.convert_img_srgb.main(image_file=self.img)
        print self.img, ' <-- self.img ', self.rgbmean
        pngout = magickProc2.subproc_magick_png(self.img, rgbmean=self.rgbmean, destdir=self.destdir)
        magickProc2.subproc_magick_large_jpg(pngout, destdir=self.destdir)
        ret = magickProc2.subproc_magick_medium_jpg(pngout, destdir=self.destdir)
        return '%s -- %s' % (ret, self.img, self.destdir)

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
