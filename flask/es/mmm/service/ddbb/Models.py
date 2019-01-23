'''
Created on 23 Jan 2019

@author: manuelmartinmartin
'''

'''
Created on 17 Jan 2019

@author: manuelmartinmartin
'''
from flask_bcrypt import Bcrypt
from flask import current_app as app
from sqlalchemy import Column, Integer, String, DateTime
from es.mmm.service.ddbb.SQLAlchemy import Base, db_session
from flask.helpers import flash
from sqlalchemy.sql import functions
from sqlalchemy.sql.schema import ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
import json

class User(Base):
    """This class defines the users table """
    __tablename__ = 'users'
    # Define the columns of the users table, starting with the primary key
    id = Column(Integer, primary_key=True)
    name = Column(String(50),nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    bucketlists = relationship('Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email='', password=''):
        """Initialize the user with an email and a password."""
        self.email = email
        if password:
            self.password = app.bcrypt.generate_password_hash(password).decode('utf-8')

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)
    
    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db_session.add(self)
        if self.name is None:
            self.name = self.email[:self.email.index('@')]
        
        result = False
        try:
            db_session.commit()
            result = True
        except Exception as error:
            app.logger.error(str(error))
            db_session.rollback()
            flash(str(error))
        return result
    
    @staticmethod
    def get(id=None,email=None):
        obj = None
        if email:
            obj = User.query.filter_by(email=email).first()
        elif id:
            obj = User.query.filter_by(id=id).first()
        else:
            obj = None
        return obj
        
    @staticmethod
    def get_all():
        """This method gets all the bucketlists for a given user."""
        return User.query.filter_by().all()
    
    def __repr__(self):
        return "<User: {0} {1} {2} {3}>".format(self.id,self.email,self.password, self.name)
        


def jsonDefault(OrderedDict):
    return OrderedDict.__dict__

class Bucketlist(Base,json.JSONEncoder):
    """This class defines the bucketlist table."""
    __tablename__ = 'bucketlists'
    #DEFINE CONSTANTS
    _CREATED = 1
    _ACCESS = 2
    _FAILURE= 3
    _DELETED = 4
    _CARS = [_CREATED, _ACCESS, _FAILURE, _DELETED]
    # define the columns of the table, starting with its primary key
    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    date_created = Column(DateTime, default=functions.current_timestamp())
    user_id = Column(Integer, ForeignKey(User.id))
    
    __table_args__ = (
            CheckConstraint(type.in_(_CARS)),
        )
    
    def __init__(self, type, user_id):
        """Initialize the bucketlist with a name and its creator."""
        self.type = type
        self.user_id = user_id

    def save(self):
        """Save a bucketlist.
        This applies for both creating a new bucketlist
        and updating an existing onupdate
        """
        db_session.add(self)
        result = False
        try:
            db_session.commit()
            result = True
        except Exception as error:
            app.logger.error(str(error))
            db_session.rollback()
            flash(str(error))
        return result
    
    @staticmethod
    def get_all(user_id):
        """This method gets all the bucketlists for a given user."""
        return Bucketlist.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_allJSON(user_id):
        jsonList = []
        list = Bucketlist.get_all(user_id)
        for v in list:
            jsonList.append(v.to_json())
        return jsonList

    def delete(self):
        """Deletes a given bucketlist."""
        db_session.delete(self)
        db_session.commit()

    def __repr__(self):
        """Return a representation of a bucketlist instance."""
        return "<Bucketlist: {0} {1}>".format(self.type, self.user_id)

    def to_json(self):
        "CREATE JSON OBJECT"
        return {
                'id':self.id,
                'type':self.type,
                'date_created':self.date_created.timestamp(),
                'user_id':self.user_id
            }
