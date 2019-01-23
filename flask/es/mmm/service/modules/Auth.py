'''
Created on 23 Jan 2019

@author: manuelmartinmartin
'''

from flask import jsonify
from flask import Blueprint, request, session, g
from flask import current_app as app

from es.mmm.service.ddbb.Models import User, Bucketlist
from flask.helpers import get_flashed_messages
from es.mmm.service.shared.Security import login_required
import json
from pprint import pprint

###    CHECK
def validateUsrAPass(request):
    "Method to validate username and password"
    username = None
    password = None
    name = None
    if request.form.keys():
        for key in request.form.keys():
            if key == 'username':
                username = request.form['username']
            if key == 'password':
                password = request.form['password']
            if key == 'name':
                name = request.form['name']
                
    if request.data:
        objOut = json.loads(request.data)
        pprint(objOut)
        username = objOut['username']
        password = objOut['password']
        
    return username, password, name

###    BLUEPRINT
serviceAuth = Blueprint('auth', __name__, url_prefix='/auth')

@serviceAuth.route('', methods=('GET', 'POST'))
def login():
    "Auth USER"
    username, password, name = validateUsrAPass(request)
    session.clear()
    if username and password:
        user = User.get(email=username)
        if user:
            typeBucket=Bucketlist._FAILURE
            if app.bcrypt.check_password_hash(user.password, password):
                app.logger.info('Auth USER {0}'.format(username))
                session['user_id'] = user.id
                user_id = session['user_id']
                #g.user = user
                typeBucket=Bucketlist._ACCESS
                app.logger.info('LOGIN_REQUIRED login: {0}'.format(user_id))
                return jsonify(isLogged=True, name=user.name),200
            else:
                app.logger.error('USER {0} error password '.format(username))
                return jsonify(isLogged=False,name=user.name),203
            
            buck = Bucketlist(user_id=user.id, type=typeBucket)
            buck.save()
        else:
            app.logger.error('USER {0} Unauthorite'.format(username))
            return('',204)
    else:
        app.logger.error('Missing arguments')
        return ('',401)

@serviceAuth.route('/register', methods=('GET', 'POST'))
def register():
    username, password, name = validateUsrAPass(request)
    session.clear()
    if username and password:
        newUser = User(email=username,password=password)
        if name:
            newUser.name = name
        result = newUser.save()
        message = get_flashed_messages()
        if newUser:
            session['user_id'] = newUser.id
            buck = Bucketlist(user_id=newUser.id, type=Bucketlist._CREATED)
            buck.save()
            return jsonify(result=result,user_id=session['user_id'],message=message),201
        app.logger.info('LOGIN_REQUIRED register: {0}'.format(session['user_id']))
    return '', 204

@serviceAuth.route('/bucketlist',methods=('GET','POST'))
@login_required
def bucketlist():
    if g.user:
        list = Bucketlist.get_allJSON(g.user.id)
        message = dict() 
        message['status_code'] = 200 
        message['list_bucketlist'] = list
        return jsonify(message)
    app.logger.info('No user logged in')
    return '',204
    

