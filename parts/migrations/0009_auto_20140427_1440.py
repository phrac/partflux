# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0008_auto_20140427_1439'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name=b'categoryproperty',
            unique_together=set([(b'category', b'key_name')]),
        ),
    ]
