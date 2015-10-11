#!/usr/bin/env python
#-*- coding: utf-8 -*-

def img_return_md5(fname):
    import hashlib
    md5 = hashlib.md5()
    with open(fname,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            md5.update(chunk)
    return md5.hexdigest()

def run_multiproccesses_magick(searchdir=None, magickProc=None):
    import multiprocessing
    import glob,os
    if not magickProc:
        import magicColorspaceModAspctLoad as magickProc
    else:
        print magickProc
        import magickProc as magickProc

    if not searchdir:
        #searchdir = os.path.abspath('.')
        print 'NO Directory to Search'
    else:
        pass

    pool = multiprocessing.Pool(4)
    multiproc_items = []
    if searchdir.split('/')[-1][:3] == 'jpg':
        [ multiproc_items.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*.jpg')) if os.path.isfile(g) ]
    elif searchdir.split('/')[-1][:3] == 'png':
        [ multiproc_items.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*.png')) if os.path.isfile(g) ]        
        print 'Image Clipping Import', searchdir
    elif searchdir.split('/')[-1][:3] == 'out':
        [ multiproc_items.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*.*')) if os.path.isfile(g) ] 
    else:
        [ multiproc_items.append(os.path.abspath(g)) for g in glob.glob(os.path.join(searchdir, '*/*')) if os.path.isdir(g) ]

    results = ''
    if multiproc_items:
        try:
            results = pool.map(magickProc.main,multiproc_items)
        except:
            results = pool.map(magickProc,multiproc_items)
        # close the pool and wait for the work to finish
        pool.close()
        print 'PoolClose'
        pool.join()
        print 'PoolJoin'
    else:
        print 'Processor Failed'
    
    if results:
        print results
        return results


if __name__ == '__main__':
    run_multiproccesses_magick()