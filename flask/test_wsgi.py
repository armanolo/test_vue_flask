'''
Created on Jan 4, 2019

@author: manolo
'''
from es.mmm.service.MainApp import create_app

if __name__ == '__main__':
    app = create_app()
    hostTest = app.config['HOST']#'0.0.0.0'
    portTest = app.config['PORT']#'5000'
    debugTest = app.config['DEBUG']#True
    load_dotenvTest =True
    print ('RUNNING SERVER')
    app.run(hostTest, portTest, debugTest,load_dotenvTest)

