#!/usr/bin/env python3

import datetime
import random


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
## Goal: Create a patient, record a few temperatures, retrieve the
## temperatures associated with the patient, and finally retrieve the
## name of all the patients stored in the CouchDB databases.
##

## 1. Create one new patient (which corresponds to an EHR in the
## framework of openEHR CDR) and associate it with a demographic
## information (i.e., patient's name)

patientName = 'John Doe n°%d' % random.randint(0, 1000)

# TODO -> OK
doc = {
    'type' : 'patient',
    'name' : patientName
}
patientID = client.addDocument('ehr',doc)


## 2. Record a few random temperatures

for i in range(10):
    temperature = random.uniform(35, 40)
    now = datetime.datetime.now().isoformat()

    # TODO -> OK
    doc = {
        'type' : 'temperature',
        'patient_id' : patientID,
        'temperature' : temperature,
        'time' : now
    }
    client.addDocument('ehr',doc)
    


## 3. Retrieve all the temperatures that have just been stored, sorted
## by increasing time

# TODO -> OK
# Option 1 (slow) : use client.listDocuments
# Option 2 : Use client.installView that requires a Java map() method
# The map function selects all 'temperature' documents and emits them with their patient id
client.installView('ehr','temperatures','by_id','''
function(elem) { 
                   if(elem.type == 'temperature'){
                   emit(elem.patient_id, elem); 
                   }
}
                   ''')
comps = client.executeView('ehr','temperatures','by_id',patientID) # Restrict to elements mapped to the key
comps_list = list(map(lambda x : x['value'],comps))

for comp in sorted(comps_list, key = lambda x : x['time']): # sort by time
    print('At %s: %.1f °C' % (comp['time'],
                              comp['temperature']))

## 4. Retrieve the name of all the patients stored in the database

# TODO -> OK
client.installView('ehr','patient_names','by_name','''
function(elem) { 
                   if(elem.type == 'patient'){
                   emit(elem.name,doc);
                   }
}
                   ''')
comps = client.executeView('ehr','patient_names','by_name')
comps_list = list(map(lambda x : x['value'],comps)) 
# QUESTION : pq value dans la solution??
# REP : 'value' renvoie la valeur du truc, pour avoir les parametres on écrit ['value']['id']

for comp in comps_list:
    print('Patient %s is %s' % (comp['__id'],
                              comp['name']))

