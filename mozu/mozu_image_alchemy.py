# coding: utf-8
from sqlalchemy import Column, DateTime, Numeric, String, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class MozuImage(Base):
    __tablename__ = 'mozu_image'

    id = Column(Numeric(scale=0, asdecimal=False), server_default=text("NULL "))
    bf_imageid = Column(String(19), primary_key=True, server_default=text("NULL "))
    mz_imageid = Column(String(37), server_default=text("NULL "))
    md5checksum = Column(String(32), server_default=text("NULL "))
    created_date = Column(DateTime, server_default=text("sysdate "))
    modified_date = Column(DateTime, server_default=text("NULL "))
    updated_count = Column(Numeric(scale=0, asdecimal=False), server_default=text("0 "))
