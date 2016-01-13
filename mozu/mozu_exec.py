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
# Post - New Image, Creates Document
@log
def upload_new_data_content(**kwargs):
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance

    mzclient = MozuRestClient(**kwargs)
    mz_imageid, document_resource = mzclient.create_new_mz_image()
    if mz_imageid == "Keyerror":
        print mz_imageid
    else:
        pass
    kwargs['mz_imageid'] = mz_imageid
    mozu_image_table = mozu_image_table_instance()
    table_args = include_keys(kwargs, __mozu_image_table_valid_keys__)
    content_response = mzclient.send_content(**kwargs)
    insert_db = mozu_image_table.insert(values=dict(**table_args))
    print "Inserting with, ", insert_db
    if len(mz_imageid) > 20:
        try:
            insert_db.execute()
            print 'Inserted --> ', kwargs.items(), ' <-- ', insert_db
        except sqlalchemy.exc.IntegrityError:
            print 'PASSING IntegrityERR with args--> ', kwargs     # # Insert to mz_imageid + **kwargs to Oracle
    return content_response

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
                        print '116 mozuexec error-- SQLAlchemy Integrity Error'
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
        res = upload_new_data_content(**kwargs)
        return res
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
def main(fileslist):
    import sqlalchemy
    from db import mozu_image_table_instance
    from mozu_image_util_functions import compile_todict_for_class_instance_variables, magick_convert_to_jpeg
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
        fileslist_jpegs = [magick_convert_to_jpeg(f, destdir=imgdest_jpg_mozu) for f in fileslist if f]
    else:
        fileslist_jpegs = fileslist # [ path.abspath(f) for f in fileslist if f ]

    compiled_instance_vars = compile_todict_for_class_instance_variables(fileslist=fileslist_jpegs)
    # print type(compiled_instance_vars), '<--Type\tLenCompiledInsVars', len(compiled_instance_vars), '\tKeys: ', compiled_instance_vars.keys()
    for key,values in compiled_instance_vars.iteritems():
        # v = include_keys(values, __mozu_image_table_valid_keys__)
        # print "IncludedKeys: {}\n\tkey:\t{}\n\tvalues:\t{}".format(v.items(), key , values.popitem())
        if not values.get('mz_imageid'):
            # ### --> src_filepath = k # will need src_filepath in order to perfom any image manipulation
            # ## ---> before loading(would actually need to redo the md5checksum from compiler)
            # Insert -- Then try Update if Insert to DB fails or Create NewDoc Fails to Mozu
            try:
                content_resp = upload_new_data_content(**values)
                if int(content_resp.keys()[0]) < 400:
                    table_args = include_keys(values, __mozu_image_table_valid_keys__)
                    insert_db = mozu_image_table.insert(values=dict(**table_args))
                    insert_db.execute()
                    print 'Inserted --> ', values.items(), ' <-- ', insert_db
                elif int(content_resp.keys()[0]) == 409:
                    raise TypeError
                else:
                    print "HTTP Status: {}\n Raising Integrity Error".format(content_resp.status_code)
                    raise ValueError #sqlalchemy.exc.IntegrityError()
            except TypeError:
                print 'TYPE Error -- 409 DOCUMENT EXISTS continuing with update-->select query'
                mozu_image_table = mozu_image_table_instance()
                table_args = include_keys(values, __mozu_image_table_valid_keys__)
                mz_imageid = mozu_image_table.select(whereclause=((mozu_image_table.c.bf_imageid == table_args['bf_imageid']))).execute().fetchone()['mz_imageid']
                #md5checksum = mozu_image_table.select(whereclause=((mozu_image_table.c.bf_imageid == table_args['md5checksum']))).execute().fetchone()['mz_imageid']
                # bf_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == table_args['mz_imageid']) ) ).execute().fetchone()['bf_imageid']
                table_args['mz_imageid'] = values['mz_imageid'] = mz_imageid
                update_content_resp = update_content_mz_image(**values)
                print "Updated Process Complete, ", update_content_resp.headers
                if update_content_resp.status_code < 300:
                    update_db = mozu_image_table.update(values=dict(**table_args),whereclause=mozu_image_table.c.bf_imageid == table_args['bf_imageid'])
                    res = update_db.execute()
                    print res, 'Updated--> ', values.items(), ' <-- ', update_db
            except ValueError: #sqlalchemy.exc.IntegrityError:
                print 'VALUE Error and everything is or will be commented out below because it is in the db already'
                #return 'IntegrityError'
            except KeyError:  # sqlalchemy.exc.IntegrityError:
                print 'KEY Error and everything is or will be commented out below because it is in the db already'
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
    ## Run in shell as mozu_exec.py *args
if __name__ == '__main__':
    import sys
    from os import environ, path


    environ['PRD_ENV'] = '1'
    insert_list = []
    print sys.argv[1]
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
        try:
            if path.isfile(path.abspath(sys.argv[1])):
                for arg in sys.argv[1:]:
                    insert_list.append(
                        arg)  # '/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
            insert_list_filepaths = list(set(sorted(insert_list)))
            print "filelist_length", len(insert_list_filepaths), insert_list_filepaths
            main(fileslist=insert_list_filepaths)
        except IndexError:
            print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args"

    try:
        if path.isfile(path.abspath(sys.argv[1])):
            for arg in sys.argv[1:]:
                insert_list.append(arg)  # '/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
        insert_list_filepaths = list(set(sorted(insert_list)))
        print "filelist_length", len(insert_list_filepaths), insert_list_filepaths
        main(fileslist=insert_list_filepaths)
    except IndexError:
        print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args"
