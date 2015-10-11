
# coding: utf-8

###########################
######################################################
###########################


###########################
######################################################
###########################

######################################################
###########################
### DB - oracle Alchemy Funcs and Table Defs
##
########################### Replaced By Alchemy ############################

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
######################################################
###########################
### Main - Conditions ##
def main(insert_list_filepaths):
    #insert_list = []
    # for f in sys.argv:
    #     insert_list.append(f)
    import sqlalchemy
    images_insert_dict = compile_data_db_import(insert_list_filepaths)
    # Insert
    for k,v in images_insert_dict.iteritems():
        bf_imageid = v['bf_imageid']
        mz_imageid = v['mz_imageid']
        md5checksum = v['md5checksum']
        #image_metadata = v['image_metadata']
        mozu_image_table = mozu_image_table_instance()
        try:
            mz_imageid, content_response = upload_productimgs_mozu(k)
            v['mz_imageid'] = mz_imageid
            insert_records = mozu_image_table.insert(values=dict(**v))
            insert_records.execute()
            print 'Inserted --> ', v.items(), ' <-- ', insert_records
        # Update
        except sqlalchemy.exc.IntegrityError:
            print 'IntegrityError ', v
            old_mz_imageid = mozu_image_table.select(whereclause=(
                                                                (mozu_image_table.c.bf_imageid == v['bf_imageid']) 
                                                                &
                                                                (mozu_image_table.c.md5checksum <> v['md5checksum'])
                                                                )
                                                    )
            #updated_mz_imageid, content_response = upload_productimgs_mozu(k, mz_imageid=old_mz_imageid)
            updated_mz_imageid =  v['mz_imageid'].replace('-','_')
            v['mz_imageid'] = updated_mz_imageid
            update_records = mozu_image_table.update(values=dict(**v),whereclause=mozu_image_table.c.bf_imageid==v['bf_imageid'])
            res = update_records.execute()
            print res, 'Updated--> ', v.items(), ' <-- ', update_records
            pass



        



