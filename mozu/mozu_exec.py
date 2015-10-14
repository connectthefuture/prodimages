#!/usr/bin/env python
# coding: utf-8
import pdb;pdb.set_trace()

def count_total_files_documents(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    total_count = mzclient.get_mz_image_documents()['totalCount']
    print "Total Files in DocumentList: {}".format(total_count)
    return total_count


def list_documents():
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    documents = mzclient.get_mz_image_documents()['items']
    print documents
    return documents


# def download_document_content(outfile=None, **kwargs):
#     from RESTClient import MozuRestClient
#     print kwargs, 'KWARGS-26'
#     _mzclient = MozuRestClient(**kwargs)
#     from os import path as path
#     image_content = _mzclient[     if not _mzclient.bf_imageid:
#         # Get bflyid from Oracle using mz_id
#         from db import mozu_image_table_instance
#         bf_imageid = mozu_image_table_instance.select( whereclause=( (mozu_image_table_instance.c.mz_imageid == _mzclient.mz_imageid) ) )[0]['bf_imageid']
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

# PUT - Update Document Data
def update_tags_mz_image(**kwargs):
    from RESTClient import MozuRestClient
    print kwargs, 'KWARGS-56'
    _mzclient = MozuRestClient(**kwargs)
    update_resp = _mzclient.update_mz_image()
    print locals(), "Update Data"
    return update_resp

# PUT - Upload UPDATE Image/DocumentContent - InsertNew/Update ie. upsert
def upsert_content_mz_image(**kwargs):   # src_filepath=None,mz_imageid=None):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)   
    src_filepath = kwargs.get("src_filepath")
    update_resp = total_count = mzclient.send_content(src_filepath)
    print update_resp.headers, "UpsertContent"
    return update_resp

# DELETE - Delete Image/DocumentContent
def delete_document_content(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs) 
    delete_resp = mzclient.delete_mz_image()
    print delete_resp.headers, "Delete"
    return delete_resp

# Post New Image, Creates Document
def upload_new(**kwargs):
    from RESTClient import MozuRestClient
    mzclient = MozuRestClient(**kwargs)
    doc_resp = _mzclient.create_new_mz_image()
    return doc_resp


###########################
### Main - Conditions ##
def main(insert_list_filepaths):
    import sqlalchemy
    from RESTClient import MozuRestClient
    from db import mozu_image_table_instance
    from mozu_image_util_functions import compile_todict_for_class_instance_variables

    compiled_instance_vars = compile_todict_for_class_instance_variables(insert_list_filepaths)

    for k,v in compiled_instance_vars.iteritems():
        src_filepath = k
        bf_imageid = v['bf_imageid']
        mz_imageid = v['mz_imageid']
        md5checksum = v['md5checksum']
        tags        = v['tags']
        print locals(), 'LOCAL80', k, v
        #image_metadata = v['image_metadata']
        mozu_image_table = mozu_image_table_instance()

        try:
            print locals(), k, v, 'LOCAL87'
            v['mz_imageid'] = upload_new(**v)
            load_content_resp = upsert_content_mz_image(**v)
            if load_content_resp.http_status_code < 400:
                insert_db = mozu_image_table.insert(values=dict(**v))
                insert_db.execute()
                print 'Inserted --> ', v.items(), ' <-- ', insert_db
            elif load_content_resp.http_status_code == 409:
                orcl_res = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == v['bf_imageid']) ) )
                v['mz_imageid'] = orcl_res['mz_imageid']
                upsert_content_resp = upsert_content_mz_image(**v) #,dict(**v))
                if upsert_content_resp.http_status_code < 300:
                    update_db = mozu_image_table.update(values=dict(**v),whereclause=mozu_image_table.c.bf_imageid==v['bf_imageid'])
                    res = update_db.execute()
                    print res, 'Updated--> ', v.items(), ' <-- ', update_db
            else:
                print "HTTP Status: {}\n Raising Integrity Error".format(load_content_resp.http_status_code)
                raise sqlalchemy.exc.IntegrityError()
        # Update
        except sqlalchemy.exc.IntegrityError:
            print 'IntegrityError and everything is or will be commented out below because it is in the db already', v
            mz_imageid = mozu_image_table.select( whereclause=( (mozu_image_table.c.bf_imageid == v['bf_imageid']) ) )
            upsert_content_resp = upsert_content_mz_image(**v)
            if upsert_content_resp.http_status_code < 300:
                update_db = mozu_image_table.update(values=dict(**v),whereclause=mozu_image_table.c.bf_imageid==v['bf_imageid'])
                res = update_db.execute()
                print res, 'Updated with Integrity Errors --> ', v.items(), ' <-- ', update_db
            #pass

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
        print insert_list_filepaths
        main(insert_list_filepaths)
    except IndexError:
        print "To Run in shell you must provide at least 1 file path as an argument. \nArgs Separated by space. \n\t mozu_exec.py \*args"
