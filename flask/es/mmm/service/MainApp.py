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