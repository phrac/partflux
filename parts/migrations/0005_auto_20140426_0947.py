# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0004_part_redirect_part'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'part',
            name=b'cross_references',
            field=models.ManyToManyField(to=b'parts.Part'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name=b'attribute',
            unique_together=set([(b'part', b'key', b'value')]),
        ),
        migrations.AlterUniqueTogether(
            name=b'part',
            unique_together=set([(b'number', b'company')]),
        ),
    ]
