from flask import Flask, jsonify, Response, request
import pymongo
from pymongo import MongoClient
import json
import uuid
import time
import datetime
#from bson.json_util import dumps
from cerberus import Validator
from bson.objectid import ObjectId
import re


app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client['DigitalNotes']
users = db['users']
notes = db['notes']

users_sessions = {}


"""
Service Support functions
"""

#Create session
def create_session(username):
    session_id = str(uuid.uuid1())
    users_sessions[session_id] = (username, time.time())
    return session_id  

#Check if session is valid 
def is_session_valid(session_id):
    return session_id in users_sessions

#Get Users email/username depending on session_id
def getUser(session_id):
	return users_sessions[session_id][0]

#Check if email is valid
def emailCheck(email):
	emailRegex = '^[a-z0-9]+[\._]?[a-zA-Za-Z0-9]+[@]\w+[.]\w{2,3}$'
	return re.search(emailRegex,email)

#Check if user is already logged in
def checkLoggedIn(user):
	for key in users_sessions:
		if user in users_sessions[key]:
			return True
		return False

#Check if user is Admin
def isAdmin(user):
	searchUser = users.find_one({"email":user})
	if searchUser['category']=='admin':
		return True
	else:
		return False

"""
Application
""" 
@app.route('/')
def ping_server():
	return "Hi DigitalNotes"


"""
-> Endpoints for:

User Registration and authentication
"""
#Registration
@app.route('/register', methods=['POST'])
def userRegistration():
	#Required JSON Schema for user registration
	schema = {
		'email' : {'required':True, 'type':'string'},
		'firstName' : {'required':True, 'type':'string'},
		'surName' : {'required':True, 'type':'string'},
		'password' : {'required':True, 'type':'string'}
		}
	val = Validator(schema)
	data = None

	try:
		data = json.loads(request.data)
	except Exception as e:
		return Response("bad json content", status=500, mimetype="application/json")

	if data == None: 
		return Response("bad json content", status=500, mimetype="application/json")

	if not val.validate(data):
		return Response("Data not matching required schema. Please check the documentation.", status=500, mimetype="application/json")

	#Check if users Exists
	searchUser = users.find_one({"email":data["email"]})

	if val.validate(data) and searchUser == None :

		if not emailCheck(data["email"]):
			return Response ("Email is not valid. Please retry registering with a valid email address.", status=200,mimetype="application/json")
		newUser = {
			"email":data["email"],
			"firstName":data["firstName"],
			"surName":data["surName"],
			"password":data["password"],
			"category":"simpleUser"
			}
		users.insert_one(newUser)
		return Response ("user was added successfuly", status=200,mimetype="application/json")
	else:
		return Response ("user already exists", status=500,mimetype="application/json")

#Login
@app.route('/login', methods=['POST'])
def userLogin():
	#Required JSON Schema for user login
	schema = {
		'email' : {'required':True, 'type':'string'},
		'password' : {'required':True, 'type':'string'}
		}
	val = Validator(schema)
	data = None

	try:
		data = json.loads(request.data)
	except Exception as e:
		return Response("bad json content", status=500, mimetype="application/json")

	if data == None: 
		return Response("bad json content", status=500, mimetype="application/json")

	if not val.validate(data):
		return Response("Data not matching required schema. Please check the documentation.", status=500, mimetype="application/json")

	#Try to bring user details from db
	searchUser = users.find_one({"email":data["email"]})

	if val.validate(data) and searchUser != None :
		if searchUser["password"]==data["password"]:
			if checkLoggedIn(searchUser['email']):
				return Response("You are already logged in",status=200, mimetype='application/json')	
			user_uuid = create_session(data["email"])
			res = {
				"uuid": user_uuid,
				"username": data['email'],
				"users sessions":users_sessions,
				"userfromSession":users_sessions[user_uuid][0]
				}

			#NA DW TO CASE firstLogin=0 kai na min exei kanei pass reset
			#Check Admin first login
			if searchUser["category"]=="admin" and searchUser['firstLogin'] == 1 and searchUser['passwordReset']== 0:
				res = {
					"uuid": user_uuid,
					"username": data['email'],
					"users sessions":users_sessions,
					"userfromSession":users_sessions[user_uuid][0],
					"message": "Successful login. Please reset your password by following the endpoints ..url../passwordReset"}
				searchUser = users.update_one({'email':data['email']},
				{"$set":
					{
						"firstLogin":0
					}
				})
				return Response(json.dumps(res),status=200, mimetype='application/json')

			return Response(json.dumps(res),status=200, mimetype='application/json')			
		else:
			return Response ("Wrong Password", status=400,mimetype="application/json")
	else:
		return Response ("User is not registered", status=400,mimetype="application/json")


