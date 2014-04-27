# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django_hstore.fields


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0006_auto_20140426_2156'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'CategoryProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'category', models.ForeignKey(to=b'parts.Category', to_field='id')),
                (b'key_name', models.CharField(max_length=16)),
                (b'required_key', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name=b'part',
            name=b'properties',
            field=django_hstore.fields.DictionaryField(null=True),
            preserve_default=True,
        ),
    ]
