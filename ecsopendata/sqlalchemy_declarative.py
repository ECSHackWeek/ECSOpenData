import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

 
Base = declarative_base()
 
class MasterTable(Base):
    __tablename__ = 'master_table'
    # Here we define columns for the master_table
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    data_name = Column(String(250), nullable=False) # this is some sort of description - or just users name?
    exp_class = Column(String(250), nullable=False) 
    authors = Column(String(250), nullable=False)
    doi = Column(String(250), nullable=False)
    paper_title = Column(String(250), nullable = False)
    journal = Column(String(250), nullable = False)
    pub_year = Column(String(250), nullable = False)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example.db')


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)