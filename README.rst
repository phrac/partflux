========
Overview
========
Partfindr is a web application that helps users find information about any part
number. The application is written in Python using the Django framework. Search
is provided by Apache Lucene/Solr, and data is stored in PostgreSQL.


Dependencies
============

Python
------
    * Django 1.4+
    * django-orm 2.0+ (https://github.com/niwibe/django-orm)
    * django-registration 0.8+: (hg clone http://bitbucket.org/ubernostrum/django-registration/)
    * pure pagination (http://pypi.python.org/pypi/django-pure-pagination/)
    * django-haystack 2.0+ (http://haystacksearch.org/)
    * sorl-thumbnail https://github.com/sorl/sorl-thumbnail
    * django-storages http://django-storages.readthedocs.org/en/latest/index.html
    * django-gravatar for user avatars: https://github.com/twaddington/django-gravatar            


Database
--------
    * PostgreSQL 9.0+
    * hstore contrib module (contrib/hstore.sql)

Search
------
    * ElasticSearch (http://www.elasticsearch.org/)
    * pyelasticsearch (https://github.com/toastdriven/pyelasticsearch.git)


Other Requirements
------------------
    * Amazon AWS/S3 account for file storage

