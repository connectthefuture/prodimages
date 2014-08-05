#!/usr/bin/env python
# -*- coding: utf-8 -*-

def run_multiproccesses_magick(searchdir=None):
	from multiprocessing import Pool
    from multiprocessing.dummy import Pool as ThreadPool 
    import magicColorspaceModAspctLoad as magickProc

    pool = ThreadPool(4)
    if not searchdir:
        searchdir = os.path.abspath('/mnt/Post_Complete/Complete_Archive/MARKETPLACE')
    else:
        pass
    directory_list = []
    [ directory_list.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*/*')) if os.path.isdir(g) ]

    results = pool.map(magickProc.main,directory_list)
    print results
    # close the pool and wait for the work to finish
    pool.close()
    print 'PoolClose'
    pool.join()
    print 'PoolJoin'

if __name__ == '__main__':
    run_multiproccesses()