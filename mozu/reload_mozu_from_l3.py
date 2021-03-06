#!/usr/bin/env python
# -*- coding: utf-8 -*-

## root_dir must have structure .ie <root_dir>/8888/888888888.png
def create_list_files_to_send(styles_list, imgnum=0, ext='.png', root_dir='/mnt/images'):
    from os import environ, path, chdir
    environ['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://MZIMG:m0zu1mages@borac102-vip.l3.bluefly.com:1521/bfyprd12'
    # environ['PRD_ENV'] = "1"
    # environ['PYDEBUG'] = "1"
    #
    import sys
    MOZU_CODE_DIR = '/usr/local/batchRunScripts/mozu'
    sys.path.append(MOZU_CODE_DIR)
    chdir(MOZU_CODE_DIR)
    #######

    if 1 < imgnum <= 6:
        ext= "_alt0{0}{1}".format(str(imgnum-1), ext)
    else:
        ext = ext
    print ext, imgnum, ' <--- ext and imgnum'
    flist = []
    if 0 < imgnum <= 6:
        for style in styles_list:
            #print 'PreCond ', root_dir,style+ext
            if style is not None:
                src = path.join(root_dir, style[:4], style + ext).replace('\n',' ').replace('\r','').replace('  ',' ')
                #from RESTClient import MozuRestClient
                #rest_client = MozuRestClient()
                #resp = rest_client.send_content(src_filepath=src)
                #print len(src), len(src[0]),'\n^^src^^\nstyle+ext-vv', style, '\t', ext
                flist.append(src)
    return flist


def main(styles_list):
    from os import environ
    ##### Temp ####
    environ['IMGDIR'] = '/mnt/images'
    ## ************* ##
    imgnum = int(environ.get('IMGNUM', 0))
    root_dir = environ.get('IMGDIR', '/mnt/Post_Complete/MozuRoot')
    ext = environ.get('IMGEXT','.png')
    ## Do for only 1 img number or load any that are found
    if imgnum > 0:
        flist = create_list_files_to_send(styles_list, imgnum=imgnum, ext=ext, root_dir=root_dir)
    else:
        flist = []
        for x in range(1,7,1):
            li1 = create_list_files_to_send(styles_list, imgnum=x, ext=ext, root_dir=root_dir)
            [ flist.append(f) for f in li1 if f is not None ]
    ####
    ## Compile Actual Styles and Filename found and Ready to Send
    loaded_filenames = [f.split('/')[-1].split('.')[0] for f in flist if f is not None]
    loaded_styles = list(set(sorted([fn[:9] for fn in loaded_filenames if fn is not None])))
    print 'loaded styles', loaded_styles
    ### Send Collected to Mozu
    import mozu_exec
    print('Starting.\nReloading {0} Images for {1} Styles from {2} to Mozu'.format(ext.lstrip('.').upper(), len(styles_list), root_dir))
    mozu_exec.main(flist)
    print('Finished.\nReloaded {0} Images for {1} Styles\n{2} Total Files from {3} to Mozu'.format(ext.lstrip('.').upper(), len(loaded_styles), len(loaded_filenames),root_dir))

    ## Set Media Version for Loaded Styles
    import media_version_ctrl
    media_version_ctrl.batch_process_by_style_list(loaded_styles)
    print('Finished.\nMedia Incr for {1} Styles from {2} to Mozu'.format(ext.lstrip('.').upper(), len(loaded_styles), root_dir))
    ## Return File Path of Loaded Styles for further ops if needed
    return loaded_filenames



if __name__ == '__main__':
    from sys import argv
    args=argv[1:]
    main(args)
