from database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey
from flask.json import JSONEncoder as BaseJSONEncoder


class JSONEncoder(BaseJSONEncoder):
    """Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JSONSerializer` mixin.
    """

    def default(self, obj):

        if isinstance(obj, (User, Role, RolesUsers)):
            if isinstance(obj, JSONSerializer):
                print('is instance')
                return obj.to_json()
        else:
            return None


class JSONSerializer(object):
    """A mixin that can be used to mark a SQLAlchemy model class which
    implements a :func:`to_json` method. The :func:`to_json` method is used
    in conjuction with the custom :class:`JSONEncoder` class. By default this
    mixin will assume all properties of the SQLAlchemy model are to be visible
    in the JSON output. Extend this class to customize which properties are
    public, hidden or modified before being being passed to the JSON serializer.

    Stolen from https://github.com/dacb/viscount/blob/a1965fcf0537a64fcaa60f31e9b00fb09afc4ce0/viscount/utils.py#L39
    """

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv


class User(Base, UserMixin, JSONSerializer):
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

    def has_role(self, role):
        return role in self.roles


class RolesUsers(Base, JSONSerializer):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin, JSONSerializer):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class MasterTable(Base, JSONSerializer):
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
