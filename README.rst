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
	 

Database indexes, triggers, functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Custom FTS trigger needed on updates and inserts::

    CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON parts_part FOR EACH ROW EXECUTE PROCEDURE 
    tsvector_update_trigger('tsv', 'pg_catalog.english', 'number', 'description')	

Unaccent function (http://readthedocs.org/docs/django-orm/en/latest/postgresql/fts.html)::

    CREATE OR REPLACE FUNCTION unaccent(text) RETURNS text AS $$
    DECLARE input_string text := $1;
    BEGIN
        input_string := translate(input_string, '??????????????????', 'aaaaaaaaaaaaaaaaaa');
        input_string := translate(input_string, '???????????????????', 'eeeeeeeeeeeeeeeeeee');
        input_string := translate(input_string, '??????????????', 'iiiiiiiiiiiiii');
        input_string := translate(input_string, '????????????????', 'oooooooooooooooo');
        input_string := translate(input_string, '????????????????', 'uuuuuuuuuuuuuuuu');
        input_string := translate(input_string, '????', 'nncc');
        return input_string;
    END; $$ LANGUAGE plpgsql IMMUTABLE;


