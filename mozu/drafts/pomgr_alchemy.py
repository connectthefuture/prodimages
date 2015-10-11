# coding: utf-8

from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapper, sessionmaker

class ProductColor(object):
    pass
 
#----------------------------------------------------------------------
def loadSession():
    """"""
    dbPath = 'places.sqlite'
 
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
 
    metadata = MetaData(engine)    
    pomgr_ProductColor = Table('pomgr_ProductColor', metadata, 
                          Column('id', Integer, primary_key=True),
                          Column('type', Integer),
                          Column('fk', Integer),
                          Column('parent', Integer),
                          Column('position', Integer),
                          Column('title', String),
                          Column('keyword_id', Integer),
                          Column('folder_type', Text),
                          Column('dateAdded', Integer),
                          Column('lastModified', Integer)
                          )
 
    mapper(ProductColor, pomgr_ProductColor)
 
    Session = sessionmaker(bind=engine)
    session = Session()
 
if __name__ == "__main__":
    session = loadSession()
    res = session.query(ProductColor).all()
    print res[1].title