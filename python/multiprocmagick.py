#!/usr/bin/env python
#-*- coding: utf-8 -*-

def run_multiproccesses_magick(searchdir=None):
    import magicColorspaceModAspctLoad as magickProc
    import multiprocessing
    import glob,os
    
    pool = multiprocessing.Pool(4)
    if not searchdir:
        searchdir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE/SWI')
    else:
        pass

    directory_list = []
    if searchdir.split('/')[-1]) == 'SWI':
        [ directory_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*')) if os.path.isdir(g) ]
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