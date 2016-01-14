#!/usr/bin/env python
# coding: utf-8
#import pdb;pdb.set_trace()

 ## Listing and Info about Document List
#######################################
import sqlalchemy
from mozu_image_util_functions import include_keys, log
from RESTClient import __mozu_image_table_valid_keys__
##
## forcing db and config settings test without to see if this is even used
# from os import environ
# environ['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://MZIMG:m0zu1mages@borac102-vip.l3.bluefly.com:1521/bfyprd12'
# environ['PRD_ENV'] = '1'
# globals()['PRD_ENV'] = 1


def cmd_line_argument_parse():
    import argparse

    parser = argparse.ArgumentParser(description='Perform actions on Images to/from Bfly/Mozu',
                                     prefix_chars='-+/',
                                     add_help=True,
                                     #version='1.1.0',
                                     )

   # parser.add_argument('--mode', choices=('insert', 'search', 'update', 'delete'), default='insert')
    parser.add_argument('-d', action="store_false", default=None,
                    help='Turn delete_flag OFF',
                    )
    parser.add_argument('+d', action="store_true", default=None,
                    help='Turn delete_flag ON',
                    )
    parser.add_argument('-u', action="store_false", default=None,
                    help='Turn update_flag OFF',
                    )
    parser.add_argument('+u', action="store_true", default=None,
                    help='Turn update_flag ON',
                    )
    #parser.add_argument('//noarg', '++noarg', action="store_true", default=False)
    parser.add_argument('-F', action='append_const', dest='const_collection',
                    const='value-1-to-append',
                    default=[],
                    help='Use the F flag to Add different style numbers as a list to run commands on')
    parser.parse_args('-d+d-u+u-F'.split())
    res = parser.parse_args()

    return vars(res)



### GET Images - Content
#
# def download_document_content(outfile=None, **kwargs):
#     from RESTClient import MozuRestClient
#     print kwargs, 'KWARGS-26'
#     mzclient = MozuRestClient(**kwargs)
#     from os import path as path
#     image_content = mzclient[     if not mzclient.bf_imageid:
#         # Get bflyid from Oracle using mz_id
#         from db import mozu_image_table_instance
          #mozu_image_table = mozu_image_table_instance()
#         bf_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.mz_imageid == mzclient.mz_imageid) ) ).execute().fetchone()['bf_imageid']
#         mzclient.bf_imageid = bf_imageid
#     if not outfile:
#         outfile = path.join('/tmp', mzclient.bf_imageid)
#     else: pass
#     with open(outfile,'w') as f:
#         f.write(image_content)
#     print locals(), "Downloaded Content"
#     return path.abspath(outfile)
#
#
# def read_document_content_headers(**kwargs):
#     from RESTClient import MozuRestClient
#     print kwargs, 'KWARGS-47'
#     mzclient = MozuRestClient(**kwargs)
#     image_data = mzclient.headers
#     print image_data
#     return image_data




if __name__ == '__main__':
    import sys
    from os import path
    insert_list = []
    #kwarguments = cmd_line_argument_parse()
    #print kwarguments
    update_flag = False
    delete_flag = False
    if sys.argv[1].upper() == 'U' or sys.argv[1].upper() == 'D':

        if path.isfile(sys.argv[2]):
            fpath = sys.argv[2]
            deletename = path.basename(fpath).split('.')[0]
            print 'Deleting 1 ', deletename
            sys.argv[1] = fpath
            print 'SettingSysArg1 - 1 ', sys.argv[1]
        elif len(sys.argv[2]) == 9:
            print 'Deleting 2 ', sys.argv[2]
            sys.argv[1] = path.join('/mnt/images/', sys.argv[2][:4], sys.argv[2] + '.png')
            print 'SettingSysArg1 - 2 ', sys.argv[1]
        else:
            raise NameError
        from mozu_exec_del_update import delete_by_mozuid
        #res = delete_by_mozuid(sys.argv[1])
        if sys.argv[1].upper() == 'U':
            update_flag = True
            print 'Update Flag Set ', sys.argv[1]
        elif sys.argv[1].upper() == 'D':
            delete_flag = True
            print 'Delete Flag Set ', sys.argv[1]
    if update_flag and not delete_flag:
        print "Delete NOT Set or Update Flag Set Continuing with reload or reload Of -->  {}".format(sys.argv[1])
        try:
            if path.isfile(path.abspath(sys.argv[1])):
                for arg in sys.argv[1:]:
                    insert_list.append(arg)  # '/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
            insert_list_filepaths = list(set(sorted(insert_list)))
            print "filelist_length", len(insert_list_filepaths), insert_list_filepaths
            main(fileslist=insert_list_filepaths)
        except IndexError:
            print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args{}".format(locals())
            cmd_line_argument_parse()
