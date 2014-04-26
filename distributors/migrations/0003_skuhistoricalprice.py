# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'parts', b'__first__'),
        (b'distributors', b'0002_skuclick'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'SKUHistoricalPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'part', models.ForeignKey(to=b'parts.Part', to_field='id')),
                (b'sku', models.ForeignKey(to=b'distributors.DistributorSKU', to_field='id')),
                (b'date', models.DateTimeField(auto_now_add=True)),
                (b'price', models.IntegerField(max_length=16)),
                (b'price_UOM', models.CharField(max_length=9)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
