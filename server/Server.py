#!/usr/bin/env python3

import json


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
    with open('server/questions.html', 'r') as f:
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

@app.route('/lookup-patients', methods = [ 'POST' ])
def lookup_patient():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())
    
    # TODO


@app.route('/lookup-observations', methods = [ 'POST' ])
def lookup_observations():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    body = json.loads(request.get_data())
    
    answer = []
    
    # TODO
    

    return Response(json.dumps(answer), mimetype = 'application/json')


if __name__ == '__main__':
    app.run(debug = True)
