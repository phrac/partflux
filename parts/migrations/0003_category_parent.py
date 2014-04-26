# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0002_attribute_part'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'category',
            name=b'parent',
            field=models.ForeignKey(to=b'parts.Category', to_field='id', null=True),
            preserve_default=True,
        ),
    ]
