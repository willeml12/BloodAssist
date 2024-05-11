#!/usr/bin/env python3

import json
import datetime

setbloodbank = True

##
## Initialization of the CouchDB server (creation of a collection of
## documents named "blood_db" for blood banks and "users_db" for the listed blood givers, if not already existing)
##
import CouchDBClient as CouchDBClient

client = CouchDBClient.CouchDBClient()

# client.reset()   # If you want to clear the entire content of CouchDB

if not 'blood_db' in client.listDatabases():
    print("notexist")
    client.createDatabase('blood_db')
if not 'users_db' in client.listDatabases():
    client.createDatabase('users_db')
    if setbloodbank :
        client.addDocument('blood_db', {'type' : 'O-', 'stock' : '670 liters', 'criticalstock' : '1000 liters'})
        client.addDocument('blood_db', {'type' : 'O+', 'stock' : '1035 liters', 'criticalstock' : '1000 liters'})
        client.addDocument('blood_db', {'type' : 'A-', 'stock' : '1123 liters', 'criticalstock' : '1000 liters'})
        client.addDocument('blood_db', {'type' : 'A+', 'stock' : '1352 liters', 'criticalstock' : '1000 liters'})
        client.addDocument('blood_db', {'type' : 'B-', 'stock' : '1236 liters', 'criticalstock' : '1000 liters'})
        client.addDocument('blood_db', {'type' : 'B+', 'stock' : '1567 liters', 'criticalstock' : '1000 liters'})
        client.addDocument('blood_db', {'type' : 'AB-', 'stock' : '1300 liters', 'criticalstock' : '1000 liters'})
        client.addDocument('blood_db', {'type' : 'AB+', 'stock' : '1152 liters', 'criticalstock' : '1000 liters'})

# TODO : Create views (users db by user type, blood db by blood type)

##
## Serving static HTML/JavaScript resources using Flask
##

from flask import Flask, Response, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def hello():
    return redirect(url_for('get_index'))

@app.route('/index.html', methods = [ 'GET' ])
def get_index():
    with open('index.html', 'r') as f:
        return Response(f.read(), mimetype = 'text/html')

@app.route('/app.js', methods = [ 'GET' ])
def get_javascript():
    with open('app.js', 'r') as f:
        return Response(f.read(), mimetype = 'text/javascript')


@app.route('/questions')
def questions():
    with open('questions.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')
@app.route('/eligible')
def eligible():
    with open('eligible.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')

@app.route('/ineligible')
def ineligible():
    with open('ineligible.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')
    
@app.route('/login', methods = [ 'GET' ])
def login():
    with open('login.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')


##
## REST API to be implemented by the students
##

   
@app.route('/create-patient', methods = [ 'POST' ])
def create_patient():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())


    patientId = None
    doc = {
        'type' : 'patient',
        'name' : body['name'],
        'btype' : body['btype']
    }
    patientId = client.addDocument('users_db',doc) # New patient document (vs. new EHR for EHRBase)
    print("User added. ID:", patientId)

    return Response(json.dumps({
        'id' : patientId
    }), mimetype = 'application/json')

@app.route('/register_user', methods=['POST'])
def register_user():
    print("inside")
    # Assuming the client sets "Content-Type" to "application/json"
    body = json.loads(request.get_data()) # Automatically parse JSON data
    patientId = None
    print("inside")


    # Construct the document to store in the database
    doc = {
        'type': 'user',
        'firstName': body['firstName'],
        'lastName': body['lastName'],
        'dob': body['dob'],
        'email': body['email'],
        'bloodType': body['bloodType'],
        'password': body['password']  # Consider hashing the password before storing
    }

    # Assuming you have a function to add a document to a CouchDB database
    patientId = client.addDocument('users_db', doc)
    print("User registered. ID:", patientId)

    return Response(json.dumps({'id': patientId}), mimetype='application/json')


@app.route('/input', methods = [ 'POST' ])
def blood_input():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())

    now = datetime.datetime.now().isoformat()  # Get current time

    # TODO -> OK?
    doc = {
        'type' : 'bloodIn',
        'btype' : body['btype'],
        'amount' : body['amount'],
        'date' : now
    }
    client.addDocument('blood_db',doc)

    return Response('', 204)

@app.route('/output', methods = [ 'POST' ])
def blood_output():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())

    now = datetime.datetime.now().isoformat()  # Get current time

    # TODO -> OK?
    doc = {
        'type' : 'bloodOut',
        'btype' : body['btype'],
        'amount' : body['amount'],
        'date' : now
    }
    client.addDocument('blood_db',doc)

    return Response('', 204)

# Retrieves all entries in blood_db and returns the results
@app.route('/lookup-blood-stock', methods = [ 'POST' ])
def lookup_blood_stock():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    groups = client.listDocuments('blood_db')
    stocks = []
    for group in groups :
        stock = client.getDocument('blood_db', group)
        stocks.append({'type' : stock.get('type'), 'stock' : stock.get('stock'), 'criticalstock' : stock.get('criticalstock')})
    answer = {
        'stocks' : stocks
    }
    return Response(json.dumps(answer), mimetype = 'application/json')

if __name__ == '__main__':
    app.run(debug = True)
