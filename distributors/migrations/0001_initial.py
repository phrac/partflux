# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'Distributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=64)),
                (b'affiliate_identifier', models.CharField(unique=True, max_length=64)),
                (b'slug', models.CharField(max_length=72, null=True, blank=True)),
                (b'description', models.TextField(null=True)),
                (b'url', models.URLField(null=True, blank=True)),
                (b'phone', models.CharField(max_length=16, null=True, blank=True)),
                (b'email', models.EmailField(max_length=32, null=True, blank=True)),
                (b'fax', models.CharField(max_length=16, null=True, blank=True)),
                (b'country', models.CharField(max_length=24, null=True, blank=True)),
                (b'affiliate_url', models.URLField()),
            ],
            options={
                'ordering': (b'name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'DistributorSKU',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'sku', models.CharField(max_length=32)),
                (b'distributor', models.ForeignKey(to=b'distributors.Distributor', to_field='id')),
                (b'part', models.ForeignKey(to=b'parts.Part', to_field='id', null=True)),
                (b'price', models.DecimalField(max_length=16, null=True, max_digits=6, decimal_places=2)),
                (b'url', models.URLField(max_length=256)),
                (b'affiliate_url', models.URLField(max_length=512, null=True)),
                (b'impression_url', models.URLField(max_length=512, null=True)),
                (b'updated', models.DateTimeField(auto_now=True)),
                (b'xpath', models.CharField(max_length=1024, null=True)),
            ],
            options={
                'unique_together': set([(b'sku', b'distributor')]),
            },
            bases=(models.Model,),
        ),
    ]
