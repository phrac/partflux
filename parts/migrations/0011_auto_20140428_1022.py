# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0010_auto_20140427_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name=b'category',
            name=b'slug',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
