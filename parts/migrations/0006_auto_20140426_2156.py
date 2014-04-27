# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0005_auto_20140426_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'part',
            name=b'category',
            field=models.ForeignKey(to=b'parts.Category', to_field='id', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name=b'part',
            name=b'redirect_part',
        ),
        migrations.RemoveField(
            model_name=b'part',
            name=b'categories',
        ),
        migrations.RemoveField(
            model_name=b'part',
            name=b'approved',
        ),
        migrations.RemoveField(
            model_name=b'part',
            name=b'hits',
        ),
    ]
