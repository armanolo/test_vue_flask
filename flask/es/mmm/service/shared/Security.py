'''
Created on 23 Jan 2019

@author: manuelmartinmartin
'''
from functools import wraps
from es.mmm.service.ddbb.Models import User
from flask import session, g
from flask import redirect, url_for
from pprint import pprint

def login_required(f):
    "Valid user is logged"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session.keys():
            user_id = session['user_id']
            if user_id is None:
                g.user = None
            else:
                newUser = User()
                g.user = newUser.get(user_id)
        else:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function