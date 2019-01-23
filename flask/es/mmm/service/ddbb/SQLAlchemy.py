'''
Created on Jan 10, 2019

@author: manolo
'''
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app as app

dbPaht = app.config.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(dbPaht, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import es.mmm.service.ddbb.Models
    Base.metadata.create_all(bind=engine)
    