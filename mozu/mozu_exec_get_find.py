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


### Count with query params
@log
def count_total_files_documents(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    if not kwargs.get('page_size'):
        returned_item_count = mzclient.get_mz_image_document_list()['totalCount']
    else:
        returned_item_count = mzclient.get_mz_image_document_list(**kwargs)['totalCount']
    print "Total Files in DocumentList: {}".format(returned_item_count)
    return returned_item_count

## Find Docs using query
@log
def list_documents(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    documents = mzclient.get_mz_image_document_list()['items']
    return documents

## Get a list of docs
@log
def resource_documents_list(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    documents_list = mzclient.get_mz_image_document_list()
    return documents_list


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



### Runs like
# >>>> reslist = get_mozu_or_bf_id(styles_list=styles_list[:999]).execute().fetchall()
################
def get_mozu_or_bf_id(mz_imageid=None,bf_imageid=None,styles_list=None):
    from os import chdir, path, curdir
    try:
        chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
        print 'Executing from ', path.abspath(curdir), bf_imageid, mz_imageid
    except:
        print 'Failed  from ', path.abspath(curdir)
    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    if styles_list:
        ret = mozu_image_table.select(whereclause=( (mozu_image_table.c.bf_imageid.in_( tuple(styles_list) )))).execute()
        print 'FZero'
        return ret.fetchall()
    elif bf_imageid:
        ret = mozu_image_table.select(whereclause=( (mozu_image_table.c.bf_imageid.like("{}".format(bf_imageid) )))).execute()
        print 'F1', ret.fetchone()
        return ret.fetchone()
    elif mz_imageid:
        ret = mozu_image_table.select(whereclause=( (mozu_image_table.c.bf_imageid.like("{}".format(bf_imageid) )))).execute()
        print 'F2'
        return ret.fetchone()
    else:
        return

## This shouldnt work unless something is duplicated in the db and most likely in mozu, ie. style_l.jpg, style.png both "name" fields are just style
def get_multi_mzid_by_bf_imageid(bf_imageid):
    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    ret = mozu_image_table.select(whereclause=( (mozu_image_table.c.bf_imageid.like("%{}".format(bf_imageid) )))).execute()
    return ret.fetchall()



## Want to eventually use arg parser above
if __name__ == '__main__':
    import sys
    from os import path
    insert_list = []
    #kwarguments = cmd_line_argument_parse()
    #print kwarguments
    # update_flag = False
    # delete_flag = False
    # if sys.argv[1].upper() == 'U' or sys.argv[1].upper() == 'D':
    #
    #     if path.isfile(sys.argv[2]):
    #         fpath = sys.argv[2]
    #         deletename = path.basename(fpath).split('.')[0]
    #         print 'Deleting 1 ', deletename
    #         sys.argv[1] = fpath
    #         print 'SettingSysArg1 - 1 ', sys.argv[1]
    #     elif len(sys.argv[2]) == 9:
    #         print 'Deleting 2 ', sys.argv[2]
    #         sys.argv[1] = path.join('/mnt/images/', sys.argv[2][:4], sys.argv[2] + '.png')
    #         print 'SettingSysArg1 - 2 ', sys.argv[1]
    #     else:
    #         raise NameError
    #     from mozu_exec_del_update import delete_by_mozuid
    #     #res = delete_by_mozuid(sys.argv[1])
    #     if sys.argv[1].upper() == 'U':
    #         update_flag = True
    #         print 'Update Flag Set ', sys.argv[1]
    #     elif sys.argv[1].upper() == 'D':
    #         delete_flag = True
    #         print 'Delete Flag Set ', sys.argv[1]
    # if update_flag and not delete_flag:
    #     print "Delete NOT Set or Update Flag Set Continuing with reload or reload Of -->  {}".format(sys.argv[1])
    #     try:
    #         if path.isfile(path.abspath(sys.argv[1])):
    #             for arg in sys.argv[1:]:
    #                 insert_list.append(arg)  # '/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
    #         insert_list_filepaths = list(set(sorted(insert_list)))
    #         print "filelist_length", len(insert_list_filepaths), insert_list_filepaths
    #         main(fileslist=insert_list_filepaths)
    #     except IndexError:
    #         print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args{}".format(locals())
    #         cmd_line_argument_parse()
