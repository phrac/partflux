# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'distributors', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'SKUClick',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'sku', models.ForeignKey(to=b'distributors.DistributorSKU', to_field='id')),
                (b'click_date', models.DateTimeField(auto_now_add=True)),
                (b'ip', models.IPAddressField()),
                (b'path', models.CharField(max_length=512, null=True)),
                (b'referrer', models.CharField(max_length=512, null=True)),
                (b'user_agent', models.CharField(max_length=512, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
