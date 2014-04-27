# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0009_auto_20140427_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'category',
            name=b'parent',
            field=models.ForeignKey(to_field='id', blank=True, to=b'parts.Category', null=True),
        ),
        migrations.AlterField(
            model_name=b'category',
            name=b'slug',
            field=models.CharField(max_length=128, unique=True, null=True, blank=True),
        ),
    ]
