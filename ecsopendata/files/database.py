# this is the database.py within the files folder
import os
import pandas as pd
import sqlite3 as sql
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists
from models import Base 
from models import MasterTable


# dataset_path = '../example_data/example3.xlsx'
# filename = 'example1'
# database_path = 'files_test.db'
# id= 18 # this is the file ID and needs to be different for each file uploaded
# exp_class='Cycling'
# authors= 'Me, myself and I'
# doi= 'somedoi'
# paper_title= 'My Amazing Paper Title'
# journal= 'Journal of Me'
# pub_year= '194'



def add_datafiles(dataset_path, filename, database_path, id, exp_class, authors, doi, paper_title, journal, pub_year):
# this function adds a dataset to the database, must be in an excel format
	DATABASE_URL_PREFIX = 'sqlite:///'
	DATABASE_PATH = 'files_test.db'
	DATABASE_URL = DATABASE_URL_PREFIX + DATABASE_PATH

	engine = create_engine(DATABASE_URL, convert_unicode=True)
	db_session = scoped_session(sessionmaker(autocommit=False,
											 autoflush=False,
											 bind=engine))

	Base.query = db_session.query_property()

	Base.metadata.create_all(engine)

	if not engine.dialect.has_table(engine, filename):
		# then that table doesn't exist in the db
		print("that table does not exist yet- adding it now ")
		# insert the actual data
		ex_df = pd.read_excel(dataset_path, 1) 
		# be sure to change the sheet number on the read_excel depending on a user input? 
		con = sql.connect(database_path)
		c = con.cursor()
		ex_df.to_sql(filename, con, if_exists="replace")
		con.close()
		# Insert a new entry of meta data in the master  table
		new_entry = MasterTable(id = id, data_name=filename, 
								 exp_class=exp_class,
								 authors= authors,
								 doi= doi,
		 						 paper_title= paper_title, 
								 journal= journal, 
								 pub_year= pub_year)
		db_session.add(new_entry)
		db_session.commit()
		print("that table has been added")
	else:
		print("that table already exists")
	return 

