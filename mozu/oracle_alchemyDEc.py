#!/usr/bin/env python[]
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

DeclarativeBase = declarative_base()

DATABASE = {
    'drivername': 'cx_oracle',
    'host': 'qarac201-vip.qa.bluefly.com',
    'port': '1521',
    'username': 'MZIMG',
    'password': 'p1zza4me',
    'database': 'bfyqa1201'
}

def db_engine_create():
    """
    Performs database connection using database settings from DATABASE dict above
    Returns sqlalchemy engine instance
    """
    global engine
    engine = create_engine(URL(**settings.DATABASE))
    return engine

def create_mozu_image_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class MozuImage(DeclarativeBase):
    __table__     = 'mozu_image'
    # id              = (Integer, Sequence('mozu_image_id_seq'), primary_key=True)
    id            =  Column(Integer(), server_default=FetchedValue(), primary_key=True)
    bf_imageid    =  Column(String(19), unique=True, nullable=False)
    mz_imageid    =  Column(String(37)) 
    md5checksum   =  Column(String(32))
    created_date  =  Column(DateTime(), server_default=FetchedValue()) 
    modified_date =  Column(DateTime(), onupdate=datetime.datetime.now)
    upload_count  =  Column(Integer(), default=0)    


class InsertMozuImage(MozuImage):
    pass

class UpdateMozuImage(MozuImage):
    pass


def session_multi_add_commit(Session, list_of_instances):
    sess = Session()
    sess.add_all(list_of_instances)
    sess.commit()

###############
### MozuPipe ##
###############
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

class MozuImagePipeline(object):
    """MozuImage pipeline for storing scraped items in the database"""
    def __init__(self, **kwargs):
        """
        Initializes database connection and sessionmaker.
        Creates MozuImage table.
        """
        engine = db_engine_create()
        create_mozu_image_table(engine)
        self.Session = sessionmaker(bind=engine)
        if kwargs.get('list_of_instances'):
            self.list_of_instances = kwargs.get('list_of_instances')
        else:
            self.list_of_instances = []


    def process_item(self, item, data):
        """Save MozuImage in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()
        _mozu_image = MozuImage(**item)
        try:
            session.add(_mozu_image)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item


    def process_multiple_items(Session, list_of_instances):
        sess = Session()
        sess.add_all(list_of_instances)
        sess.commit()

