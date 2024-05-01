# BloodAssist
## Table of Content
* [Requirements](#requirements)
* [How to run](#how-to-run)
* [Authors](#authors)
## Requirements
To execute the code, the machine must have the following intalled :
* Docker
* Python with the following packages :
   * flask
   * requests
## How to run
First, start up the couch-db server with docker. If this is the first time you run the app, you can create one with the command :
```bash
docker run --rm -t -i -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password couchdb:3.3.3
```
Then, execute the file "Server.py" and access the web application with your web browser with URL ``http://localhost:5000``.
## Authors
This applications was develloped by Aroud Farah, François Simon, Pêcheur Flore and Willem Laureline for the course [LINFO2381 - Health informatics](https://uclouvain.be/en-cours-2023-linfo2381) given at [UCLouvain](https://uclouvain.be/en/index.html) during the academic year 2023-2024.
