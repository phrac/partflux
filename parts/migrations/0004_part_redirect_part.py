# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'0003_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name=b'part',
            name=b'redirect_part',
            field=models.ForeignKey(to=b'parts.Part', to_field='id', null=True),
            preserve_default=True,
        ),
    ]
