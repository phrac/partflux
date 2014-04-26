# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'attribute',
            name=b'part',
            field=models.ForeignKey(to=b'parts.Part', to_field='id'),
            preserve_default=True,
        ),
    ]
