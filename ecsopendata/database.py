import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL_PREFIX = 'sqlite:///'
DATABASE_PATH = 'test.db'
DATABASE_URL = DATABASE_URL_PREFIX + DATABASE_PATH

engine = create_engine(DATABASE_URL, \
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from models import *
def init_db():
#    import models
#    from models import *
    Base.metadata.create_all(bind=engine)
    if not os.path.exists(DATABASE_PATH):
    	# replace this if statement with sqlalchemy if table doesn't exist in master table:
        print("Template database will be created")
        #import models
        #Base.metadata.create_all(bind = engine)
        print("call init master table")
        print("import example data")
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
 
