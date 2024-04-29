#!/usr/bin/env python3

import datetime
import json


##
## Initialization of the CouchDB server (creation of 1 collection of
## documents named "ehr", if it is not already existing)
##

import CouchDBClient

client = CouchDBClient.CouchDBClient()

# client.reset()   # If you want to clear the entire content of CouchDB

if not 'ehr' in client.listDatabases():
    client.createDatabase('ehr')


##
## Optional: You can install CouchDB views at this point (this is not
## mandatory, but using views will vastly improve performance)
##

# TODO -> OK? , from solution
# Install same views as for the client
client.installView('ehr', 'temperatures', 'by_patient_id', '''
function(doc) {
if (doc.type == 'temperature') {
    emit(doc.patient_id, doc);
  }
}
''')
client.installView('ehr', 'patients', 'by_patient_name', '''
function(doc) {
  if (doc.type == 'patient') {
    emit(doc.name, doc);
  }
}
''')



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


##
## REST API to be implemented by the students
##
    
@app.route('/create-patient', methods = [ 'POST' ])
def create_patient():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())

    patientId = None

    # TODO -> OK?
    doc = {
        'type' : 'patient',
        'name' : body['name']
    }
    patientId = client.addDocument('ehr',doc) # New patient document (vs. new EHR for EHRBase)
    

    return Response(json.dumps({
        'id' : patientId
    }), mimetype = 'application/json')
        

@app.route('/record', methods = [ 'POST' ])
def record_temperature():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())

    now = datetime.datetime.now().isoformat()  # Get current time

    # TODO -> OK?
    doc = {
        'type' : 'temperature',
        'patient_id' : body['id'],
        'temperature' : body['temperature'],
        'time' : now
    }
    client.addDocument('ehr',doc)

    return Response('', 204)


@app.route('/patients', methods = [ 'GET' ])
def list_patients():
    result = []

    # TODO -> Vérif si ça marche
    results = client.executeView('ehr', 'patients', 'by_patient_name')
    result = list(map(lambda x : {
        'id' : x['value']['_id'],
        'name' : x['value']['name']

    },results))
    

    return Response(json.dumps(result), mimetype = 'application/json')
        

@app.route('/temperatures', methods = [ 'GET' ])
def list_temperatures():
    patientId = request.args.get('id')

    result = []
    # TODO -> Vérif si ça marche
    results = client.executeView('ehr', 'temperatures', 'by_id', patientId)
    result = list(map(lambda x : {
        'id' : x['value']['time'],
        'name' : x['value']['temperature']

    },results))
    
    

    return Response(json.dumps(result), mimetype = 'application/json')

if __name__ == '__main__':
    app.run()
