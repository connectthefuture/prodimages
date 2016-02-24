#!/usr/bin/env python
# coding: utf-8

from mozu_image_util_functions import log
########################### DB Table Defs ############################
##
@log
def mozu_image_table_instance(**kwargs):
    import sqlalchemy
    import datetime
    from os import environ
    from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, DateTime
    from sqlalchemy import FetchedValue, Text, Sequence
    from sqlalchemy.dialects import oracle as oracle_dialect


    db_uri = environ['SQLALCHEMY_DATABASE_URI']

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


@log
def mozu_bfly_imageid_url_table_instance(**kwargs):
    import sqlalchemy
    import datetime
    from os import environ
    from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, DateTime
    from sqlalchemy import FetchedValue, Text, Sequence
    from sqlalchemy.dialects import oracle as oracle_dialect

    db_uri = environ['SQLALCHEMY_DATABASE_URI']

    engine = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
    metadata = MetaData(bind=engine)  #, quote_schema=True, schema='bfyqa1201')
    mozu_image_table = Table( 'mozu_image_media', metadata,
        #Column('id', Integer, Sequence('mozu_image_seq_trigger'), primary_key=True),
        Column('id', Integer, server_default=FetchedValue(), primary_key=True),
        Column('bf_imageid', String(19), unique=True, nullable=False),
        Column('mz_imageid', String(37)),
        Column('md5checksum', String(32), nullable=True),
        Column('mz_hypr_class', String(29), nullable=True),
        Column('cdn_zoom_url', String(199), nullable=True),
        Column('media_version', Integer(7), default=1),
        Column('created_date', oracle_dialect.DATE, server_default=FetchedValue()),
        Column('modified_date', oracle_dialect.DATE, onupdate=datetime.datetime.now),
        )
    return mozu_image_table


def main():
    pass


if __name__ == '__main__':
    main()
