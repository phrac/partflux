# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        (b'companies', b'__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'PartImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'image', sorl.thumbnail.fields.ImageField(upload_to=b'part_images')),
                (b'approved', models.BooleanField(default=True)),
                (b'album_cover', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'key', models.CharField(max_length=64)),
                (b'value', models.CharField(max_length=128)),
            ],
            options={
                'ordering': (b'value',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=64)),
                (b'slug', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'number', models.CharField(max_length=48)),
                (b'slug', models.CharField(max_length=64)),
                (b'description', models.TextField()),
                (b'long_description', models.TextField(null=True)),
                (b'company', models.ForeignKey(to=b'companies.Company', to_field='id')),
                (b'created_at', models.DateTimeField(auto_now_add=True)),
                (b'updated_at', models.DateTimeField(auto_now=True)),
                (b'hits', models.IntegerField(default=0, editable=False)),
                (b'approved', models.BooleanField(default=True)),
                (b'image_url', models.URLField(max_length=512, null=True)),
                (b'asin', models.CharField(max_length=10, null=True)),
                (b'upc', models.CharField(max_length=13, null=True)),
                (b'ean', models.CharField(max_length=13, null=True)),
                (b'weight', models.DecimalField(null=True, max_digits=7, decimal_places=2)),
                (b'categories', models.ManyToManyField(to=b'parts.Category')),
                (b'images', models.ManyToManyField(to=b'parts.PartImage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
