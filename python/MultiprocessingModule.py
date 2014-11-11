#!/usr/bin/env python
#-*- coding: utf-8 -*-

def run_multiproccesses_magick(searchdir=None, magickProc=None):
    import multiprocessing
    import glob,os
    if not magickProc:
        import magicColorspaceModAspctLoad.main as magickProc
    else:
        import magickProc as magickProc

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

    if os.path.isdir(directory_list[0] 
    results = pool.map(magickProc,directory_list)
    print results
    
    # close the pool and wait for the work to finish
    pool.close()
    print 'PoolClose'
    pool.join()
    print 'PoolJoin'

if __name__ == '__main__':
    run_multiproccesses_magick()