#!/usr/bin/env python

def mozu_image_table_instance(**kwargs):
    import sqlalchemy
    from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, create_engine
    from sqlalchemy import Sequence, FetchedValue, Text
    #from sqlalchemy.dialects import oracle as oracle_dialect
    import datetime

    db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
    engine = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
    metadata = MetaData(bind=engine)  #, quote_schema=True, schema='bfyqa1201')
    mozu_image_table = Table( 'mozu_image', metadata,
        #Column('id', Integer, Sequence('mozu_image_seq'), primary_key=True),
        Column('id', Integer, server_default=FetchedValue(), primary_key=True),
        Column('bf_imageid', String(19), unique=True, nullable=False),
        Column('mz_imageid', String(37)), 
        Column('md5checksum', String(32)),
        Column('created_date', DateTime, server_default=FetchedValue()), 
        Column('modified_date', DateTime, onupdate=datetime.datetime.now), 
        Column('updated_count', Integer, default=0)    
        )
    return mozu_image_table


# def insert_update_mozu_image(**kwargs):
#     i = dict(bf_imageid=kwargs.get(bf_imageid), 
#              mz_imageid=kwargs.get(mz_imageid), 
#              md5checksum=kwargs.get(md5checksum))

#     mozu_image_table = mozu_image_table_instance()
#     insert_records = mozu_image_table.insert(i)
#     update_records = mozu_image_table.update(values=dict(**i),whereclause=mozu_image.c.bf_imageid==bf_imageid)
#     try:
#         res = insert_records.execute()
#         print 'InsertResult --> ', res
#         return res

#     except:
#         print 'IntegrityError ', i
#         res = update_records.execute()
#         print 'InsertResult --> ', res
#         return res
#         #pass


def main_upload_post(src_filepath, **kwargs):
    import os.path as path
    ## Convert it to jpg if not one (ie png, tiff, gif)
    src_basename = path.basename(src_filepath)
    ext = src_basename.split('.')[-1].lower().replace('jpeg','jpg')
    if src_basename[:9].isdigit() and ext:
        bf_imageid = path.basename(src_filepath)  # .split('.')[0]
    else:
        bf_imageid = ''

    mz_imageid = ''
    md5checksum = md5_checksumer(src_filepath)

    #md5colorstyle_exists = orcl_validate_md5checksum(md5checksum, bf_imageid=bf_imageid)
    # 1A Validate md5 # TODO: NEW # sqlalchemy 
    if bf_imageid: 
        OLDbf_imageid = select('bf_imageid').where('md5checksum'==md5checksum).execute()
        if bf_imageid == OLDbf_imageid:  
            md5colorstyle_exists = md5checksum
        else: 
            md5colorstyle_exists = ''
            if ext == 'jpg':
                pass
            else:
                src_filepath = magick_convert_to_jpeg(src_filepath, destdir=None)

    args = [
        {'bf_imageid': bf_imageid },
        {'mz_imageid': mz_imageid },
        {'md5checksum': md5checksum }
        ]

    #md5colorstyle_exists = orcl_validate_bf_imageid(bf_imageid=bf_imageid).execute()
    # 1B Validate bf_imageid_exists # TODO: NEW # sqlalchemy 
    bf_imageid_exists = select('*').where('bf_imageid'==bf_imageid)   
    if bf_imageid_exists.execute():
        if bf_imageid_exists.where('md5checksum'!=md5checksum).execute():
            mz_imageid = select('mz_imageid').where('bf_imageid'==bf_imageid)
    else:
        NEWBFLY_INSERT = True

    import json
    json_insert = json.dumps(args)

    ## Finished collecting k/v data to send now send if md5colorstyle_exists returns False (meaning we dont have an image for this yet)
    if NEWBFLY_INSERT and not md5colorstyle_exists:
        try:
            mz_imageid, content_response = upload_productimgs_mozu(src_filepath)
            orcl_insert_bf_imageid_mz_imageid(bf_imageid, mz_imageid, md5checksum)
            # 2 Insert # TODO: NEW # sqlalchemy 
            insert_update_mozu_image(**args)
            printoutput = 'bf_imageid={}\tmz_imageid={}\tmd5checksum={}\n'.format(bf_imageid, mz_imageid, md5checksum).split()
            mr_logger('/mnt/mozu_upload.txt', printoutput)
            print printoutput, ' Line-420RESULT'
            return mz_imageid, bf_imageid
        except TypeError, e:
            print '\n\t...', src_filepath, ' None TypeError --> ', e
            pass
    elif bf_imageid_exists and not md5colorstyle_exists:
        updated_mz_imageid, content_response = upload_productimgs_mozu(src_filepath, mz_imageid=mz_imageid)
        orcl_update_bf_imageid_mz_imageid(bf_imageid, updated_mz_imageid, md5checksum=md5checksum)
        # 3 Update # TODO: NEW # sqlalchemy table.update()
    else:
        print md5colorstyle_exists, ' \n\t<-- Duplicated - Passing -- Exists -- with --> ', bf_imageid, bf_imageid_exists

# if NEWBFLY_INSERT and not md5colorstyle_exists:
#         try:
#             mz_imageid, content_response = upload_productimgs_mozu(src_filepath)
#             orcl_insert_bf_imageid_mz_imageid(bf_imageid, mz_imageid, md5checksum)
#             # 2 Insert # TODO: NEW # sqlalchemy 
#             insert_update_mozu_image(**args)
#             printoutput = 'bf_imageid={}\tmz_imageid={}\tmd5checksum={}\n'.format(bf_imageid, mz_imageid, md5checksum).split()
#             mr_logger('/mnt/mozu_upload.txt', printoutput)
#             print printoutput, ' Line-420RESULT'
#             return mz_imageid, bf_imageid
#         except TypeError, e:
#             print '\n\t...', src_filepath, ' None TypeError --> ', e
#             pass

    if bf_imageid_exists and not md5colorstyle_exists:
        updated_mz_imageid, content_response = upload_productimgs_mozu(src_filepath, mz_imageid=mz_imageid)
        orcl_update_bf_imageid_mz_imageid(bf_imageid, updated_mz_imageid, md5checksum=md5checksum)
        # 3 Update # TODO: NEW # sqlalchemy table.update()
    else:
        print md5colorstyle_exists, ' \n\t<-- Duplicated - Passing -- Exists -- with --> ', bf_imageid, bf_imageid_exists

def main(**kwargs):
    insert_list = []
    # for f in sys.argv:
    #     insert_list.append(f)
    args = dict(bf_imageid=kwargs.get(bf_imageid), 
                            mz_imageid=kwargs.get(mz_imageid), 
                            md5checksum=kwargs.get(md5checksum))

    mozu_image_table = mozu_image
    # Insert
    try:
        mz_imageid, content_response = upload_productimgs_mozu(src_filepath)
        args['mz_imageid'] == mz_imageid
        insert_records = mozu_image_table.insert(**args)
        insert_records.execute()
        print 'Inserted --> ', args, ' <-- ', insert_records
    # Update
    except:
        print 'IntegrityError ', args
        update_records = mozu_image_table.update(values=dict(**args),whereclause=mozu_image_table.c.bf_imageid==bf_imageid)
        res = update_records.execute()
        print 'Updated--> ', args, ' <-- ', update_records
        pass



if __name__ == '__main__':
    main()
