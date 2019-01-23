'''
Created on Jan 10, 2019

@author: manolo
'''
from pprint import pprint
from flask import Flask, jsonify, request, g, redirect, url_for, session
from flask_session import Session

from flask_cors.extension import CORS
from flask_session.sessions import MongoDBSessionInterface
from pymongo.mongo_client import MongoClient

from flask_bcrypt import Bcrypt
from logging.config import dictConfig
import logging


def create_app(config_filename='config'):
    "CREATE APP"
    app = Flask(__name__)
    app.config.from_object(config_filename)
    ###    CORS
    #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    
    ###    CREATE SESSION
    #app.secret_key = app.config['SECRET_KEY']
    sess = None
    if app.config['SESSION_TYPE'] == 'SESSION_MONGODB':
        ###    MONGO SESSION
        client = MongoClient('localhost', 27017)
        dataBase = 'session_camera'
        collection = 'sessions'
        keyPrefix = 'session:'
        sess = MongoDBSessionInterface(client,dataBase,collection,keyPrefix,False, True)
        #sess.open_session(app, request)
    else:
        ###    FLASK SESSION
        sess = Session()
        sess.init_app(app)
    
    ###    DATABASE
    with app.app_context():
        from es.mmm.service.ddbb.SQLAlchemy import init_db
        init_db()
        
    bcrypt = Bcrypt(app)
    app.bcrypt = bcrypt
    
    ###    CREATE BLUEPRINT
    
    from es.mmm.service.modules.Auth import serviceAuth
    app.register_blueprint(serviceAuth)
    
    @app.route('/')
    def home():
        "ACCESS HOME"
        data = dict()
        data['result'] = 'OK'
        data['action'] = 'home'
        data['message'] = 'Service is working'
        if request.args.keys():
            for key in request.args.keys():
                data[key] = request.args[key]
            
        return jsonify(**data)
    
    @app.errorhandler(404)
    def page_not_found(e):
        "Return to page not found"
        pprint(e)
        return redirect(url_for('home',page=request.path))
    
    ###    CREATE LOG
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
    ###    SET LEVEL LOG
    if app.config.get('DEBUG'):
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.ERROR)
    
    return app










'''
import os
from flask import Flask, request
#from bluePrints import authBlue
from flask import jsonify, session
from flask_session import Session
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')

database_file = "sqlite:///{}".format(os.path.join(app.config.get('PATH_IMAGE_FILE'), "bookdatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
from es.mmm.service.ddbb import models

###    CREATE SESSION
#SESSION_TYPE = 'SESSION_MONGODB'
#SECRET_KEY = os.urandom(16)
###
#app.secret_key = SECRET_KEY
#app.config['SESSION_TYPE'] = SESSION_TYPE

sess = Session()
sess.init_app(app)

###    CREATE BLUEPRINT

db.create_all();

#app.register_blueprint(simple_page)
#app.register_blueprint(authBlue)

@app.route('/', methods=('GET', 'POST'))
def home():
    book = models.Book(title='Nuevo')
    db.session.add(book)
    db.session.commit()

    for key in request.headers.keys():
        print(' {0} -> {1}'.format(key,request.headers.get(key)))

    header = request.headers.get('your-header-name')
    if header:
        pprint(header)

    remoteIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return jsonify(result='OK',message='I am alive',you_are=remoteIp)

print('FLASK APP CREATED')
'''