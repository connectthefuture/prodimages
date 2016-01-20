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
    ret_select = mozu_image_table.select(whereclause=((mozu_image_table.c.mz_imageid == mz_imageid))).execute().fetchone()
    ret = mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == mz_imageid ))).execute()
    print 'Deleted bf_imageid', ret #ret.fetchone()
    return ret_select['bf_imageid']

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
    try:
        mz_imageid = ret_select.fetchone()['mz_imageid']
        if mz_imageid:
            resp = delete_document_data_content(mz_imageid=mz_imageid)

            ret = mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == mz_imageid ))).execute()
            print 'Deleted bf_imageid', ret #ret.fetchone()
            return bf_imageid
    except TypeError:
        'NoneTpe Error in delete by bfid. {} Not in DB'.format(bf_imageid)
#### Update or UpdateDel -- aka "delete from mozu and db then reload to mozu and store new mozu docID"

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

## Delete current Mozu image and load newest version from netsrv101
def update_replace_content(**kwargs):
    if kwargs.get("mz_imageid"):
        mz_imageid = kwargs.get("mz_imageid")
        bf_imageid = kwargs.get("bf_imageid")
        res_del = delete_by_mozuid(mz_imageid=mz_imageid)
        print 'Update Option 1'
    elif kwargs.get("src_filepath"):
        src_filepath = kwargs.get("src_filepath")
        bf_imageid = src_filepath.split('/')[-1].split('.')[0]
        ext = src_filepath.split('.')[-1]
        res_del = delete_by_bflyid(bf_imageid=bf_imageid)
        print 'Update Option 2'
    elif kwargs.get("bf_imageid"):
        from os import path
        bf_imageid = kwargs.get("bf_imageid")
        ext = kwargs.get("ext", "png")
        src_filepath = path.join('/mnt/images', bf_imageid[:4], bf_imageid + '.' + ext)
        kwargs['src_filepath'] = src_filepath
        res_del = delete_by_bflyid(bf_imageid=bf_imageid)
        print 'Update Option 3'
    else:
        print 'Update Option KeyError'
        raise KeyError
    kwargs["bf_imageid"] = bf_imageid
    if bf_imageid:
        resp = update_content_mz_image(**kwargs)
    print 'Successful replace-update \n', locals()
    return resp


if __name__ == '__main__':
    try:
        from sys import argv
        from os import path
        arg1 = argv[1]
        if len(arg1) == 9:
            bf_imageid = arg1
        elif path.isfile(arg1):
            src_filepath = arg1
        elif len(arg1) > 15:
            mz_imageid = arg1
        result = update_replace_content(dict(locals()))
        print result
    except:
        print "Error or Cannot be called from shell.\v Import using python...", locals()
