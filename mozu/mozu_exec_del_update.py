#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'

 ## Listing and Info about Document List
#######################################
import sqlalchemy
from mozu_image_util_functions import include_keys, log
from RESTClient import __mozu_image_table_valid_keys__

#### Initially written in ipython notebook for testing
# ## recent aka highest colorstyle number
# def delete_most_recent_images(page_size="200"):
#     from os import chdir, path, curdir
#     chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
#     print 'Executing from ', path.abspath(curdir)
#
#     from RESTClient import MozuRestClient
#     from db import mozu_image_table_instance
#     client = MozuRestClient()
#     mozu_image_table = mozu_image_table_instance()
#     documents = client.get_mz_image_document_list()  ##[0]['items']
#
#     for x in documents['items']:
#         # Delete Mozu First then db
#         resp = delete_document_data_content(mz_imageid=x['id']) #, page_size="200") # ['id']# = documents.get('items')[0]
#         mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == x['id']) )).execute()
#         import json
#         return json.dumps(x.items())


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

# @log
# # PUT - Upload/Update Image/DocumentContent
def update_content_mz_image(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    mzclient = MozuRestClient(**kwargs)
    content_response = mzclient.send_content(**kwargs)
    print content_response.headers, "Update Mozu Content"
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    update_db = mozu_image_table.update(values=dict(**table_args))
    print content_response.headers, "Update DB MZ_IMAGE"
    return content_response


# DELETE - Delete Image/DocumentContent - Everything
@log
def delete_document_data_content(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    mzclient = MozuRestClient(**kwargs)
    delete_resp = mzclient.delete_mz_image()
    mozu_image_table = mozu_image_table_instance()

    delete_db = mozu_image_table.delete( whereclause=(mozu_image_table.c.mz_imageid == kwargs.get('mz_imageid')) )
    # res = delete_db.execute()
    print delete_resp.headers, "Delete \n", delete_db, "\nMZ CLIENTID in FUNCtion: ", kwargs
    return delete_resp

# Delete doc content and db entry using mzid to query db
def delete_by_mozuid(mz_imageid=None):
    from os import chdir, path, curdir
    try:
        chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
        print 'Executing from ', path.abspath(curdir), mz_imageid
    except:
        pass
    resp = delete_document_data_content(mz_imageid=mz_imageid)
    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    ret = mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == mz_imageid ))).execute()
    print 'Deleted bf_imageid', ret #ret.fetchone()
    return ret

# Delete doc content and db entry using bfly colorstyle to query db
def delete_by_bflyid(bf_imageid=None):
    from os import chdir, path, curdir
    try:
        chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
        print 'Executing from ', path.abspath(curdir), bf_imageid
    except:
        pass

    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    ret_select = mozu_image_table.select(whereclause=( (mozu_image_table.c.bf_imageid == bf_imageid ))).execute()
    mz_imageid = ret_select.fetchone()['mz_imageid']
    resp = delete_document_data_content(mz_imageid=mz_imageid)

    ret = mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == mz_imageid ))).execute()
    print 'Deleted bf_imageid', ret #ret.fetchone()
    return ret


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


if __name__ == '__main__':
    print "Cannot be called from shell.\v Import using python..."

