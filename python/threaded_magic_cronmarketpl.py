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
import magicColorspaceModAspctLoad as magickProc

class Loader(object):

    def threadLoad(self,directory_list):
        for directory in directory_list:
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
    directory_list = []
    sorted([directory_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*/*')) if os.path.isdir(g)])
    print searchdirs, 'rootdir',searchdir,  'dirlist',directory_list
    load = Loader()
    threads = [threading.Thread(target=load.threadLoad, args=(tuple(directories,), ))
               for directories in [directory_list]]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    load.finishUp()


if __name__ == '__main__':
    main()
