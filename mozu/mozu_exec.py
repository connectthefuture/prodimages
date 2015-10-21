#!/usr/bin/env python
# coding: utf-8
#import pdb;pdb.set_trace()

#######################################
## Listing and Info about Document List
#######################################
import sqlalchemy
from db import mozu_image_table_instance
from mozu_image_util_functions import include_keys, log
from RESTClient import __mozu_image_table_valid_keys__

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

@log
def list_documents(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    documents = mzclient.get_mz_image_document_list()['items']
    return documents

@log
def resource_documents_list(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    documents_list = mzclient.get_mz_image_document_list()
    return documents_list

#######################################
##### Single File / Single Document Obj
#######################################
# Post - New Image, Creates Document
@log
def upload_new(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    mzclient = MozuRestClient(**kwargs)
    mz_imageid, document_resource = mzclient.create_new_mz_image()
    kwargs['mz_imageid'] = mz_imageid
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    mzclient.send_content(**kwargs)
    insert_db = mozu_image_table.insert(values=dict(**table_args))
    print "Inserting with, ", insert_db
    insert_db.execute()
    print 'Inserted --> ', kwargs.items(), ' <-- ', insert_db
    ## Insert to mz_imageid + **kwargs to Oracle
    return mz_imageid, document_resource
# @log
# # PUT - Upload/Update Image/DocumentContent
# def upsert_data_mz_image(**kwargs):
#     from RESTClient import MozuRestClient
#     if not args:
#         mzclient = MozuRestClient(**kwargs)
#     update_resp = mzclient.send_content(**kwargs)
#     print update_resp.headers, "UpsertContent"
#     return update_resp

# PUT - Update Document Data and Content- Properties/Metadata
@log
def upsert_data_mz_image(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    mozu_image_table = mozu_image_table_instance()
    select_db = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == kwargs.get('bf_imageid')) ) )
    select_result = select_db.execute()
    test = [ row for row in select_result ]
    print select_db, '\n\nTEST -->\n', test
    if test:
        kwargs['mz_imageid'] = select_result.fetchone()['mz_imageid']
        md5checksum = []
        kwargs['md5checksum'] = md5checksum
        mzclient = MozuRestClient(**kwargs)
        update_resp = mzclient.update_mz_image(**kwargs)
        table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
        update_db = mozu_image_table.update(values=dict(**table_args),whereclause=mozu_image_table.c.bf_imageid==kwargs.get('bf_imageid'))
        print "1\nUpdate Statement: \v", update_db
        res = update_db.execute()
        print res, '2-Updated--> ', kwargs.items(), ' <--kwargs.items ', update_db
        return update_resp
    else:
        mzclient = MozuRestClient(**kwargs)
        mz_imageid, document_resource = mzclient.create_new_mz_image()
        # kwargs['mz_imageid'], kwargs['mozu_url'] =  mzclient.create_new_mz_image() #mzclient.create_new_mz_image(**kwargs)
        if mz_imageid: #type(post_resp) == dict:
            kwargs['mz_imageid'] = mz_imageid # mz_imageid.keys()[0]
            table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
            try:
                content_response = mzclient.send_content(**kwargs)
                insert_db = mozu_image_table.insert(**table_args)
                print "3-\nInsert Statement: \v", insert_db
                insert_result = insert_db.execute()
                print content_response, "Not in DB. Insert Result: ", insert_result.is_insert
                return insert_result.is_insert
            except sqlalchemy.exc.IntegrityError:
                content_response = mzclient.send_content(**kwargs)
                if kwargs.get('bf_imageid'):
                    kwargs.get('bf_imageid')
                    update_db = mozu_image_table.update(values=dict(**table_args),
                                                        whereclause=  #mozu_image_table.c.bf_imageid==kwargs.get('bf_imageid')
                                                        (mozu_image_table.c.bf_imageid == v['bf_imageid'])
                                                        |
                                                        (mozu_image_table.c.mz_imageid == v['mz_imageid'])
                                                        )

                    print "4-\nUpdate Statement: \v", update_db
                    update_result = update_db.execute()
                    print content_response, '4.5-Updated--> ', kwargs.items(), ' <--kwargs.items ', update_db
                    return update_result
                else:

                    #print 'NO BFID to update ', locals()

                    insert_db = mozu_image_table.insert(**table_args)
                    print "5-\nInsert Statement: \v", insert_db
        else:
            print mz_imageid, ' Failed'

# DELETE - Delete Image/DocumentContent - Everything
@log
def delete_document_data_content(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    delete_resp = mzclient.delete_mz_image()
    mozu_image_table = mozu_image_table_instance()

    delete_db = mozu_image_table.delete( whereclause=( (mozu_image_table.c.mz_imageid == kwargs.get('mz_imageid')) ) )
    #res = delete_db.execute()
    # TODO: Need to delete from db or alter insome way
    print delete_resp.headers, "Delete", "MZ CLIENTID in FUNCtion: ", kwargs
    return delete_resp


### GET Images - Content
#
# def download_document_content(outfile=None, **kwargs):
#     from RESTClient import MozuRestClient
#     print kwargs, 'KWARGS-26'
#     _mzclient = MozuRestClient(**kwargs)
#     from os import path as path
#     image_content = _mzclient[     if not _mzclient.bf_imageid:
#         # Get bflyid from Oracle using mz_id
#         from db import mozu_image_table_instance
          #mozu_image_table = mozu_image_table_instance()
#         bf_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.mz_imageid == _mzclient.mz_imageid) ) )[0]['bf_imageid']
#         _mzclient.bf_imageid = bf_imageid
#     if not outfile:
#         outfile = path.join('/tmp', _mzclient.bf_imageid)
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
#     _mzclient = MozuRestClient(**kwargs)
#     image_data = _mzclient_h[ders()
#     print image_data
#     return image_data

#######################################
### Main - Conditions ##
#######################################
########
@log
def main(list_of_filepaths):
    import sqlalchemy, sys
    from db import mozu_image_table_instance
    from mozu_image_util_functions import compile_todict_for_class_instance_variables
    # Compiles Data Payload and other Vars per Doc -- Including src_filepath -- **v keys set per instance
    # print type(list_of_filepaths), '<--Type\tLenLoFilepaths', len(list_of_filepaths), '\t', list_of_filepaths
    compiled_instance_vars = compile_todict_for_class_instance_variables(list(list_of_filepaths))
    # print type(compiled_instance_vars), '<--Type\tLenCompiledInsVars', len(compiled_instance_vars), '\tKeys: ', compiled_instance_vars.keys()
    for key,value in compiled_instance_vars.iteritems():
        v = include_keys(value, __mozu_image_table_valid_keys__)
        # print "IncludedKeys: {}\n\tkey:\t{}\n\tvalue:\t{}".format(v.items(), key , value.popitem())
        if not v.get('mz_imageid'):
            #### --> src_filepath = k # will need src_filepath in order to perfom any image manipulation
            ### ---> before loading(would actually need to redo the md5checksum from compiler)
            # Insert -- Then try Update if Insert to DB fails or Create NewDoc Fails to Mozu
            try:
                v['mz_imageid'], response = upload_new(**v)
                load_content_resp = upload_new(**v)
                mozu_image_table = mozu_image_table_instance()
                if int(load_content_resp.keys()[0]) < 400:
                    table_args = include_keys(v, __mozu_image_table_valid_keys__)
                    insert_db = mozu_image_table.insert(values=dict(**table_args))
                    insert_db.execute()
                    print 'Inserted --> ', v.items(), ' <-- ', insert_db
                elif int(load_content_resp.keys()[0]) == 409:
                    table_args = include_keys(v, __mozu_image_table_valid_keys__)
                    select_db = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == table_args['bf_imageid']) ) )
                    table_args['mz_imageid'] = v['mz_imageid'] = select_db['mz_imageid']

                    upsert_content_resp = upsert_data_mz_image(**v) #,dict(**v))
                    if upsert_content_resp.http_status_code < 300:
                        update_db = mozu_image_table.update(values=dict(**table_args),whereclause=mozu_image_table.c.bf_imageid==table_args['bf_imageid'])
                        res = update_db.execute()
                        print res, 'Updated--> ', v.items(), ' <-- ', update_db
                else:
                    print "HTTP Status: {}\n Raising Integrity Error".format(load_content_resp.http_status_code)
                    raise sqlalchemy.exc.IntegrityError()
            except sqlalchemy.exc.IntegrityError:
                try:
                    upsert_content_resp = upsert_data_mz_image(**v) #,dict(**v))
                    if upsert_content_resp.http_status_code < 300:
                        table_args = include_keys(v, __mozu_image_table_valid_keys__)
                        update_db = mozu_image_table.update(values=dict(**table_args),whereclause=mozu_image_table.c.bf_imageid==table_args['bf_imageid'])
                        res = update_db.execute()
                        print res, 'Updated--> ', table_args.items(), ' <-- ', update_db

                    print 'IntegrityError and everything is or will be commented out below because it is in the db already', v
                except:
                    print "ENDING ERROR...", v

        elif v.get('mz_imageid'):
            print "KWARGS has MZID: {}".format(v.get('mz_imageid'))


## Run in shell as mozu_exec.py *args
if __name__ == '__main__':
    import sys
    import os.path as path
    insert_list = []
    try:
        if path.isfile(path.abspath(sys.argv[1])):
            for arg in sys.argv[0].split():
                insert_list.append(arg)##'/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
        insert_list_filepaths = list(set(sorted(insert_list)))
        print "filelist_length", len(insert_list_filepaths), insert_list_filepaths
        print locals(), arg #main(insert_list_filepaths)
    except IndexError:
        print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args"
