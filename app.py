from flask import Flask, jsonify, Response, request
import pymongo
from pymongo import MongoClient
import json
import uuid
import time
import datetime
from bson.json_util import dumps
from cerberus import Validator



app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')
db = client['DigitalNotes']
users = db['users']
notes = db['notes']
test = "test"


users_sessions = {}

def create_session(username):
    session_id = str(uuid.uuid1())
    users_sessions[session_id] = (username, time.time())
    return session_id  

def is_session_valid(session_id):
    return session_id in users_sessions

#Home 
@app.route('/')
def ping_server():
	return "Hi DigitalNotes"

####USER AUTH AND REGISTRATION

#Registration
@app.route('/register', methods=['POST'])
def userRegistration():
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
		newUser = {"email":data["email"], "firstName":data["firstName"], "surName":data["surName"], "password":data["password"], "category":"simpleUser"}
		users.insert_one(newUser)
		return Response ("user was added successfuly", status=200,mimetype="application/json")
	else:
		return Response ("user already exists", status=500,mimetype="application/json")

#Login
@app.route('/login', methods=['POST'])
def userLogin():
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

	#Check details
	searchUser = users.find_one({"email":data["email"]})

	if val.validate(data) and searchUser != None :
		if searchUser["password"]==data["password"]:

			user_uuid = create_session(data["email"])
			#res = {"uuid": user_uuid, "username": data['email']}
			res = {"uuid": user_uuid, "username": data['email'], "users sessions":users_sessions, "userfromSession":users_sessions[user_uuid][0]}
			return Response(json.dumps(res),status=200, mimetype='application/json')

			# return Response ("Login Successful", status=200,mimetype="application/json")
		else:
			return Response ("Wrong Password", status=500,mimetype="application/json")
	else:
		return Response ("User is not registered", status=500,mimetype="application/json")

####Notes Management

#Add Note
@app.route('/notes/add', methods=['POST'])
def addNote():
	schema = {
		'title' : {'required':True, 'type':'string'},
		'content' : {'required':True, 'type':'string'},
		'tags' : {'required':True, 'type':'string'},
		}
	val = Validator(schema)
	data = None
	
	
	session_id = request.headers.get('Test')
	if session_id == None:
		return Response("You are not authorized to perform this action. Please try to login first.", status=500, mimetype="application/json")

	#Json Contents
	try:
		data = json.loads(request.data)
	except Exception as e:
		return Response("bad json content", status=500, mimetype="application/json")

	if data == None: 
		return Response("bad json content", status=500, mimetype="application/json")

	if not val.validate(data):
		return Response("Data not matching required schema. Please check the documentation.", status=500, mimetype="application/json")


	
	if val.validate(data):
		tags = data["tags"].split(',')
		#newNote = {"title":data["title"], "content":data["content"], "tags":tags, "createdDt":datetime.datetime.now(), "owner":users_sessions[user_id][0]}
		newNote = {"title":data["title"], "content":data["content"], "tags":tags, "createdDt":datetime.datetime.now()}
		notes.insert_one(newNote)
		return Response ("test", status=200,mimetype="application/json")


#Search Note by Title
# @app.route('/notes/search/<string:title>', methods=['GET'])
# def searchNoteTitle(title):

# 	session_id = request.headers.get('Authorization')
# 	if session_id == None:
# 		return Response("You are not authorized to perform this action. Please try to login first.", status=500, mimetype="application/json")

# 	if title == None:
# 		return Response("bad json content", status=500, mimetype="application/json")

# 	searchNote = notes.find_one({"title":title})

# 	if searchNote == None:
# 		return Response("Note with title " +title+ " not found", status=500, mimetype="application/json")

# 	if searchNote !=None:
# 		searchNote = {'title':searchNote["title"],'content':searchNote["content"], 'tags':searchNote["tags"]}
# 		#return jsonify(searchNote)
# 		return Response(json.dumps(searchNote),status=200,mimetype='application/json')

#Search Note by Title
@app.route('/searchnote/<string:title>', methods=['GET'])
def searchNoteTitle(title):

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("You are not authorized to perform this action. Please try to login first.", status=500, mimetype="application/json")

	if title == None:
		return Response("bad json content", status=500, mimetype="application/json")

	searchNote = notes.find({"title":title})

	if searchNote == None:
		return Response("Note with title " +title+ " not found", status=500, mimetype="application/json")

	if searchNote !=None:
		searchNote = [{'title':y["title"],'content':y["content"], 'tags':y["tags"]} for y in searchNote]
		#return jsonify(searchNote)
		return Response(json.dumps(searchNote),status=200,mimetype='application/json')

#Search Note by  Tag
@app.route('/notes/searchtag/<string:tag>', methods=['GET'])
def searchNoteTag(tag):
	
	if tag == None:
		return Response("bad json content", status=500, mimetype="application/json")

	searchNote = notes.find({"tags":tag})

	if searchNote == None:
		return Response("Note a single with tag " +tag+ " not found", status=500, mimetype="application/json")

	if searchNote !=None:
		searchTag = [{'title':y["title"],'content':y["content"], 'tags':y["tags"]} for y in searchNote]
		#return jsonify(searchNote)
		return Response(json.dumps(searchTag),status=200,mimetype='application/json')
	
