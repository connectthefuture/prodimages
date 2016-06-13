#!/usr/bin/env python
#-*- coding: utf-8 -*-

import multiprocessing
from Queue import Empty

### Date Defs
from os import chdir, path, curdir, makedirs, environ
import datetime, glob, shutil

######
todaysdatefullsecs = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
todaysdatefull = todaysdatefullsecs[:12]
todaysdate = todaysdatefull[:8] # '{:%Y,%m,%d}'.format(datetime.datetime.now())
todaysdatearch = todaysdatefull # '{:%Y,%m,%d,%H,%M}'.format(datetime.datetime.now())
archive = '/mnt/Post_Complete/Complete_Archive/images'
archive_uploaded_day = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""))
mozu_sending_dir = environ.get('MOZU_HIERARCHY', '/mnt/Post_Complete/Complete_Archive/MozuRoot')
mozu_log_dir = path.join(mozu_sending_dir, 'log')

try:
    makedirs(mozu_log_dir)
    #makedirs(mozu_sending_dir)
    #makedirs(imgdest_jpg_mozu)
    #makedirs(imgdest_jpg_mozu_loaded)
except OSError:
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
        import sys
        sys.path.append('/usr/local/batchRunScripts/python/jbmodules/image_processing/marketplace_dev')
        self.img = img
        self.rgbmean = rgbmean
        self.destdir          = destdir
        self.mozu_sending_dir = mozu_sending_dir
        self.mozu_log_dir = mozu_log_dir
        self.pngout           = ''
        self.mozu_out         = ''

    def __call__(self):
        import magicColorspaceModAspctLoadFaster2 as magickProc2
        import convert_img_srgb
        convert_img_srgb.main(image_file=self.img)
        print self.img, ' <-- self.img ', self.rgbmean
        try:
            if self.mozu_sending_dir:
                _mozu_send_subdir = path.join(self.mozu_sending_dir, self.img.split('/')[-1][:4])
                try:
                    makedirs(_mozu_send_subdir)
                except Exception, e:
                    pass
                self.mozu_out = magickProc2.subproc_magick_png(self.img, rgbmean=self.rgbmean, destdir=_mozu_send_subdir)
                with open(path.join(self.mozu_log_dir, todaysdate + '_index.txt'), mode='a+') as fwrite:
                    logged_line = '{0}\t{1}\t{2}'.format('{:%Y%m%d%H%M%S}'.format(datetime.datetime.now()), 'PROCESSED', self.mozu_out)
                    fwrite.write(logged_line)
            self.pngout = magickProc2.subproc_magick_png(self.img, rgbmean=self.rgbmean, destdir=self.destdir)
            ## TODO: Possible insertion of Mozu and/or GoogleDrive upload and key exchange
            ## COPY TO MOZU DAILY DIR DEFINED AS GLOBAL ABOVE
            #shutil.copy2(self.pngout, imgdest_jpg_mozu)
            if self.mozu_out:
                magickProc2.subproc_magick_large_jpg(self.mozu_out, destdir=self.destdir)
                ret = magickProc2.subproc_magick_medium_jpg(self.mozu_out, destdir=self.destdir)
            else:
                magickProc2.subproc_magick_large_jpg(self.png_out, destdir=self.destdir)
                ret = magickProc2.subproc_magick_medium_jpg(self.png_out, destdir=self.destdir)

            return '-ret- %s \n-path- %s \n-dest- %s \n' % (ret, self.img, self.destdir)
            #except TypeError:
            #    print 'TypeError in __call__'
            #    pass
        except ImportError:
            import os
            print 'Import Error multiprocmagick2:69'
            os.remove(self.pngout[1])
        except TypeError:
            print self.img, ' <-- Type-Error in Task -->', self.destdir
            pass
        except IndexError:
            ' None Type Error End '
            pass
        except AttributeError, e:
            import os
            print 'Attribute error creating png in Consumer Manager, bad download expected\n', e
            try:
                os.remove(self.img)
                print '\n\tDeleted {0} due to Attrib None Type error'.format(self.img)
            except:
                print 'Failed Removal in Consumer Manager'

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
