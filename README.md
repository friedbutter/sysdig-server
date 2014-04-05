sysdig-server
=============

sysdig server that gets all the requests from clients

I wrote this to test sysdig over http. This is just a test server, and I will maintain this.

Copy/Clone whatever you need.. 

Install
=======

Create a python virtual environment. 
Install MongoDB
Install modules from requirements.txt

Run
===

Run behind a gunicorn:
    python manage.py rungunicorn --gunicorn-config gunicorn.ini

Run naked: 
    python manage.py runserver
