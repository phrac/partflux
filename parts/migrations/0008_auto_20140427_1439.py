# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0007_auto_20140426_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name=b'part',
            name=b'weight',
        ),
        migrations.AlterField(
            model_name=b'part',
            name=b'ean',
            field=models.CharField(max_length=13, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name=b'part',
            name=b'properties',
            field=django_hstore.fields.DictionaryField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name=b'part',
            name=b'upc',
            field=models.CharField(max_length=13, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name=b'part',
            name=b'long_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name=b'part',
            name=b'asin',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
