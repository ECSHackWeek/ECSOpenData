from sqlalchemy import Boolean, DateTime, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MasterTable(Base):
    __tablename__ = 'master_table'
    # Here we define columns for the master_table
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    data_name = Column(String(250), nullable=False) 
    # this is some sort of description - or just users name?
    exp_class = Column(String(250), nullable=False) 
    authors = Column(String(250), nullable=False)
    doi = Column(String(250), nullable=False)
    paper_title = Column(String(250), nullable = False)
    journal = Column(String(250), nullable = False)
    pub_year = Column(String(250), nullable = False)
