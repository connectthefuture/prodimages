#!/usr/bin/env python
# coding: utf-8
#import pdb;pdb.set_trace()

 ## Listing and Info about Document List
#######################################
import sqlalchemy
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
    #import pdb
    #pdb.set_trace()
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

                            # print 'NO BFID to update ', locals()

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


# # PUT - Upload/Update Image/DocumentContent
def update_content_mz_image(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    mzclient = MozuRestClient()
    content_response = mzclient.send_content(**kwargs)
    print content_response.headers, "\nUpdate Mozu Content"
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    update_db = mozu_image_table.update(values=dict(**table_args))
    print content_response.headers, "\nUpdate DB MZ_IMAGE"
    return content_response

####
# Post - New Image, Creates Document Resource or 409 error
@log
def upload_new(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance

    mzclient = MozuRestClient(**kwargs)
    mz_imageid, document_resource = mzclient.create_new_mz_image()
    if document_resource == "Keyerror":
        print mz_imageid
    elif document_resource == "documentTree":
        bf_imageid = mzclient.bf_imageid
    elif document_resource == "documentListDocumentContent":
        kwargs['mz_imageid'] = mz_imageid
    kwargs['bf_imageid'] = bf_imageid
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    insert_db = mozu_image_table.insert(values=dict(**table_args))
    print "Inserting with, ", insert_db
    if kwargs['bf_imageid']:
        content_response = update_content_mz_image(**kwargs)
        try:
            insert_db.execute()
            print 'Inserted --> ', kwargs.items(), ' <-- ', insert_db
        except sqlalchemy.exc.IntegrityError:
            print 'PASSING IntegrityERR with args--> ', kwargs     # # Insert to mz_imageid + **kwargs to Oracle
    return content_response


#######################################
### Main - Conditions ##
#######################################
########
@log
def main(fileslist):
    import sqlalchemy
    from db import mozu_image_table_instance
    from mozu_image_util_functions import compile_todict_for_class_instance_variables, magick_convert_to_jpeg, netsrv101_path_maker
    # Compiles Data Payload and other Vars per Doc -- Including src_filepath -- **values keys set per instance
    # print type(fileslist), '<--Type\tLenLoFilepaths', len(fileslist), '\t', fileslist
    ### Date Defs
    from os import path # chdir , curdir
    import datetime #, glob, shutil

    todaysdatefullsecs = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    todaysdatefull = todaysdatefullsecs[:12]
    todaysdate = todaysdatefull[:8]  # '{:%Y,%m,%d}'.format(datetime.datetime.now())

    # Define for Creating Archive dirs
    archive = '/mnt/Post_Complete/Complete_Archive/Uploaded'
    # archive_uploaded = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""), "uploaded_" + str(todaysdatefullsecs).replace(",", ""))
    archive_uploaded_day = path.join(archive, "dateloaded_" + str(todaysdate).replace(",", ""))
    imgdest_jpg_mozu = path.join(archive_uploaded_day, 'JPG_MOZU_LOAD')
    # imgdest_jpg_mozu_loaded = path.join(imgdest_jpg_mozu, 'LOADED')
    if path.dirname(fileslist[0]).split('/')[-1] == 'JPG_MOZU_LOAD':
        #         fileslistX= [magick_convert_to_jpeg(f) for f in fileslist if f.split('.')[-1] == 'png']
        fileslist = [magick_convert_to_jpeg(f, destdir=imgdest_jpg_mozu) for f in fileslist if f]
    else:
        fileslist = fileslist # [ path.abspath(f) for f in fileslist if f ]
    if not path.isfile(fileslist[0]):
        fileslist = netsrv101_path_maker(fileslist)
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
                create_resource_resp = upload_new(**values)
                mozu_image_table = mozu_image_table_instance()
                if int(create_resource_resp.keys()[0]) < 400:
                    table_args = include_keys(values, __mozu_image_table_valid_keys__)
                    insert_db = mozu_image_table.insert(values=dict(**table_args))
                    insert_db.execute()
                    print 'Inserted --> ', values.items(), ' <-- ', insert_db
                elif int(create_resource_resp.keys()[0]) == 409:
                    table_args = include_keys(values, __mozu_image_table_valid_keys__)
                    mz_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == table_args['bf_imageid']) ) ).execute().fetchone()['mz_imageid']
                    bf_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.mz_imageid == table_args['mz_imageid']) ) ).execute().fetchone()['bf_imageid']
                    table_args['bf_imageid'] = values['bf_imageid'] = bf_imageid
                    table_args['mz_imageid'] = values['mz_imageid'] = mz_imageid
                    resp = update_content_mz_image(**values)
                    print('RESP 207 mzexec: {}'.format(resp))
                    #upsert_content_resp = upsert_data_mz_image(**values)  # ,dict(**values))
                    if resp.http_status_code < 400:
                        update_db = mozu_image_table.update(values=dict(**table_args),whereclause=mozu_image_table.c.bf_imageid == table_args['bf_imageid'])
                        res = update_db.execute()
                        print res, 'Updated--> ', values.items(), ' <-- ', update_db
                else:
                    print "HTTP Status: {}\n Raising Integrity Error".format(create_resource_resp.http_status_code)
                    raise sqlalchemy.exc.IntegrityError()
            except ValueError: #sqlalchemy.exc.IntegrityError:
                print 'Type or VALUE Error and everything is or will be commented out below because it is in the db already'
                #return 'IntegrityError'
            except KeyError:  # sqlalchemy.exc.IntegrityError:
                print 'TYPE or Value Error and everything is or will be commented out below because it is in the db already'
                #return 'IntegrityError'
                #pass
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
            for arg in sys.argv[1:]:
                insert_list.append(arg)  # '/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
        insert_list_filepaths = list(set(sorted(insert_list)))
        print "filelist_length", len(insert_list_filepaths), insert_list_filepaths
        main(fileslist=insert_list_filepaths)
    except IndexError:
        print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args"