#TO DO: LOGOUT
#Logout
@app.route('/logout', methods=['GET'])
def logout():
	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=401, mimetype="application/json")

	if not is_session_valid(session_id):
		#return Response("No active session. Please login", status=500, mimetype="application/json")
		return Response("You can't logout if you are not logged in...https://bit.ly/3bD9zmQ", status=400, mimetype="application/json")

	tmpUser = getUser(session_id)
	isLoggedIn= checkLoggedIn(tmpUser)
	
	if isLoggedIn: 
		del users_sessions[session_id]
		return Response("Logout completed. Hope to see you back soon! :)", status=200, mimetype="application/json")

#Delete Account
@app.route('/deleteAccount', methods=['GET'])
def deleteAccount():

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")

	tmpUser = getUser(session_id)

	if isAdmin(tmpUser):
		return Response("This service is available only for simple users.", status=500, mimetype="application/json")

	query={"email":tmpUser}
	searchUser = users.find(query)

	if searchUser == None:
		return Response("Not such user found", status=500, mimetype="application/json")

	if searchUser != None:
		users.delete_one(query)
		notes.delete_many({'owner':tmpUser})
		return Response("Your account and all the data has been deleted.", status=200, mimetype="application/json")


"""
-> Endpoints for:

Notes management
"""
#Add Note
@app.route('/notes/add', methods=['POST'])
def addNote():
	#Required JSON Schema for new note
	schema = {
		'title' : {'required':True, 'type':'string'},
		'content' : {'required':True, 'type':'string'},
		'tags' : {'required':True, 'type':'string'},
		}
	val = Validator(schema)
	data = None
		
	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("You are not authorized to perform this action. Please try to login first.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")

	tmpUser = getUser(session_id) #Get User's email/username
	if isAdmin(tmpUser):
		return Response("This service is available only for simple users.", status=500, mimetype="application/json")

	try:
		data = json.loads(request.data)
	except Exception as e:
		return Response("bad json content", status=500, mimetype="application/json")

	if data == None: 
		return Response("bad json content", status=500, mimetype="application/json")

	if not val.validate(data):
		return Response("Data not matching required schema. Please check the documentation.", status=500, mimetype="application/json")
	
	if val.validate(data):
		tags = data["tags"].split(',') #Split comma seperated tags and add to list
		newNote = {
			"title":data["title"],
			"content":data["content"],
			"tags":tags,
			"createdDt":datetime.datetime.now(),
			"owner":tmpUser
			}
		notes.insert_one(newNote)
		return Response ("Note added successfully", status=200,mimetype="application/json")

#Search Note by Title
@app.route('/notes/search/<string:title>', methods=['GET'])
def searchNoteTitle(title):

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("You are not authorized to perform this action. Please try to login first.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")

	tmpUser = getUser(session_id) #Get User's email/username
	if isAdmin(tmpUser):
		return Response("This service is available only for simple users.", status=500, mimetype="application/json")

	if title == None:
		return Response("bad json content", status=500, mimetype="application/json")

	tmpUser = getUser(session_id)
	searchNote = notes.find({"title":title, "owner":tmpUser})

	if searchNote == None:
		return Response("Note with title " +title+ " not found", status=500, mimetype="application/json")

	if searchNote !=None:
		searchNote = [
			{"_id":str(y["_id"]), 'title':y["title"],'content':y["content"], 'tags':y["tags"]} for y in searchNote]
		#return jsonify(searchNote)
		return Response(json.dumps(searchNote),status=200,mimetype='application/json')

