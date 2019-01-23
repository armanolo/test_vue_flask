'''
Created on 17 Jan 2019

@author: manuelmartinmartin
'''
import sys
import os
pathRoot = os.path.abspath(os.curdir)
sys.path.append(pathRoot)

from es.mmm.test.UserTest import AuthTestCase

clean = False
username = None
password = None
option = 0
nameUser = None

#OPTION 1 = CLEAN OR NOT DATABASE   :  sys.argv[1]
#OPTION 2 = OPTIONS                 :  sys.argv[2]
#OPTION 3 = USERNAME                :  sys.argv[3]
#OPTION 4 = PASSOWRD                :  sys.argv[4]
#OPTION 5 = NAME                    :  sys.argv[5]

if len(sys.argv) > 1:
    try:
        clean = bool(int(sys.argv[1]))
    except ValueError as error:
        print(type(sys.argv[1]))
    if len(sys.argv) > 2:
        option = int(sys.argv[2])
    if len(sys.argv) > 3:
        username = sys.argv[3]
        password = sys.argv[4]
    if len(sys.argv) > 5:
        nameUser = sys.argv[5]
     
uni =None    
if username:
    uni = AuthTestCase(clean,username,password)
    if nameUser:
        uni.user_data['name'] = nameUser
else:
    uni = AuthTestCase(clean)
    

print('OPTIONS: {0}:{1}:{2}:{3}'.format(clean,option,username,password))    
if option == 1:
    print('LOGIN USER: {0} {1}'.format(username,password))
    uni.test_log_in()
elif option == 2:
    print('TEST USER IS CREATED: {0} {1}'.format(username,password))
    uni.test_already_registered_user()
elif option == 3:
    print('REGISTER USER: {0} {1}'.format(username,password))
    uni.test_registration()
elif option == 4:
    print('LOGIN USER AND BUCKETLIST: {0} {1}'.format(username,password))
    uni.test_log_in()
    uni.test_bucketlist()
else:
    print('1. OPTION: LOGIN USER')
    print('2. OPTION: TEST USER IS CREATED')
    print('3. OPTION: REGISTER USER')
    print('4. OPTION: LOGIN USER AND BUCKETLIST')
    
print('ALL OK')