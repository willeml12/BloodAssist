#!/usr/bin/env python3

import json
import datetime


##
## Initialization of the CouchDB server (creation of a collection of
## documents named "blood_db" for blood banks and "users_db" for the listed blood givers, if not already existing)
##
import CouchDBClient as CouchDBClient

client = CouchDBClient.CouchDBClient()

# client.reset()   # If you want to clear the entire content of CouchDB

if not 'blood_db' in client.listDatabases():
    client.createDatabase('blood_db')
if not 'users_db' in client.listDatabases():
    client.createDatabase('users_db')

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
    with open('server/index.html', 'r') as f:
        return Response(f.read(), mimetype = 'text/html')

@app.route('/app.js', methods = [ 'GET' ])
def get_javascript():
    with open('server/app.js', 'r') as f:
        return Response(f.read(), mimetype = 'text/javascript')


@app.route('/eligible')
def eligible():
    with open('server/eligible.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')

@app.route('/ineligible')
def ineligible():
    with open('server/ineligible.html', 'r') as f:
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

if __name__ == '__main__':
    app.run(debug = True)