#Search Note by Tag
@app.route('/notes/searchByTag/<string:tag>', methods=['GET'])
def searchNoteTag(tag):

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("You are not authorized to perform this action. Please try to login first.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")
	
	tmpUser = getUser(session_id) #Get User's email/username
	if isAdmin(tmpUser):
		return Response("This service is available only for simple users.", status=500, mimetype="application/json")

	if tag == None:
		return Response("bad json content", status=500, mimetype="application/json")

	tmpUser = getUser(session_id)
	searchNote = notes.find({"tags":tag, "owner":tmpUser}).sort([("createdDt", pymongo.DESCENDING)])

	if searchNote == None:
		return Response("Note with tag " +tag+ " not found", status=500, mimetype="application/json")

	if searchNote !=None:
		searchTag = [{'title':y["title"],'content':y["content"], 'tags':y["tags"], "createdDt":y['createdDt']} for y in searchNote]
		#return jsonify(searchNote)
		return (jsonify(searchTag))
		return Response(json.dumps(searchTag),status=200,mimetype='application/json')
	
#Update Note by ID
@app.route('/notes/update/<string:id>', methods=['PATCH'])
def updateNote(id):
	#Required JSON Schema for note update
	schema = {
	'title' : {'required':False, 'type':'string'},
	'content' : {'required':False, 'type':'string'},
	'tags' : {'required':False, 'type':'string'},
	}

	val = Validator(schema)
	data = None
	session_id = request.headers.get('Authorization')

	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	session_id = request.headers.get('Authorization')

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")
	
	tmpUser = getUser(session_id) #Get User's email/username
	if isAdmin(tmpUser):
		return Response("This service is available only for simple users.", status=500, mimetype="application/json")

	if id == None or len(id)!=24:
		return Response("Pass valid note ID", status=500, mimetype="application/json")

	query={"_id":ObjectId(id)}
	updateNote = notes.find_one(query)

	if updateNote != None:
		try:
			data = json.loads(request.data)
		except Exception as e:
			return Response("bad json content", status=500, mimetype="application/json")

		if data == None: 
			return Response("bad json content", status=500, mimetype="application/json")

		if not val.validate(data):
			return Response("Data not matching required schema. Please check the documentation.", status=500, mimetype="application/json")

		if val.validate(data):

			key1 = 'title'
			key2 = 'content'
			key3 = 'tags'

			updateQuery = {"_id":ObjectId(id)}
			
			if key1 in data:
				notes.update_one(updateQuery,
				{"$set":
					{
						"title":data[key1]
					}
				})

			if key2 in data:
				notes.update_one(updateQuery,
				{"$set":
					{
						"content":data[key2]
					}
				})

			if key3 in data:
				notes.update_one(updateQuery,
				{"$set":
					{
						"tags":data[key3].split(',')
					}
				})

			updateNote = notes.find_one({"title":key1})
			return Response ("Note updated successfully.", status=200,mimetype="application/json")
		return Response ("Schema not valid", status=200,mimetype="application/json")
	else:
		return Response("Note does not exist. System couldn't proceed with update. ", status=500, mimetype="application/json")

#Delete Note by ID
@app.route('/notes/delete/<string:id>', methods=['DELETE'])
def deleteNote(id):

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")
	
	tmpUser = getUser(session_id) #Get User's email/username
	if isAdmin(tmpUser):
		return Response("This service is available only for simple users.", status=500, mimetype="application/json")
	
	if id == None or len(id)!=24:
		return Response("Pass valid note ID.", status=500, mimetype="application/json")

	query={"_id":ObjectId(id)}
	searchNote = notes.find_one(query)

	if searchNote !=None:	
		notes.delete_one(query)
		return Response ("Note deleted", status=200,mimetype="application/json")
	else :
		return Response("Not not found", status=500, mimetype="application/json")

#Get All Notes
@app.route('/getnotes/<string:sortType>', methods=['GET'])
def getNotes(sortType):

	if sortType!='desc' and sortType!='asc':
		return Response("Sorting option not valid. Please check documentation and try again", status=500, mimetype="application/json")

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")

	tmpUser = getUser(session_id)
	if isAdmin(tmpUser):
		return Response("This service is available only for simple users.", status=500, mimetype="application/json")

	if sortType=='desc':
		cursor = db.notes.find({"owner":tmpUser}).sort([("createdDt", pymongo.DESCENDING)])
	
	if sortType=='asc':
		cursor = db.notes.find({"owner":tmpUser}).sort([("createdDt", pymongo.ASCENDING)])

	notes = [{"title":y['title'],"content":y['content'], "tags":y['tags'], "createdDt":y['createdDt'], "_id":str(y["_id"])} for y in cursor]
	return jsonify(notes)

	
