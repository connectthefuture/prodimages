#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *

class MozuImage(Base):
	__table__ 	  = 'mozu_image'
	# id 			  = (Integer, Sequence('mozu_image_id_seq'), primary_key=True)
    id 			  =  Column(Integer, server_default=FetchedValue(), primary_key=True)
    bf_imageid    =  Column(String(19), unique=True, nullable=False)
    mz_imageid    =  Column(String(37)) 
    md5checksum   =  Column(String(32))
    created_date  =  Column(DateTime, server_default=FetchedValue()) 
    modified_date =  Column(DateTime, onupdate=datetime.datetime.now)
    upload_count  =  Column(Integer, default=0)    


class NewMozuImage(MozuImage):


class UpdatedMozuImage(MozuImage):
