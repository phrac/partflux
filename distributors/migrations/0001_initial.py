# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Distributor'
        db.create_table(u'distributors_distributor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=72, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=32, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
            ('affiliate_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'distributors', ['Distributor'])

        # Adding model 'DistributorSKU'
        db.create_table(u'distributors_distributorsku', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sku', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('distributor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distributors.Distributor'])),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parts.Part'], null=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_length=16, null=True, max_digits=6, decimal_places=2)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=256)),
            ('affiliate_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('xpath', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
        ))
        db.send_create_signal(u'distributors', ['DistributorSKU'])

        # Adding unique constraint on 'DistributorSKU', fields ['sku', 'distributor']
        db.create_unique(u'distributors_distributorsku', ['sku', 'distributor_id'])

        # Adding model 'SKUHistoricalPrice'
        db.create_table(u'distributors_skuhistoricalprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parts.Part'])),
            ('sku', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['distributors.DistributorSKU'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')(max_length=16)),
            ('price_UOM', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal(u'distributors', ['SKUHistoricalPrice'])


    def backwards(self, orm):
        # Removing unique constraint on 'DistributorSKU', fields ['sku', 'distributor']
        db.delete_unique(u'distributors_distributorsku', ['sku', 'distributor_id'])

        # Deleting model 'Distributor'
        db.delete_table(u'distributors_distributor')

        # Deleting model 'DistributorSKU'
        db.delete_table(u'distributors_distributorsku')

        # Deleting model 'SKUHistoricalPrice'
        db.delete_table(u'distributors_skuhistoricalprice')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'companies.company': {
            'Meta': {'object_name': 'Company'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'facebook_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'logo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'twitter_name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'wikipedia_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'distributors.distributor': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Distributor'},
            'affiliate_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '72', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'distributors.distributorsku': {
            'Meta': {'unique_together': "(('sku', 'distributor'),)", 'object_name': 'DistributorSKU'},
            'affiliate_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'distributor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['distributors.Distributor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parts.Part']", 'null': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_length': '16', 'null': 'True', 'max_digits': '6', 'decimal_places': '2'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '256'}),
            'xpath': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'})
        },
        u'distributors.skuhistoricalprice': {
            'Meta': {'object_name': 'SKUHistoricalPrice'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parts.Part']"}),
            'price': ('django.db.models.fields.IntegerField', [], {'max_length': '16'}),
            'price_UOM': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'sku': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['distributors.DistributorSKU']"})
        },
        u'parts.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parts.Category']", 'null': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'parts.part': {
            'Meta': {'unique_together': "(('number', 'company'),)", 'object_name': 'Part'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'asin': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'part_category'", 'symmetrical': 'False', 'to': u"orm['parts.Category']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['companies.Company']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cross_references': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'xrefs'", 'symmetrical': 'False', 'to': u"orm['parts.Part']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'ean': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['parts.PartImage']", 'symmetrical': 'False'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'redirect_part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parts.Part']", 'null': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'parts.partimage': {
            'Meta': {'object_name': 'PartImage'},
            'album_cover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['distributors']