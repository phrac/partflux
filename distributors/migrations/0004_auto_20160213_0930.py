# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-13 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0003_skuhistoricalprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skuclick',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='skuhistoricalprice',
            name='price',
            field=models.IntegerField(),
        ),
    ]
