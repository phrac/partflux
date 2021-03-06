# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-13 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0011_auto_20140428_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='categoryproperty',
            options={'verbose_name_plural': 'Category Properties'},
        ),
        migrations.AlterField(
            model_name='part',
            name='cross_references',
            field=models.ManyToManyField(related_name='xrefs', to='parts.Part'),
        ),
    ]
