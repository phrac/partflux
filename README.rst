========
Overview
========
Part Engine is a web application that helps users find information about any part
number. The application is written in Python using the Django framework. Search
is provided by Haystack with an Elastic Search backend, and data is stored in 
PostgreSQL.


Dependencies
============

Django Applications
------
    * Django 1.4+
    * django-orm 2.0+ (https://github.com/niwibe/django-orm)
    * django-registration 0.8+: (http://bitbucket.org/ubernostrum/django-registration/)
    * pure pagination (http://pypi.python.org/pypi/django-pure-pagination/)
    * sorl-thumbnail https://github.com/sorl/sorl-thumbnail
    * django-storages http://django-storages.readthedocs.org/en/latest/index.html
    * django-gravatar (user avatars): https://github.com/twaddington/django-gravatar
    * django-markdown-deux for notes: https://github.com/trentm/django-markdown-deux                

Python
------
    * virtualenv
    * All other Python modules: see requirements.txt (pip install -r requirements.txt)

Database
--------
    * PostgreSQL 9.0+

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

