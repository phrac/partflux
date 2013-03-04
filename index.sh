#!/bin/sh

cd /home/derek/partengine
. bin/activate
cd partengine
python manage.py update_index --age=5

