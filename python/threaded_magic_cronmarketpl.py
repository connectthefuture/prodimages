#!/usr/bin/env python
# -*- coding: utf-8 -*-

# maxconnections = 5
# # ...
# pool_sema = BoundedSemaphore(value=maxconnections)

# Once spawned, worker threads call the semaphore’s acquire and release methods when they need to connect to the server:

# with pool_sema:
#     conn = connectdb()
#     try:
#         # ... use connection ...
#     finally:
#         conn.close()

import subprocess
import threading
import magicColorspace_modulate-aspect-normalize_AND_Upload as magickProc

class Loader(object):
    def __init__(self, directory_list, **kargs):
        #self.__main__
        self.directory_list = directory_list

    def threadLoad(self):
        for directory in self.directory_list:
            load_cmd =  magickProc.main(root_img_dir=directory) # load command
            run = subprocess.Popen(load_cmd, shell=True)
            # block until subprocess is done
            run.communicate()
        name = threading.current_thread().name
        print "finished running {n}".format(n=name)

    def finishUp(self):
        print 'finishing up'


import glob,os,threading
def main(searchdir=None):
    load = Loader()
    threads = [threading.Thread(target=load.threadLoad, args=(directory_list, ))
               for directory_list in [directory_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*/*')) if os.path.isdir(g)]]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    load.finishUp()


if __name__ == '__main__':
    main()
