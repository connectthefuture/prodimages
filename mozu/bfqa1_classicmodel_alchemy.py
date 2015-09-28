import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, create_engine
from sqlalchemy import Sequence, FetchedValue, Text
#from sqlalchemy.dialects import oracle as oracle_dialect
import datetime


##### Table and Metadata Create Obj
db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
engine = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False)
metadata = MetaData(bind=engine)  #, quote_schema=True, schema='bfyqa1201')
mozu_image = Table( 'mozu_image', metadata,
    #Column('id', Integer, Sequence('mozu_image_id_seq'), primary_key=True),
    Column('id', Integer, server_default=FetchedValue(), primary_key=True),
    Column('bf_imageid', String(19), unique=True, nullable=False),
    Column('mz_imageid', String(37)), 
    Column('md5checksum', String(32)),
    Column('created_date', DateTime, server_default=FetchedValue()), 
    Column('modified_date', DateTime, onupdate=datetime.datetime.now), 
    Column('updated_count', Integer, default=0)    
    )

varbfid='358598401.jpg'
varmzid='8b2d01b5-a57e-4a41-acea-b2201c4eb926' 
varmd5='9678727d35c137f9e04b8c7e769b394a'

k1=['bf_imageid', 'mz_imageid', 'md5checksum']
v1=['360534401_alt02.jpg', '19caaf58-053e-44d8-bdcf-91499c7993f6', '8b75c5299ce164cc562f457a9bdf0ac5']
v2=['360534401_alt03.jpg', '32ce68ac-949f-4dca-8a84-8a865011d57a', '65a8d8d3b92b3bdf79a462309356ba0c']

insert_list = []
# for f in sys.argv:
#     insert_list.append(f)
insert_list.append(dict(bf_imageid=varbfid, mz_imageid=varmzid, md5checksum=varmd5))
insert_list.append(dict(zip(k1,v1)))
insert_list.append(dict(zip(k1,v2)))


instance_list = []
for i in insert_list:
    mozu_image_table = mozu_image
    insert_records = mozu_image_table.insert(i)
    update_records = mozu_image_table.update(values=dict(**i),whereclause=mozu_image.c.bf_imageid==varbfid)
    try:
        engine.execute(insert_records)
    except:
        print 'IntegrityError ', i
        engine.execute(update_records)
        pass


