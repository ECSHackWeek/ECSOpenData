import pandas as pd
import pandas.io.sql as pd_sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3 as sql
 
from sqlalchemy_declarative import MasterTable, Base
 
engine = create_engine('sqlite:///sqlalchemy_example.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
 
# For every new entry in the database we will update the master
# table and we will add the file as a pandas dataframe
 
# below is adding a pandas dataframe to the database as a new table 
# named NLTcyclingdata
filename = 'NLTcyclingdata'
ex_df = pd.read_excel('example_data/CS2_33_8_17_10.xlsx', 1) 
# be sure to change the sheet number on the read_excel depending on a user input? 
con = sql.connect('sqlalchemy_example.db')
c = con.cursor()
ex_df.to_sql(filename, con, if_exists="replace")


# Insert a new entry of meta data in the master  table
new_entry = MasterTable(data_name='NLTcyclingdata', 
						 exp_class='Cycling',
						 authors= 'Me, myself and I',
						 doi= 'somedoi',
 						 paper_title= 'My Amazing Paper Title', 
						 journal= 'Journal of Me', 
						 pub_year= '1994')
session.add(new_entry)
session.commit()