#Update Note
@app.route('/notes/update/<string:title>', methods=['PATCH'])
def updateNote(title):

	schema = {
	'_id': {'required':True, 'type':'string'},
	'title' : {'required':False, 'type':'string'},
	'content' : {'required':False, 'type':'string'},
	'tags' : {'required':False, 'type':'string'},
	}

	val = Validator(schema)
	data = None
	session_id = request.headers.get('Authorization')

	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")

	if title == None:
		return Response("bad json content", status=500, mimetype="application/json")

	query={"title":title}
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
			#update = {"title":data["title"], "content":data["content"], "tags":data["tags"], "createdDt":datetime.datetime.now(), "owner":users_sessions[user_id][0]}

			# newTitle = data["title"]
			# newContent = data["content"] 
			# newTags = data["tags"]  
			id = updateNote["_id"]
			key1 = 'title'
			key2 = 'content'
			key3 = 'tags'

			updateQuery = {"_id":data['_id']}
			#NA KANW UPDATE ME OBJECT ID
			
			if key1 in data:
				notes.update_one({'title':data['title']},
				{"$set":
					{
						"title":data[key1]
					}
				})

			if key2 in data:
				notes.update_one({'_id':data['_id']},
				{"$set":
					{
						"content":data[key2]
					}
				})

			if key3 in data:
				notes.update_one({'_id':data['_id']},
				{"$set":
					{
						"tags":data[key3].split(',')
					}
				})

			# updateNote = notes.update_one(query,{
			# 	"$set":
			# 	{
			# 		"title":data["title"],
			# 		"content":data["content"],
			# 		"tags":data["tags"]
			# 	}
			# })

			updateNote = notes.find_one({"title":key1})
			#updateNote = {"title":updateNote["title"], "content":updateNote["content"], "tags":updateNote["tags"], "update message":"note updated successfully"}
			#return jsonify(updateNote)
			return ("SUCCESS")
		return Response ("test", status=200,mimetype="application/json")

	else:
		return Response("Note not found. We couldn't proceed with update. ", status=500, mimetype="application/json")


	
	if val.validate(data):
		tags = data["tags"].split(',')
		#newNote = {"title":data["title"], "content":data["content"], "tags":tags, "createdDt":datetime.datetime.now(), "owner":users_sessions[user_id][0]}
		newNote = {"title":data["title"], "content":data["content"], "tags":tags, "createdDt":datetime.datetime.now()}
		notes.insert_one(newNote)
		return Response ("test", status=200,mimetype="application/json")



#Delete Note
@app.route('/notes/delete/<string:title>', methods=['DELETE'])
def deleteNote(title):

	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")
	
	if title == None:
		return Response("bad json content", status=500, mimetype="application/json")

	query={"title":title}
	searchNote = notes.find_one(query)

	if searchNote == None:
		return Response("Not with title " +title+ " not found", status=500, mimetype="application/json")

	if searchNote !=None:	
		notes.delete_one(query)
		return Response ("Note deleted", status=200,mimetype="application/json")


#Delete Account
@app.route('/deleteAccount/<string:username>', methods=['GET'])
def deleteUser(username):


	session_id = request.headers.get('Authorization')
	if session_id == None:
		return Response("Authorization key is missing. Please pass session_id in Authorization header.", status=500, mimetype="application/json")


	if username == None:
		return Response("bad json content", status=500, mimetype="application/json")

	query={"email":username}
	searchUser = users.find(query)

	if searchUser == None:
		return Response("Not such user found", status=500, mimetype="application/json")

	if searchUser != None and searchUser['email']==username:
		users.delete_one(query)
		notes.delete_many({'owner':username})
		return Response("Your account and all the data has been deleted.", status=200, mimetype="application/json")









#Get All Notes
@app.route('/getnotes/', methods=['GET'])
def getNotes():
	cursor = db.notes.find().sort([("createdDt", pymongo.DESCENDING)])
	users = [{"title":y['title'],"content":y['content'], "tags":y['tags'], "createdDt":y['createdDt'], "_id":str(y["_id"])} for y in cursor]
	return jsonify(users)


#Add New Note
# @app.route('/addNote', methods=['POST'])
# def newNote():
# 	data = None
# 	try:
# 		data = json.loads(request.data)
# 	except Exception as e:
# 		return Response("bad json content", status=500, mimetype="application/json")
# 	if data == None: 
# 		return Response("bad json content", status=500, mimetype="application/json")
# 	if not "title" in data or not "note" in data:
# 		return Response("incomplete data", status=500, mimetype="application/json")
# 	else:
# 		newNote = {"title":data["title"], "note":data["note"]}
# 		notes.insert_one(newNote)
# 		return Response ("note was added successfuly", status=200,mimetype="application/json")




if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)

