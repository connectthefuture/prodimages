#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'johnb'

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
#     from mozu_exec import delete_document_data_content
#     mozu_image_table = mozu_image_table_instance()
#     documents = client.get_mz_image_document_list()  ##[0]['items']
#
#     for x in documents['items']:
#         # Delete Mozu First then db
#         resp = mozu_exec.delete_document_data_content(mz_imageid=x['id']) #, page_size="200") # ['id']# = documents.get('items')[0]
#         mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == x['id']) )).execute()
#         import json
#         return json.dumps(x.items())


def delete_by_mozuid(mz_imageid=None):
    from os import chdir, path, curdir
    try:
        chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
        print 'Executing from ', path.abspath(curdir), mz_imageid
    except:
        pass
    from mozu_exec import delete_document_data_content
    resp = mozu_exec.delete_document_data_content(mz_imageid=mz_imageid)
    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    ret = mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == mz_imageid ))).execute()
    print 'Deleted bf_imageid', ret #ret.fetchone()
    return ret


def delete_by_bflyid(bf_imageid=None):
    from os import chdir, path, curdir
    try:
        chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
        print 'Executing from ', path.abspath(curdir), bf_imageid
    except:
        pass

    from mozu_exec import delete_document_data_content
    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    ret_select = mozu_image_table.select(whereclause=( (mozu_image_table.c.bf_imageid == bf_imageid ))).execute()
    mz_imageid = ret_select.fetchone()['mz_imageid']
    resp = mozu_exec.delete_document_data_content(mz_imageid=mz_imageid)

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

