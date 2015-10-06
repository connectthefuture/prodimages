##Defining Tables

#The most common use of the MetaData object is in defining the tables in your schema. In order to define tables in the MetaData, you use the Table and Column classes as shown in the following example:
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

## classic mapping style
class MozuImage(object):
    def __init__(self,*args,**kwargs):
        self.bf_imageid = kwargs.get('bf_imageid')
        self.mz_imageid = kwargs.get('mz_imageid')
        self.md5checksum = kwargs.get('md5checksum')
        self.created_date = kwargs.get('created_date')
        self.modified_date = kwargs.get('modified_date')
        self.updated_count = kwargs.get('updated_count')

    # def __repr__(self):
    #     return '<BlueflyID: %s - MozuID: %s>' % (self.bf_imageid, self.mz_imageid)


from sqlalchemy.orm import mapper
mapper(MozuImage, mozu_image)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)


def session_multi_add_commit(Session, list_of_instances):
    sess = Session()
    sess.add_all(list_of_instances)
    sess.commit()


def insert_mozu_image(MozuImage, **kwargs): 
    MZ_TABLE = MozuImage
    NEW_MZ = MZ_TABLE
    NEW_MZ.bf_imageid = kwargs.get('bf_imageid')
    NEW_MZ.mz_imageid = kwargs.get('mz_imageid')
    NEW_MZ.md5checksum = kwargs.get('md5checksum')
    NEW_MZ.created_date = kwargs.get('created_date')
    NEW_MZ.modified_date = kwargs.get('modified_date')
    NEW_MZ.updated_count = kwargs.get('updated_count')
    #new_mz=NEW_MZ('bf_imageid'=bf_imageid,'mz_imageid'=mz_imageid,'md5checksum'=md5checksum,'created_date'=created_date,'modified_date'=modified_date,'updated_count'=updated_count)
    return NEW_MZ




varbfid='358598401.jpg'
varmzid='8b2d01b5-a57e-4a41-acea-b2201c4eb926' 
varmd5='9678727d35c137f9e04b8c7e769b394a'

k1=['bf_imageid', 'mz_imageid', 'md5checksum']
v1=['360534401_alt02.jpg', '19caaf58-053e-44d8-bdcf-91499c7993f6', '8b75c5299ce164cc562f457a9bdf0ac5']
v2=['360534401_alt03.jpg', '32ce68ac-949f-4dca-8a84-8a865011d57a', '65a8d8d3b92b3bdf79a462309356ba0c']

insert_list = []
insert_list.append(dict(bf_imageid=varbfid, mz_imageid=varmzid, md5checksum=varmd5))
insert_list.append(dict(zip(k1,v1)))
insert_list.append(dict(zip(k1,v2)))


instance_list = []
for i in insert_list:
    mozu_image_table = mozu_image
    insert_records = mozu_image_table.insert(i)
    update_records = mozu_image_table.update(values=dict(**i),whereclause=mozu_image.c.mz_imageid==varmzid)
    engine.execute()
    if i['bf_imageid']:
        instance_list.append(mozu_image_table.insert(**i))



#session_multi_add_commit(Session, [i])
#(s, bfid=varbfid, md5=varmd5)
##############################

class BaseTableClass(Table):
    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)

# quote=True, quote_schema=True
##############
### Bind params to Select Statement to pass as kwargs at execution time
from sqlalchemy.sql import bindparam
s_bfid = mozu_image.select(mozu_image.c.bf_imageid == bindparam('bfid'))
s_mzid = mozu_image.select(mozu_image.c.mz_imageid == bindparam('mzid'))
s_md5  = mozu_image.select(mozu_image.c.md5checksum == bindparam('md5'))




##########
## Inserts
##########
def insert_mozu_image(**kwargs): 
    mozu_image.insert()

##########
## Updates
#u_where_bfid_md5 = 
#u_where_bfid_notmd5 = 

# u_where_bfid_notmd5 = 

varbfid='358598401.jpg'
varmzid='8b2d01b5-a57e-4a41-acea-b2201c4eb926' 
varmd5='9678727d35c137f9e04b8c7e769b394a'
s_insert = dict(bfid=varbfid, mzid=varmzid, md5=varmd5)


#### Connection
db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
conn = sqlalchemy.create_engine(db_uri, implicit_returning=False, coerce_to_decimal=False))


### Execute Statments
conn.execute(s, bfid=varbfid, md5=varmd5).fetchall()


# def get_mzimg_oracle_connection():
#     import sqlalchemy,sys
#     orcl_engine = sqlalchemy.create_engine('oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201')
#     cur = orcl_engine.raw_connection().cursor()
#     conn = orcl_engine.connect()
#     print(dir(conn))
#     return conn, cur






# db_uri = 'oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201'
# conn = sqlalchemy.create_engine(db_uri, implicit_returning=False)
# conn.execute(ins, dict(insert_vars))

# db = create_engine('oracle+cx_oracle://MZIMG:p1zza4me@qarac201-vip.qa.bluefly.com:1521/bfyqa1201')
# mozu_image_reflect = Table('mozu_image', metadata, autoload=True, autoload_with=db)

# ##Unlike some other database mapping libraries, SQLAlchemy fully supports the use of composite and non-integer primary and foreign keys:
# brand_table = Table( 'brand', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', Unicode(255), unique=True, nullable=False)
#     )


# product_table = Table( 'product', metadata,
#     Column('brand_id', Integer, ForeignKey('brand.id'), primary_key=True),
#     Column('sku', Unicode(80), primary_key=True)
#     )

# style_table = Table( 'style', metadata,
#     Column('brand_id', Integer, primary_key=True), 
#     Column('sku', Unicode(80), primary_key=True), 
#     Column('code', Unicode(80), primary_key=True),
#     )
