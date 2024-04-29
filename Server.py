#!/usr/bin/env python3

import json
import FHIRToolbox

FHIR_URL = 'https://hapi.fhir.org/baseR5'


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

@app.route('/lookup-patients', methods = [ 'POST' ])
def lookup_patient():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())
    
    # TODO
    if body['family'] != '' :
        if body['ehr-id'] != '' :
            cursor = FHIRToolbox.FHIRCursor(FHIR_URL + '/Patient', { # 
                'family' : body['family'],
                'identifier' : body['ehr-id'],
                }) # Instanciate search
        else :
            cursor = FHIRToolbox.FHIRCursor(FHIR_URL + '/Patient', { # 
                'family' : body['family'],
                }) # Instanciate search
    else :
        if body['ehr-id'] != '' :
            cursor = FHIRToolbox.FHIRCursor(FHIR_URL + '/Patient', { # 
                'identifier' : body['ehr-id'],
                }) # Instanciate search
        else :
            cursor = FHIRToolbox.FHIRCursor(FHIR_URL + '/Patient', {
                }) # Instanciate search
    cursor.read_next() # get first page
    entries = cursor.get_entries()
    patients = []
    for elem in entries :
        ehr = []
        for i in elem['resource'].get('identifier', []) :
            ehr.append(i.get('value'))
        patients.append({
            'ehr-ids' : ehr,
            'family' : elem['resource']['name'][0].get('family'),
            'fhir-id' : elem['resource']['id'],
            'first-name' : elem['resource']['name'][0].get('given')})
    answer = {"complete" : cursor.is_done(), 'patients' : patients}

    print(answer)

    return Response(json.dumps(answer), mimetype = 'application/json')


@app.route('/lookup-observations', methods = [ 'POST' ])
def lookup_observations():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())
    
    answer = []
    
    # TODO
    

    return Response(json.dumps(answer), mimetype = 'application/json')


if __name__ == '__main__':
    app.run(debug = True)
