#!/usr/bin/env python
# coding: utf-8
import pdb;pdb.set_trace()

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
    select_result = mozu_image_table.select( whereclause=(mozu_image_table.c.bf_imageid == kwargs.get('bf_imageid')) ).execute().fetchone()
    # test = [ row for row in select_result ]
    print select_result, '\n\nTEST -->\n', kwargs  # , test
    if select_result:
        try:
            if select_result['mz_imageid']:
                kwargs['mz_imageid'] = select_result['mz_imageid']
                md5checksum = []
                kwargs['md5checksum'] = md5checksum
                mzclient = MozuRestClient(**kwargs)
                update_resp = mzclient.update_mz_image(**kwargs)
                table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
                update_db = mozu_image_table.update(values=dict(**table_args), whereclause=mozu_image_table.c.bf_imageid==kwargs.get('bf_imageid'))
                print "1\nUpdate Statement: \t", update_db
                update_result = update_db.execute()
                print update_result, '2-Updated--> ', kwargs.items(), ' <--kwargs.items ', update_db
                return update_resp
            else:
                mzclient = MozuRestClient(**kwargs)
                # mz_imageid, document_resource = mzclient.create_new_mz_image()
                mz_imageid = mzclient.get_mz_image_document_list(name=kwargs.get('bf_imageid'))['id']
                # kwargs['mz_imageid'], kwargs['mozu_url'] =  mzclient.create_new_mz_image() #mzclient.create_new_mz_image(**kwargs)
                if mz_imageid: #type(post_resp) == dict:
                    kwargs['mz_imageid'] = mz_imageid # mz_imageid.keys()[0]
                    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
                    try:
                        content_response = mzclient.send_content(**kwargs)
                        insert_db = mozu_image_table.insert(**table_args)
                        print "3-\nInsert Statement: \t", insert_db
                        insert_result = insert_db.execute()
                        print content_response, "Not in DB. Insert Result: ", insert_result.fetchone()['mz_imageid']
                        return insert_result.fetchone()
                    except sqlalchemy.exc.IntegrityError:
                        content_response = mzclient.send_content(**kwargs)
                        if kwargs.get('bf_imageid'):
                            kwargs.get('bf_imageid')
                            update_db = mozu_image_table.update(values=dict(**table_args),
                                                                whereclause=  # mozu_image_table.c.bf_imageid==kwargs.get('bf_imageid')
                                                                (mozu_image_table.c.bf_imageid == table_args['bf_imageid'])
                                                                |
                                                                (mozu_image_table.c.mz_imageid == table_args['mz_imageid'])
                                                                )

                            print "4-\nUpdate Statement: \t", update_db
                            update_result = update_db.execute()
                            print content_response, '4.5-Updated--> Maybe', kwargs.items(), ' <--kwargs.items ', update_db
                            return update_result.fetchone()
                        else:

                            #print 'NO BFID to update ', locals()

                            insert_db = mozu_image_table.insert(**table_args)
                            print "5-\nFailed Insert Statement: \t", insert_db
                else:
                    print mz_imageid, ' Failed'
        except TypeError:
            print ' 128 Type-aka-OldAttribError in Upsert_mz_exec Locals -->', locals()
            #pass

    else:
        res = upload_new(**kwargs)
        return res
