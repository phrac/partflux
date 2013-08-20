#!/bin/sh

cd /home/derek/partflux
. bin/activate
cd partengine
python manage.py update_index --age=2 

