========
Overview
========
Part Flux is a web application that helps users find information about any part
number. The application is written in Python using the Django framework. Search
is provided by Haystack with an Elastic Search backend, and data is stored in 
PostgreSQL.


Dependencies
============

Django
------
    * Django 1.7+
    * virtualenv __HIGHLY RECOMMENDED__
    * All other Python modules: see requirements.txt (pip install -r requirements.txt)

Database
--------
    * PostgreSQL 9.0+
    * hstore extension (CREATE EXTENSION hstore)

Search
------
    * Haystack 2.0+ https://github.com/toastdriven/django-haystack
    * pyelasticsearch
    * Elastic Search 0.19+
     
Web Server
----------
    * nginx
    * mod_uwsgi (see wsgi file)                    

Other Requirements
------------------
    * Amazon AWS/S3 account for file storage  

