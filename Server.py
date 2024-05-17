#!/usr/bin/env python3

import json
import datetime


##
## Initialization of the CouchDB server (creation of a collection of
## documents named "blood_db" for blood banks and "users_db" for the listed blood givers, if not already existing)
##
import CouchDBClient as CouchDBClient

client = CouchDBClient.CouchDBClient()

critical_id = "37dfb07408d165283133578aa7000327"

# client.reset()   # If you want to clear the entire content of CouchDB
# TODO QUESTION : all id generated are the same (??)

def fill_bloodbank():
    print("Filling blood_db...")
    client.addDocument('blood_db', {'type':'entry','btype' : 'O-', 'stock' : 564,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'O+', 'stock' : 654,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'A-', 'stock' : 405,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'A+', 'stock' : 1352,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'B-', 'stock' : 657,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'B+', 'stock' : 1567,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'AB-', 'stock' : 1300,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'AB+', 'stock' : 1152,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'A+', 'stock' : 1568,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'B-', 'stock' : 865,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'B+', 'stock' : 364,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'AB-', 'stock' : 325,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'AB+', 'stock' : 209,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'O+', 'stock' : -5,'unit' : 'l'})
    client.addDocument('blood_db', {'type':'entry','btype' : 'B+', 'stock' : -246,'unit' : 'l'})

    critical_id = client.addDocument('blood_db', {'type' : 'criticalstocks', 'O-' : 1000, 'O+' : 1000,'AB+' : 1000,'A+' : 1000,'B+' : 1000,'AB-' : 1000,'A-' : 1000,'B-' : 1000})


if not 'blood_db' in client.listDatabases():
    client.createDatabase('blood_db')
    fill_bloodbank()
if not 'users_db' in client.listDatabases():
    client.createDatabase('users_db')


##
## Create views (users db by user type, blood db by blood type)
## Can be used later to list information 
##
client.installView('users_db', 'users', 'by_bloodtype', '''
function(doc) {
emit(doc.btype,doc.email);
}
''')
# View to facilitate login
client.installView('users_db', 'users', 'by_email', '''
function(doc) {
if (doc.type == 'user') {
    emit(doc.email, doc.password);}
}
''')
client.installView('blood_db','entries','by_type','''
function(doc) {
emit(doc.type,doc);
}
'''
)

# Total of all entries per blood type
# TODO : The reduce function doesn't seem to work
client.installView('blood_db', 'banks', 'by_bloodtype', '''
function(doc) {
if (doc.type == 'entry') {
    emit(doc.btype, doc.stock);}
}
''')





##
## Serving static HTML/JavaScript resources using Flask
##

from flask import Flask, Response, request, redirect, url_for
app = Flask(__name__, static_url_path='/static')

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

@app.route('/register', methods = [ 'GET' ])
def register():
    with open('register.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')
    
@app.route('/questions')
def questions():
    with open('questions.html', 'r') as f:
        return Response(f.read(), mimetype='text/html')
    
# ##
# ## REST API for questions.html
# ##  
# @app.route('/create-user', methods = ['POST'])
# def create_user():
#     body = json.loads(request.get_data())

#     userID = None
#     doc = {
#         'type' : 'user',
#         'name' : body['name'],
#         'gender' : body['gender'],
#         'birthDate' : body['dob'],
#         'btype' : body['btype']
#     }
#     userID = client.addDocument('users_db',doc) # New patient document (vs. new EHR for EHRBase)
#     print("User added. ID:", userID)

#     return Response(json.dumps({
#         'id' : userID
#     }), mimetype = 'application/json')
    
# ##
# ## REST API for index.html
# ##   
# @app.route('/create-user', methods = [ 'POST' ])
# def create_patient():
#     # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
#     body = json.loads(request.get_data())

    # patientId = None
    # doc = {
    #     'type' : 'user',
    #     'firstName' : body['fname'],
    #     'lastName' : body['lname'],
    #     'email' : body['email'],
    #     'btype' : body['btype']
    # }
    # patientId = client.addDocument('users_db',doc) # New patient document (vs. new EHR for EHRBase)
    # print("User added. ID:", patientId)

    # return Response(json.dumps({
    #     'id' : patientId
    # }), mimetype = 'application/json')


@app.route('/check-login',methods=['POST'])
def check_login():
    body = json.loads(request.get_data())
    email = body['email']
    password = body['password']
    user = client.executeView('users_db', 'users', 'by_email', key=email)
    # TODO : Corner case when 2 users have the same email
    if user[0]['value'] == password:
        print("Password is correct")
        resp = Response(json.dumps({'success': True}),mimetype = 'application/json')
        print(resp.data)
        return resp
    else:
        print("Password is incorrect")
        return Response(json.dumps({'success': False}), mimetype = 'application/json')


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
# TODO QUESTION : Comment ne pas hardcoder le id de critical? 
# TODO QUESTION : 
@app.route('/lookup-blood-stock', methods = [ 'GET' ])
def lookup_blood_stock():
    # "request.get_json()" necessitates the client to have set "Content-Type" to "application/json"
    groups = client.executeView('blood_db','banks', 'by_bloodtype')
    critical = client.executeView('blood_db','entries','by_type',key='criticalstocks')[0]  
    stock_dict = {}
    for stock in groups:
        key = stock['key']
        value = stock['value']
        if key in stock_dict:
            stock_dict[key] += value
        else:
            stock_dict[key] = value

    stocks = []
    for k,v in stock_dict.items() :
        stocks.append({
            'type' : k, 
            'stock' : v, 
            'criticalstock' : critical['value'][k]})
    
    return Response(json.dumps(stocks), mimetype = 'application/json')



if __name__ == '__main__':
    app.run(debug = True)
