#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, create_engine
from sqlalchemy import Sequence, FetchedValue, Text
#from sqlalchemy.dialects import oracle as oracle_dialect
import datetime

db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
engine = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
mdata = MetaData(bind=engine, quote_schema=True, schema='mz_image')
Base = declarative_base(bind=engine, metadata=mdata, name='BaseBfyqa1201')

engine = None
def setup_database(dburl, echo, num):
    global engine
    engine = create_engine(dburl, echo=echo)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

class MozuImage(Base):
    __table__     = 'mozu_image'
    # id              = (Integer, Sequence('mozu_image_id_seq'), primary_key=True)
    id            =  Column(Integer(), server_default=FetchedValue(), primary_key=True)
    bf_imageid    =  Column(String(19), unique=True, nullable=False)
    mz_imageid    =  Column(String(37)) 
    md5checksum   =  Column(String(32))
    created_date  =  Column(DateTime(), server_default=FetchedValue()) 
    modified_date =  Column(DateTime(), onupdate=datetime.datetime.now)
    upload_count  =  Column(Integer(), default=0)    


class NewMozuImage(MozuImage):


class UpdatedMozuImage(MozuImage):
