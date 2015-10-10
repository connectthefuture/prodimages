#!/usr/bin/env python
# coding: utf-8

from RESTClient import MozuRestClient
def count_total__files_documents(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    total_count = mzclient.get_mz_image()['totalCount']
    print "Total Files in DocumentList: {}".format(total_count)
    return total_count


def list_files_documents(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    image_data = mzclient.get_mz_image()['items']
    #print image_data
    return image_data


def download_document_content(MozuRestClient,mz_imageid,outfile=None):
    from os import path as path
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    image_content = mzclient().get_mz_image()
    if not mzclient.bf_imageid:
        # Get bflyid from Oracle using mz_id
        from db import mozu_image_table_instance
        bf_imageid = mozu_image_table_instance.select( whereclause=( (mozu_image_table_instance.c.mz_imageid == mzclient.mz_imageid) ) )[0]['bf_imageid']
        mzclient.bf_imageid = bf_imageid
    if not outfile:
        outfile = path.join('/tmp', mzclient.bf_imageid)
    else: pass
    with open(outfile,'w') as f:
        f.write(image_content)
    return path.abspath(outfile)

def read_document_content_headers(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    image_data = mzclient().get_mz_image_headers()
    print image_data
    return image_data

# PUT - Upload NEW Image/DocumentContent
def update_tags_mz_image(MozuRestClient,mz_imageid,**kwargs):
    tags = kwargs.get('tags','')
    mzclient = MozuRestClient(mz_imageid=mz_imageid,tags=tags)
    update_resp = update_tags_mz_image(MozuRestClient, mz_imageid)
    return update_resp

# PUT - Upload UPDATE Image/DocumentContent - InsertNew/Update ie. upsert
def upsert_content_mz_image(MozuRestClient,src_filepath=None,mz_imageid=None,**kwargs):
    tags = kwargs.get('tags','')
    mzclient = MozuRestClient(mz_imageid=mz_imageid,src_filepath=src_filepath,tags=tags)
    update_resp = update_tags_mz_image(MozuRestClient, mz_imageid)
    return update_resp

# DELETE - Delete Image/DocumentContent
def delete_document_content(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    delete_resp = mzclient.delete_mz_image()
    print locals()
    return delete_resp.headers


def upload_new(MozuRestClient,src_filepath,**kwargs):
    tags=kwargs.get('tags','')
    mzclient = MozuRestClient(src_filepath=src_filepath,tags=tags)
    doc_resp = mzclient.create_new_mz_image()
    return doc_resp


###########################
### Main - Conditions ##
def main(insert_list_filepaths):
    import sqlalchemy
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    from mozu_image_util_functions import *

    compiled_instance_vars = compile_todict_for_class_instance_variables(insert_list_filepaths)
    
    for k,v in compiled_instance_vars.iteritems():
        src_filepath = k 
        bf_imageid = v['bf_imageid']
        mz_imageid = v['mz_imageid']
        md5checksum = v['md5checksum']
        tags        = v['tags']

        #image_metadata = v['image_metadata']
        mozu_image_table = mozu_image_table_instance()

        try:
            mozu_client = MozuRestClient(dict(**v))
            mz_imageid = upload_new(mozu_client,src_filepath)
            load_content_resp = upsert_content_mz_image(mozu_client, src_filepath=src_filepath,tags=tags) 
            if load_content_resp.http_status_code < 400:
                v['mz_imageid'] = mz_imageid
                insert_db = mozu_image_table.insert(values=dict(**v))
                insert_db.execute()
                print 'Inserted --> ', v.items(), ' <-- ', insert_db
            elif load_content_resp.http_status_code == 409:
                mz_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == v['bf_imageid']) ) )
                upsert_content_resp = upsert_content_mz_image(mozu_client,dict(**v))
                if upsert_content_resp.http_status_code < 300:
                    update_db = mozu_image_table.update(values=dict(**v),whereclause=mozu_image_table.c.bf_imageid==v['bf_imageid'])
                res = update_db.execute()
                print res, 'Updated--> ', v.items(), ' <-- ', update_db
            else:
                print("HTTP Status: {}\n Raising Integrity Error").format(load_content_resp.http_status_code)
                raise sqlalchemy.exc.IntegrityError()
        # Update
        except sqlalchemy.exc.IntegrityError:
            print 'IntegrityError ', v
            mozu_client = MozuRestClient(dict(**v))
            mz_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == v['bf_imageid']) ) )
            upsert_content_resp = upsert_content_mz_image(mozu_client,dict(**v))
            if upsert_content_resp.http_status_code < 300:
                update_db = mozu_image_table.update(values=dict(**v),whereclause=mozu_image_table.c.bf_imageid==v['bf_imageid'])
                res = update_db.execute()
            print res, 'Updated with Integrity Errors --> ', v.items(), ' <-- ', update_db
            pass

## Run in shell as mozu_exec.py *args
if __name__ == '__main__':
    import sys
    import os.path as path
    insert_list = []
    try:
        if path.isfile(sys.argv[1]):
            for arg in sys.argv:
                insert_list.append(arg)##'/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'    
        insert_list_filepaths = list(set(sorted(insert_list)))
        main(insert_list_filepaths)
    except IndexError:
        print("To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args")
