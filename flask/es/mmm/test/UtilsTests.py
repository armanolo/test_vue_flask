'''
Created on 18 Jan 2019

@author: manuelmartinmartin
'''
import random
import functools 
from datetime import datetime
from _datetime import timedelta
import jwt
from flask import current_app as app

def randomEmail():
    num = random.randint(5,10)
    end_mail = random.choice(['hotmail.com','gmail.com','yahoo.com','outlook.com','icloud.com'])
    cadena = []
    for v in range(0,num):
        cadena.insert(0, random.choice("abcdefghijklmnopqrstuvwxyz"))
    cadena.append('@')
    cadena.append(end_mail)
    #lis = [ 1 , 3, 5, 6, 2, ]
    #functools.reduce(lambda a,b : a+b,lis)
    return ''.join(cadena)

def randomPassword():
    num = random.randint(5,10)
    cadena = []
    for v in range(0,num):
        ifOrNo = bool(random.randint(0,1))
        option = random.choice("abcdefghijklmnopqrstuvwxyz1234567890")
        isCapt = option.upper() if ifOrNo else option.lower()
        cadena.insert(0, isCapt)
    return ''.join(cadena)

def generate_token(self, user_id):
    """ Generates the access token"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        # create the byte string token using the payload and the SECRET key
        jwt_string = jwt.encode(
            payload,
            app.config.get('SECRET'),
            algorithm='HS256'
        )
        return jwt_string

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)

def decode_token(token):
    """Decodes the access token from the Authorization header."""
    try:
        # try to decode the token using our SECRET variable
        payload = jwt.decode(token, app.config.get('SECRET'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        # the token is expired, return an error string
        return "Expired token. Please login to get a new token"
    except jwt.InvalidTokenError:
        # the token is invalid, return an error string
        return "Invalid token. Please register or login"
