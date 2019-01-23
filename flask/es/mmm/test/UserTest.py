'''
Created on 20 Jan 2019

@author: manuelmartinmartin
'''

import unittest
from unittest.case import TestCase
from pprint import pprint
from es.mmm.service.MainApp import create_app
from es.mmm.test.UtilsTests import randomEmail, randomPassword

class AuthTestCase(TestCase):
    
    app = None
    client = None
    user_data = None
    _type_equality_funcs = {}
    
    def __init__(self,deleteTables=False, username=None, password=None):
        self.app = create_app()
        self.client = self.app.test_client()
        
        if username is None:
            username = randomEmail()
            password = randomPassword()
            
        self.user_data = dict(
            username=username,
            password=password
        )
        
        if(deleteTables):
            with self.app.app_context():
                from es.mmm.service.ddbb.SQLAlchemy import Base, db_session, engine
                db_session.close()
                Base.metadata.drop_all(engine)
                Base.metadata.create_all(engine)
    
    def test_registration(self):
        self.app.logger.info('test_registration {0}'.format(self.user_data['username']))
        res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        
    def test_already_registered_user(self):
        self.app.logger.info('test_already_registered_user {0}'.format(self.user_data['username']))
        res = self.client.post('/auth/register', data=self.user_data)
        outJson = res.get_json()
        self.assertEqual(res.status_code, 201)
        self.assertFalse(outJson['result'])
        
    def test_log_in(self):
        self.app.logger.info('test_log_in {0}'.format(self.user_data['username']))
        res1 = self.client.post('/auth', data=self.user_data,follow_redirects=True)
        self.assertEqual(res1.status_code, 200)
        
    def test_bucketlist(self):
        self.app.logger.info('test_bucketlist {0}'.format(self.user_data['username']))
        res2 = self.client.post('/auth/bucketlist',follow_redirects=True)
        self.assertEqual(res2.status_code, 200)
        self.assertIsNotNone(res2.data)
        
    def getResult(self):
        return self._type_equality_funcs
        
        

        