# coding: utf-8
from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy import Integer, String, Text
from sqlalchemy import Sequence, FetchedValue
from sqlalchemy.dialects import oracle as oracle_dialect
from sqlalchemy.orm import mapper, sessionmaker
from bfqa1_classicmodel_alchemy import mozu_image_table_instance
#----------------------------------------------------------------------

class ProductColor(object):
    pass


class MozuImage_(object):
    pass


class ImageMetadata(object):
    pass


def bfyqa1201_engine_creator():
	db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
    engine = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
	return engine

#----------------------------------------------------------------------
def mozu_image_table_instance(**kwargs):
    import sqlalchemy, datetime
    from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, create_engine, Sequence
    from sqlalchemy import Sequence, FetchedValue, Text
    from sqlalchemy.dialects import oracle as oracle_dialect

    metadata = MetaData(bind=bfyqa1201_engine_creator())  #, quote_schema=True, schema='bfyqa1201')
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

def image_metadata_table_instance(**kwargs):
    import sqlalchemy, datetime
    from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, create_engine, Sequence
    from sqlalchemy import Sequence, FetchedValue, Text
    from sqlalchemy.dialects import oracle as oracle_dialect
	
	metadata = MetaData(bind=bfyqa1201_engine_creator()) 
	image_metadata_table = Table( 'image_metadata', metadata,
        Column('id', Integer, Sequence('image_metadata_seq'), primary_key=True),
        #Column('id', Integer, server_default=FetchedValue(), primary_key=True),
        Column('bf_imageid', String(19), ForeignKey("mozu_image.bf_imageid"),
		Column('metadata_array', Array, nullable=False)

#----------------------------------------------------------------------
def loadSession(TableClassName,table_instance):
    """"""
    mapper(TableClassName, table_instance)
    Session = sessionmaker(bind=table_instance.metadata.engine)
    session = Session()


if __name__ == "__main__":
    metaData_session = loadSession(ImageMetadata)
    mozuImage_session = loadSession(MozuImage)
    mozuRes = mozuImage_session.query().all()
    metadataRes = metaData_session.query().all()
    print mozuRes[1].id

