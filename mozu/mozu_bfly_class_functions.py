#!/usr/bin/env python
# coding: utf-8

## Use Classes - Could be in separate file
# from RESTClient import MozuRestClient
def count_total__files_documents(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    totalCount = mzclient.get_mz_image()['totalCount']
    print "Total Files in DocumentList: {}".format(totalCount)
    return totalCount


def list_files_documents(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    image_data = mzclient.get_mz_image()['items']
    #print image_data
    return image_data


def read_document_content_headers(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    image_data = mzclient().get_mz_image_headers()
    print image_data
    return image_data


def update_tags_mz_image(MozuRestClient,mz_imageid,**kwargs):
    tags = kwargs.get('tags','')
    mzclient = MozuRestClient(mz_imageid=mz_imageid,tags=tags)
    update_resp = update_tags_mz_image(MozuRestClient, mz_imageid)
    return update_resp


def upsert_content_mz_image(MozuRestClient,src_filepath=None,mz_imageid=None,**kwargs):
    tags = kwargs.get('tags','')
    mzclient = MozuRestClient(mz_imageid=mz_imageid,src_filepath=src_filepath,tags=tags)
    update_resp = update_tags_mz_image(MozuRestClient, mz_imageid)
    return update_res


def delete_document(MozuRestClient,mz_imageid):
    mzclient = MozuRestClient(mz_imageid=mz_imageid)
    delete_resp = mzclient.delete_mz_image()
    print locals()
    return delete_resp.headers


def upload_new(MozuRestClient,src_filepath,**kwargs):
    tags=kwargs.get('tags','')
    mzclient = MozuRestClient(src_filepath=src_filepath,tags=tags)
    doc_resp = mzclient.create_new_mz_image()
    return doc_resp


########################### DB Table Defs ############################
##
def mozu_image_table_instance(**kwargs):
    import sqlalchemy, datetime
    from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, create_engine
    from sqlalchemy import Sequence, FetchedValue, Text
    from sqlalchemy.dialects import oracle as oracle_dialect

    db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
    engine = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
    metadata = MetaData(bind=engine)  #, quote_schema=True, schema='bfyqa1201')
    mozu_image_table = Table( 'mozu_image', metadata,
        #Column('id', Integer, Sequence('mozu_image_seq_trigger'), primary_key=True),
        Column('id', Integer, server_default=FetchedValue(), primary_key=True),
        Column('bf_imageid', String(19), unique=True, nullable=False),
        Column('mz_imageid', String(37)), 
        Column('md5checksum', String(32)),
        Column('created_date', oracle_dialect.DATE, server_default=FetchedValue()), 
        Column('modified_date', oracle_dialect.DATE, onupdate=datetime.datetime.now), 
        Column('updated_count', Integer, default=0)    
        )
    return mozu_image_table

###########################
### Main - Conditions ##
def main(insert_list_filepaths):
    import sqlalchemy
    from mozu_image_util_functions import *
    from RESTClient import MozuRestClient
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
            mz_imageid = upload_new(MozuRestClient,src_filepath)
            load_content_resp = upsert_content_mz_image(src_filepath=src_filepath,tags=tags) 
            v['mz_imageid'] = mz_imageid
            insert_records = mozu_image_table.insert(values=dict(**v))
            insert_records.execute()
            print 'Inserted --> ', v.items(), ' <-- ', insert_records
        # Update
        except sqlalchemy.exc.IntegrityError:
            print 'IntegrityError ', v
            old_mz_imageid = mozu_image_table.select(
                whereclause=( (mozu_image_table.c.bf_imageid == v['bf_imageid'])  & (mozu_image_table.c.md5checksum <> v['md5checksum']) )
                )
            update_records = mozu_image_table.update(values=dict(**v),whereclause=mozu_image_table.c.bf_imageid==v['bf_imageid'])
            res = update_records.execute()
            print res, 'Updated--> ', v.items(), ' <-- ', update_records
            pass

if __name__ == '__main__':
    import sys
    import os.path as path
    if path.isfile(sys.argv[1]):
        insert_list_filepaths =  sys.argv[1] ##'/mnt/Post_Complete/Complete_Archive/xTestFiles/xTestMarketplace/999999/360128501.png'
        main([insert_list_filepaths])


