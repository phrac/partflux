========
Overview
========
Partfindr is a web application that helps users find information about any part
number. The application is written in Python using the Django framework. Search
is provided by Google Custom Search, and data is stored in PostgreSQL.


Dependencies
============

Python
------
    * Django 1.4+
    * django-orm 2.0+ (https://github.com/niwibe/django-orm)
    * django-registration 0.8+: (hg clone http://bitbucket.org/ubernostrum/django-registration/)
    * pure pagination (http://pypi.python.org/pypi/django-pure-pagination/)
    * sorl-thumbnail https://github.com/sorl/sorl-thumbnail
    * django-storages http://django-storages.readthedocs.org/en/latest/index.html
    * django-gravatar for user avatars: https://github.com/twaddington/django-gravatar
    * django-markdown-deux for notes: https://github.com/trentm/django-markdown-deux                


Database
--------
    * PostgreSQL 9.0+

Search
------
    * Googlesearch django module


Other Requirements
------------------
    * Amazon AWS/S3 account for file storage

