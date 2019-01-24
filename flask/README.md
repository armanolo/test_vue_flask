###	SERVER FLASK

### RUN SERVER
python3 test_wsgi.py

### TEST CLIENT
python3 ./es/mmm/test/AuthTest.py 

	# 4 parameters:
	
		1.	Integer (1 or 0) => clean database or no
		2.	Integer (1:4)	OPTIONS below:
			#1. OPTION: LOGIN USER
			#2. OPTION: TEST USER IS CREATED
			#3. OPTION: REGISTER USER
			#4. OPTION: LOGIN USER AND BUCKETLIST
		3.	String (email)
		4.	String (password)
		5.	String (name)
		
	#Example to register a new user
	python3 ./es/mmm/test/AuthTest.py 0 3 'armanolo@hotmail.com' 'passmanolo' 'Manolo'  

