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
			return Response ("Login Successful", status=200,mimetype="application/json")
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
		newNote = {"title":data["title"], "content":data["content"], "tags":tags, "createdDt":datetime.datetime.now()}
		notes.insert_one(newNote)
		return Response ("Note created", status=200,mimetype="application/json")


#Search Note by Title
@app.route('/notes/search/<string:title>', methods=['GET'])
def searchNoteTitle(title):
	if title == None:
		return Response("bad json content", status=500, mimetype="application/json")

	searchNote = notes.find_one({"title":title})

	if searchNote == None:
		return Response("Note with title " +title+ " not found", status=500, mimetype="application/json")

	if searchNote !=None:
		searchNote = {'title':searchNote["title"],'content':searchNote["content"], 'tags':searchNote["tags"]}
		#return jsonify(searchNote)
		return Response(json.dumps(searchNote),status=200,mimetype='application/json')

#Search Note by Title
# @app.route('/searchnote/<string:title>', methods=['GET'])
# def searchNoteTitle(title):
# 	if title == None:
# 		return Response("bad json content", status=500, mimetype="application/json")

# 	searchNote = notes.find({"title":title})

# 	if searchNote == None:
# 		return Response("Note with title " +title+ " not found", status=500, mimetype="application/json")

# 	if searchNote !=None:
# 		searchNote = [{'title':y["title"],'content':y["content"], 'tags':y["tags"]} for y in searchNote]
# 		#return jsonify(searchNote)
# 		return Response(json.dumps(searchNote),status=200,mimetype='application/json')

#Update Note
@app.route('/notes/update/', methods=['PUT'])
def updateNote(title):
	if title == None:
		return Response("bad json content", status=500, mimetype="application/json")

	searchNote = notes.find_one({"title":title})

	if searchNote == None:
		return Response("Note with title " +title+ " not found", status=500, mimetype="application/json")

	if searchNote !=None:
		searchNote = {'title':searchNote["title"],'content':searchNote["content"], 'tags':searchNote["tags"]}
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
	











#Get All Notes
@app.route('/getnotes/', methods=['GET'])
def getNotes():
	cursor = db.notes.find()
	users = [{"title":y['title'],"content":y['content'], "tags":y['tags']} for y in cursor]
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

