========
Overview
========
Complete rewrite of the basic partfindr application in Python + Django


Dependencies
============

Python
------
	* Django 1.3.1
	* django-orm 2.0+ (https://github.com/niwibe/django-orm)
	* django-registration 0.8+: (hg clone http://bitbucket.org/ubernostrum/django-registration/)
	* pure pagination (http://pypi.python.org/pypi/django-pure-pagination/)

Database
--------
	* PostgreSQL 9.0+
	* hstore contrib module (contrib/hstore.sql)
	 
Custom FTS trigger needed on updates::

        CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON parts_part FOR EACH ROW EXECUTE PROCEDURE 
        tsvector_update_trigger('tsv', 'pg_catalog.english', 'number', 'description')	

Also need unindent custom function
