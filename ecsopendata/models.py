from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

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
