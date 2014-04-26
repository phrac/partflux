# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'name', models.CharField(unique=True, max_length=128)),
                (b'slug', models.CharField(unique=True, max_length=64, blank=True)),
                (b'description', models.TextField(null=True, blank=True)),
                (b'url', models.URLField(null=True, blank=True)),
                (b'wikipedia_url', models.URLField(null=True, blank=True)),
                (b'facebook_url', models.URLField(null=True, blank=True)),
                (b'twitter_name', models.CharField(max_length=32, null=True, blank=True)),
                (b'linkedin_url', models.URLField(null=True, blank=True)),
                (b'email', models.EmailField(max_length=32, null=True, blank=True)),
                (b'phone', models.CharField(max_length=16, null=True, blank=True)),
                (b'fax', models.CharField(max_length=16, null=True, blank=True)),
                (b'address1', models.CharField(max_length=64, null=True, blank=True)),
                (b'address2', models.CharField(max_length=64, null=True, blank=True)),
                (b'city', models.CharField(max_length=32, null=True, blank=True)),
                (b'state', models.CharField(max_length=32, null=True, blank=True)),
                (b'zip', models.CharField(max_length=10, null=True, blank=True)),
                (b'country', models.CharField(max_length=32, null=True, blank=True)),
                (b'created_at', models.DateTimeField(auto_now_add=True)),
                (b'updated_at', models.DateTimeField(auto_now=True)),
                (b'logo', sorl.thumbnail.fields.ImageField(null=True, upload_to=b'company_logos', blank=True)),
            ],
            options={
                'ordering': (b'name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'CompanyAltName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'company', models.ForeignKey(to=b'companies.Company', to_field='id')),
                (b'name', models.CharField(unique=True, max_length=128)),
            ],
            options={
                'ordering': (b'company',),
            },
            bases=(models.Model,),
        ),
    ]