"""
-> Endpoints for:

Admin & Password Reset
"""

#Add Admin
@app.route('/addAdmin', methods=['POST'])
def addAdmin():
	#Required JSON Schema for new admin
	schema = {
		'email' : {'required':True, 'type':'string'},
		'firstName' : {'required':True, 'type':'string'},
		'surName' : {'required':True, 'type':'string'},
		}
	val = Validator(schema)
	data = None

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")

	tmpAdmin = getUser(session_id)
		
	if not isAdmin(tmpAdmin):
		return Response("This service is available only for admins.", status=500, mimetype="application/json")

	try:
		data = json.loads(request.data)
	except Exception as e:
		return Response("bad json content", status=500, mimetype="application/json")

	if data == None: 
		return Response("bad json content", status=500, mimetype="application/json")

	if not val.validate(data):
		return Response("Data not matching required schema. Please check the documentation.", status=500, mimetype="application/json")

	#Check if users Exists
	searchAdmin = db.users.find_one({"email":data["email"]})

	if val.validate(data) and searchAdmin == None :
		if not emailCheck(data["email"]):
			return Response ("Email is not valid. Please retry registering with a valid email address.", status=200,mimetype="application/json")

		newAdmin = {"email":data["email"], "firstName":data["firstName"], "surName":data["surName"], "password":"1234", "category":"admin", "firstLogin":1, "passwordReset":0}
		db.users.insert_one(newAdmin)
		return Response ("Admin was added successfuly", status=200,mimetype="application/json")
	else:
		return Response ("Admin already exists", status=500,mimetype="application/json")

#Password Reset
@app.route('/passwordReset', methods=['PUT'])
def passReset():
	#Required JSON Schema for password reset
	schema = {
		'oldPass' : {'required':True, 'type':'string'},
		'newPass' : {'required':True, 'type':'string'},
		'confirmPass' : {'required':True, 'type':'string'}
		}
	val = Validator(schema)
	data = None

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")

	tmpUser = getUser(session_id)
	searchUser = users.find_one({'email':tmpUser})

	try:
		data = json.loads(request.data)
	except Exception as e:
		return Response("bad json content", status=500, mimetype="application/json")

	if data == None: 
		return Response("bad json content", status=500, mimetype="application/json")

	if not val.validate(data):
		return Response("Data not matching required schema. Please check the documentation.", status=500, mimetype="application/json")

	if val.validate(data):
		#check if old pass is matching existing
		if data['oldPass']==searchUser['password']:
			#check if pass and confirm pass matches
			if data['newPass']== data['confirmPass']:
				# check if new pass is different than old one & update pass
				if data['newPass'] != data['oldPass']:
					users.update_one({'email':tmpUser},
							{"$set":
								{
									"password":data['newPass']
								}
							})
					#check if is first pw reset for admin
					if searchUser['category']=="admin" and searchUser['passwordReset'] == 0:
						searchUser = users.update_one({'email':tmpUser},
							{"$set":
								{
									"passwordReset": 1
								}
							})
						#auto logout after password reset
						del users_sessions[session_id]
						return ("Password updated successfully. Please re-login.")
					#auto logout after password reset						
					del users_sessions[session_id]
					return ("Password updated successfully. Please re-login.")
				else: 
					return ("New password can't be the same with old one.")
			else : 
				return ("New password does not match password confirmation.")
		else : 
			return ("Given 'Current Password' does not match your password.")
	else :
		return ("Data not matching required schema. Please check the documentation.")

#Admin Delete User
@app.route('/deleteUser/<string:email>', methods=['DELETE'])
def deleteUser(email):
	deleteUser = email

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	if not is_session_valid(session_id):
		return Response("No active session. Please login", status=500, mimetype="application/json")

	tmpAdmin = getUser(session_id)
		
	if not isAdmin(tmpAdmin):
		return Response("This service is available only for admins.", status=400, mimetype="application/json")

	#Check if users Exists
	searchUser = db.users.find_one({"email":deleteUser})

	if searchUser != None:
		users.delete_one({"email":deleteUser})
		return Response ("User deleted", status=200,mimetype="application/json")
	else:
		return Response ("No user found", status=400,mimetype="application/json")


"""
Application
"""
if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)

