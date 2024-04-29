#!/usr/bin/env python3

# Copyright (c) 2024, Sebastien Jodogne, ICTEAM UCLouvain, Belgium
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import json
import requests
import requests.auth
import urllib.parse

# Class that represents a connection to some CouchDB server
class CouchDBClient:

    # Constructor for the connection: An URL, an username, and a
    # password are expected.
    def __init__(self,
                 url = 'http://localhost:5984',
                 username = 'admin',
                 password = 'admin'):
        # Make sure that the URL does not end with a slash
        if url.endswith('/'):
            self.url = url[0 : len(url) - 1]
        else:
            self.url = url

        self.username = username
        self.password = password

    def _getAuthentication(self):
        return requests.auth.HTTPBasicAuth(self.username, self.password)

    def _generateUuid(self):
        r = requests.get('%s/_uuids' % self.url,
                         params = {
                             'count' : 1
                         })
        r.raise_for_status()
        return r.json() ['uuids'][0]

    def _getDocumentRevision(self, db, key):
        return self.getDocument(db, key) ['_rev']


    # Return the list of all the databases (i.e., all the collections
    # of JSON documents) that are defined in the CouchDB server.
    def listDatabases(self):
        r = requests.get('%s/_all_dbs' % self.url,
                         auth = self._getAuthentication())
        r.raise_for_status()

        return r.json()


    # Create a new database in the CouchDB server (i.e., a collection
    # of JSON documents), and return the identifier of the newly
    # created database.
    def createDatabase(self, name):
        r = requests.put('%s/%s' % (self.url, name),
                         auth = self._getAuthentication())
        r.raise_for_status()


    # Delete the given database from the CouchDB server, including all
    # of its documents.
    def deleteDatabase(self, name):
        r = requests.delete('%s/%s' % (self.url, name),
                            auth = self._getAuthentication())
        r.raise_for_status()


    # Add a new JSON document with content "doc" to the database whose
    # name is "db", and return the identifier of the newly created
    # document.
    #
    # By default, this identifier is a UUID (universally unique
    # identifier) that is automatically generated by CouchDB. If you
    # want to manually set an identifier by yourself, you can specify
    # it in the "_id" field of "doc".
    def addDocument(self, db, doc):
        if '_id' in doc:
            key = doc['_id']
        else:
            key = self._generateUuid()
        
        r = requests.put('%s/%s/%s' % (self.url, db, key),
                         data = json.dumps(doc),
                         auth = self._getAuthentication())
        r.raise_for_status()

        return key


    # Return the list of the identifiers of all the documents that are
    # part of the database "db".
    def listDocuments(self, db):
        r = requests.get('%s/%s/_all_docs' % (self.url, db),
                         auth = self._getAuthentication())
        r.raise_for_status()

        result = []
        for row in r.json() ['rows']:
            if not row['id'].startswith('_design/'):  # Ignore design documents
                result.append(row['id'])
            
        return result


    # Return the content of the JSON document associated with
    # identifier "key" that is part of the database "db".
    def getDocument(self, db, key):
        r = requests.get('%s/%s/%s' % (self.url, db, key),
                         auth = self._getAuthentication())
        r.raise_for_status()
        return r.json()


    # Replace the content of the JSON document associated with
    # identifier "key" that is part of the database "db", with the
    # document "doc" that is provided in argument.
    #
    # This method takes care of revisions (MVCC) in a very basic way:
    # By default, the handling of conflicts simply consists in
    # overwriting the latest version of the document. If you want to
    # resolve conflicts by yourself, the argument "revision" must
    # contain the revision of the document that you intend to replace.
    def replaceDocument(self, db, key, doc, revision = None):
        if revision == None:
            revision = self._getDocumentRevision(db, key)
        
        r = requests.put('%s/%s/%s?rev=%s' % (self.url, db, key, urllib.parse.quote(revision)),
                         data = json.dumps(doc),
                         auth = self._getAuthentication())
        r.raise_for_status()


    # Delete the document associated with identifier "key" that is
    # part of the database "db".
    #
    # By default, the method will delete the latest version of the
    # document (the security mechanism of MVCC is bypassed). If you
    # want to control revisions by yourself, the argument "revision"
    # must contain the revision of the document that you intend to
    # remove.
    def deleteDocument(self, db, key, revision = None):
        if revision == None:
            revision = self._getDocumentRevision(db, key)
        
        r = requests.delete('%s/%s/%s?rev=%s' % (self.url, db, key, urllib.parse.quote(revision)),
                            auth = self._getAuthentication())
        r.raise_for_status()


    # Install a view called "viewName" in database "db", inside the
    # design document with name "designName". The view must contain a
    # map() function defined in JavaScript (this function is provided
    # as a string in argument "mapFunction"). If this view is already
    # installed, it is simply overwritten (the security mechanism of
    # MVCC is bypassed).
    #
    # In addition to the mandatory map() function, the view can
    # contain a reduce() function (also provided as a string
    # containing a JavaScript function in argument "reduceFunction").
    def installView(self, db, designName, viewName, mapFunction, reduceFunction = None):
        r = requests.get('%s/%s/_design/%s' % (self.url, db, designName),
                         auth = self._getAuthentication())

        if r.status_code == 404:
            design = {
                'views' : {
                }
            }
            revision = None
        else:
            design = r.json()
            revision = r.json() ['_rev']

        design['views'][viewName] = {
            'map' : mapFunction,
        }

        if reduceFunction != None:
            design['views'][viewName]['reduce'] = reduceFunction

        if revision == None:
            r = requests.put('%s/%s/_design/%s' % (self.url, db, designName),
                             data = json.dumps(design),
                             auth = self._getAuthentication())
        else:
            r = requests.put('%s/%s/_design/%s?rev=%s' % (self.url, db, designName, urllib.parse.quote(revision)),
                             data = json.dumps(design),
                             auth = self._getAuthentication())

        r.raise_for_status()
        

    # Execute the view "viewName", installed inside the design
    # document "designName" of the database "db".
    #
    # If provided, the argument "key" restricts the view to the JSON
    # documents in the view that are mapped to the provided key.
    def executeView(self, db, designName, viewName, key = None):
        params = {}
        if key != None:
            params['key'] = '"%s"' % key
        
        r = requests.get('%s/%s/_design/%s/_view/%s' % (self.url, db, designName, viewName),
                         params = params,
                         auth = self._getAuthentication())
        r.raise_for_status()
        return r.json() ['rows']


    # Remove all the databases and all the JSON documents that are
    # currently stored inside the CouchDB server.
    def reset(self):
        for db in self.listDatabases():
            self.deleteDatabase(db)