# DELETE - Delete Image/DocumentContent - Everything
@log
def delete_document_data_content(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    delete_resp = mzclient.delete_mz_image()
    mozu_image_table = mozu_image_table_instance()

    delete_db = mozu_image_table.delete( whereclause=(mozu_image_table.c.mz_imageid == kwargs.get('mz_imageid')) )
    # res = delete_db.execute()
    # TODO: Need to delete from db or alter insome way
    print delete_resp.headers, "Delete \n", delete_db, "\nMZ CLIENTID in FUNCtion: ", kwargs
    return delete_resp


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

#######################################
### Main - Conditions ##
#######################################
########
@log
def main(fileslist=None):
    import sqlalchemy
    from db import mozu_image_table_instance
    from mozu_image_util_functions import compile_todict_for_class_instance_variables
    # Compiles Data Payload and other Vars per Doc -- Including src_filepath -- **values keys set per instance
    # print type(fileslist), '<--Type\tLenLoFilepaths', len(fileslist), '\t', fileslist
    compiled_instance_vars = compile_todict_for_class_instance_variables(fileslist=fileslist)
    # print type(compiled_instance_vars), '<--Type\tLenCompiledInsVars', len(compiled_instance_vars), '\tKeys: ', compiled_instance_vars.keys()
    # print compiled_instance_vars, "186-MZEXECY"
    for key,values in compiled_instance_vars.iteritems():
        # v = include_keys(values, __mozu_image_table_valid_keys__)
        # print "IncludedKeys: {}\n\tkey:\t{}\n\tvalues:\t{}".format(v.items(), key , values.popitem())
        if not values.get('mz_imageid'):
            # ### --> src_filepath = k # will need src_filepath in order to perfom any image manipulation
            # ## ---> before loading(would actually need to redo the md5checksum from compiler)
            # Insert -- Then try Update if Insert to DB fails or Create NewDoc Fails to Mozu
            try:
                values['mz_imageid'], response = upload_new(**values)
                load_content_resp = upload_new(**values)
                mozu_image_table = mozu_image_table_instance()
                if int(load_content_resp.keys()[0]) < 400:
                    table_args = include_keys(values, __mozu_image_table_valid_keys__)
                    insert_db = mozu_image_table.insert(values=dict(**table_args))
                    insert_db.execute()
                    print 'Inserted --> ', values.items(), ' <-- ', insert_db
                elif int(load_content_resp.keys()[0]) == 409:
                    table_args = include_keys(values, __mozu_image_table_valid_keys__)
                    mz_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == table_args['bf_imageid']) ) ).execute().fetchone()['mz_imageid']
                    #bf_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == table_args['bf_imageid']) ) ).execute().fetchone()['bf_imageid']

                    table_args['mz_imageid'] = values['mz_imageid'] = mz_imageid
                    upsert_content_resp = upsert_data_mz_image(**values)  # ,dict(**values))
                    if upsert_content_resp.http_status_code < 300:
                        update_db = mozu_image_table.update(values=dict(**table_args),whereclause=mozu_image_table.c.bf_imageid==table_args['bf_imageid'])
                        res = update_db.execute()
                        print res, 'Updated--> ', values.items(), ' <-- ', update_db
                else:
                    print "HTTP Status: {}\n Raising Integrity Error".format(load_content_resp.http_status_code)
                    raise sqlalchemy.exc.IntegrityError()
            except OSError: #sqlalchemy.exc.IntegrityError:
                # try:
                #     upsert_content_resp = upsert_data_mz_image(**values) #,dict(**values))
                #     if upsert_content_resp.http_status_code < 300:
                #         table_args = include_keys(values, __mozu_image_table_valid_keys__)
                #         update_db = mozu_image_table.update(values=dict(**table_args),whereclause=mozu_image_table.c.bf_imageid==table_args['bf_imageid'])
                #         res = update_db.execute()
                #         print res, 'Updated--> ', table_args.items(), ' <-- ', update_db
                #
                print 'IntegrityError and everything is or will be commented out below because it is in the db already'
                #return 'IntegrityError'
                pass

                # except IOError:
                #     print "ENDING ERROR...", values

        elif values.get('mz_imageid'):
            print "KWARGS has MZID: {}".format(values.get('mz_imageid'))


## Run in shell as mozu_exec.py *args
if __name__ == '__main__':
    import sys
    import os.path as path
    insert_list = []
    try:
        if path.isfile(path.abspath(sys.argv[1])):
            for arg in " ".join(sys.argv[1:]):
                insert_list.append(arg)  # '/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
        insert_list_filepaths = list(set(sorted(insert_list)))
        print "filelist_length", len(insert_list_filepaths), insert_list_filepaths
        main(fileslist=insert_list_filepaths)
    except IndexError:
        print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args"
