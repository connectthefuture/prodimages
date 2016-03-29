#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main(styles_list, ext='.png', root_dir='/mnt/images'):
    from os import getcwd, environ, path, chdir
    MOZU_CODE_DIR = '/usr/local/batchRunScripts/mozu'
    JBMODULES_ROOT = '/usr/local/batchRunScript/python/jbmodules'
    chdir(MOZU_CODE_DIR)
    print getcwd()

    environ['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://MZIMG:m0zu1mages@borac102-vip.l3.bluefly.com:1521/bfyprd12'
    environ['PRD_ENV'] = "1"
    # environ['PYDEBUG'] = "1"
    print('Starting.\nReloading {0} Images for {1} Styles from {2} to Mozu'.format(ext.lstrip('.').upper(), len(styles_list), root_dir))

    import db, mozu_image_util_functions
    flist = []
    for fname in styles_list.split():
        if fname is not None:
            src = path.join(root_dir, fname[:4], fname + ext)
            #from RESTClient import MozuRestClient
            #rest_client = MozuRestClient()
            #resp = rest_client.send_content(src_filepath=src)
            flist.append(src)

    import mozu_exec
    mozu_exec.main(fileslist=flist)
    print('Finished.\nReloaded {0} Images for {1} Styles from {2} to Mozu'.format(ext.lstrip('.').upper(), len(styles_list), root_dir))
    loaded_filenames = [f.split('/')[-1].split('.')[0] for f in flist if f is not None]
    return loaded_filenames



if __name__ == '__main__':
    from sys import argv
    main(styles_list=argv[1:])
