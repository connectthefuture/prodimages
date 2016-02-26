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
    if kwargs.get('mz_imageid'):
        delete_db = mozu_image_table.delete( whereclause=(mozu_image_table.c.mz_imageid == kwargs.get('mz_imageid')) )
    else:
        delete_db = mozu_image_table.delete( whereclause=(mozu_image_table.c.bf_imageid == kwargs.get('bf_imageid')) )
    # res = delete_db.execute()
    print delete_resp.headers, "Delete \n", delete_db, "\nMZ CLIENTID in FUNCtion: ", kwargs
    return delete_resp

# Delete doc content and db entry using mzid to query db
def delete_by_mozuid(**kwargs):
    from os import chdir, path, curdir
    try:
        chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
        print 'Executing from ', path.abspath(curdir), kwargs.get('mz_imageid', '')
    except:
        pass
    resp = delete_document_data_content(mz_imageid=kwargs.get('mz_imageid', ''))
    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    ret_select = mozu_image_table.select(whereclause=((mozu_image_table.c.mz_imageid == kwargs.get('mz_imageid', '')))).execute().fetchone()
    ret = mozu_image_table.delete(whereclause=( (mozu_image_table.c.mz_imageid == kwargs.get('mz_imageid', '') ))).execute()
    print 'Deleted bf_imageid', ret #ret.fetchone()
    return ret_select['bf_imageid']

# Delete doc content and db entry using bfly colorstyle to query db
def delete_by_bflyid(**kwargs):
    from os import chdir, path, curdir
    try:
        chdir(path.join('/usr/local/batchRunScripts', 'mozu'))
        print 'Executing from ', path.abspath(curdir), kwargs.get('bf_imageid', '')
    except:
        pass
    try:
        resp = delete_document_data_content(**kwargs)
        from db import mozu_image_table_instance
        mozu_image_table = mozu_image_table_instance()
        try:
            ret = mozu_image_table.delete(whereclause=((mozu_image_table.c.mz_imageid == kwargs.get('bf_imageid', '')))).execute()
        except:
            print('Skipping Delete DB data when using delete by BFID')
        return kwargs.get('bf_imageid', '')
    except TypeError:
        'NoneTpe Error in delete by bfid. {} Not in DB'.format(kwargs.get('bf_imageid', ''))
#### Update or UpdateDel -- aka "delete from mozu and db then reload to mozu and store new mozu docID"
def del_or_replace_by_bf_style_list(**kwargs):
    from os import chdir, path
    MOZU_CODE_DIR = '/usr/local/batchRunScripts/mozu'
    JBMODULES_ROOT = '/usr/local/batchRunScript/python/jbmodules'
    chdir(MOZU_CODE_DIR)
    import mozu_exec_del_update
    #mozu_exec.main(insert_list)

    netsrv101_mnt = '/mnt/images'
    ext = '.png'
    files_list = []
    missing_mzid = []

    if not kwargs.get('styles_list'):
        styles_list = ['351480205_alt01']##379612301 381880001 381879601 381878901 381856401 381856303 381856201 381720702 381689201 381640905 380874901 380874701 380874601 380471502 380306001 380305201 380304801 380303401 379801701 379612301 379597701 379597601 379597301 379597101 379578201 379534101 379448301 379366301 378548201 378536702 378536701 378536605 378536604 378536603 378536602 378536502 378536501 378536404 378536403 378536402 378536401 378536304 378536303 378536302 378536301 378534401 378444401 378444301 377849901 377849603 377849305 377809901 364184801 359178201 359164301 358207301 356190201 356088501 356088401 355434801 347278201 346088501 323643602']  # ['345496501'] #, '379438901','373101102']
    for f in styles_list[0].split():
        #client = MozuRestClient()
        src = path.join(netsrv101_mnt, f[:4], f + ext).replace('\n', '')
        if path.isfile(src):
            files_list.append(src)
            #mozu_exec_del_update.delete_by_bflyid(bf_imageid=f)
            resp = mozu_exec_del_update.update_content_mz_image(bf_imageid=f, src_filepath=src)
            print '\n\n\n\n\n\n\n\\t\tEND LOOP FILES LIST APPEND\n\n\n\n{0}\n\n\n'.format(resp)

#     if 1==1: ##kwargs.get('REPLACE'):
#         import mozu_exec
#         mozu_exec.main(files_list)
#         print files_list, f
#         #res = mozu_exec_del_update.update_replace_content(bf_imageid=f)
#     else:
    return files_list

#### basic db insert
def insert_data_db(**kwargs):
    from db import mozu_image_table_instance
    from RESTClient import __mozu_image_table_valid_keys__
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    insert_db = mozu_image_table.insert(values=dict(**table_args))
    #update_db = mozu_image_table.update(values=dict(**table_args), whereclause=mozu_image_table.c.bf_imageid == table_args['bf_imageid'])
    insert_db.execute()

# @log
# # PUT - Upload/Update Image/DocumentContent
def update_content_mz_image(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    mzclient = MozuRestClient(**kwargs)
    content_response = mzclient.send_content(**kwargs)
    print content_response.headers, "\nUpdate Mozu Content"
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    update_db = mozu_image_table.update(values=dict(**table_args))
    print content_response.headers, "\nUpdate DB MZ_IMAGE"
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
    print 'Successful replace-update \nLocals: \t', locals()
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
        result = update_replace_content(**locals())
        print result
    except:
        print "Error or Cannot be called from shell.\v Import using python...", locals()
