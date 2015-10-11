#!/usr/bin/env python
# coding: utf-8

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


def main():
    pass


if __name__ == '__main__':
    main()
