#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main(styles_list, imgnum=1, ext='.png', root_dir='/mnt/images'):
    from os import getcwd, environ, path, chdir
    import sys
    MOZU_CODE_DIR = '/usr/local/batchRunScripts/mozu'
    JBMODULES_ROOT = '/usr/local/batchRunScript/python/jbmodules'
    chdir(MOZU_CODE_DIR)
    sys.path.append(MOZU_CODE_DIR)
    sys.path.append(JBMODULES_ROOT)
    import db, mozu_image_util_functions, mozu_exec
#####
    #
    #######
    #######
    environ['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://MZIMG:m0zu1mages@borac102-vip.l3.bluefly.com:1521/bfyprd12'
    #environ['PRD_ENV'] = "1"
    # environ['PYDEBUG'] = "1"
    print('Starting.\nReloading {0} Images for {1} Styles from {2} to Mozu'.format(ext.lstrip('.').upper(), len(styles_list), root_dir))
    if imgnum > 1 and imgnum <= 6:
        ext= "alt0{0}{1}".format(str(imgnum-1), ext)
    else:
        ext = ext
    flist = []
    for fname in styles_list:
        print 'PreCond ', root_dir,fname+ext
        if fname is not None:
            src = path.join(root_dir, fname[:4], fname + ext) #.replace('\n',' ').replace('\r','').replace('  ',' ')
            #from RESTClient import MozuRestClient
            #rest_client = MozuRestClient()
            #resp = rest_client.send_content(src_filepath=src)
            print src,'\n^^src^^\nfname+ext-vv', fname, '\t', ext
            flist.append(src)

    loaded_filenames = [f.split('/')[-1].split('.')[0] for f in flist if f is not None]
    mozu_exec.main(flist)
    print('Finished.\nReloaded {0} Images for {1} Styles from {2} to Mozu'.format(ext.lstrip('.').upper(), len(flist), root_dir))
    return loaded_filenames



if __name__ == '__main__':
    from sys import argv
    if len(argv[1]) == 1:
        main(argv[2:], imgnum=argv[1])
    else:
        main(argv[1:])
