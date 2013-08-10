# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'parts_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parts.Category'], null=True)),
        ))
        db.send_create_signal(u'parts', ['Category'])

        # Adding model 'Part'
        db.create_table(u'parts_part', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('redirect_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parts.Part'], null=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['companies.Company'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('hits', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('asin', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('upc', self.gf('django.db.models.fields.CharField')(max_length=13, null=True)),
            ('ean', self.gf('django.db.models.fields.CharField')(max_length=13, null=True)),
        ))
        db.send_create_signal(u'parts', ['Part'])

        # Adding unique constraint on 'Part', fields ['number', 'company']
        db.create_unique(u'parts_part', ['number', 'company_id'])

        # Adding M2M table for field categories on 'Part'
        m2m_table_name = db.shorten_name(u'parts_part_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('part', models.ForeignKey(orm[u'parts.part'], null=False)),
            ('category', models.ForeignKey(orm[u'parts.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['part_id', 'category_id'])

        # Adding M2M table for field images on 'Part'
        m2m_table_name = db.shorten_name(u'parts_part_images')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('part', models.ForeignKey(orm[u'parts.part'], null=False)),
            ('partimage', models.ForeignKey(orm[u'parts.partimage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['part_id', 'partimage_id'])

        # Adding M2M table for field cross_references on 'Part'
        m2m_table_name = db.shorten_name(u'parts_part_cross_references')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_part', models.ForeignKey(orm[u'parts.part'], null=False)),
            ('to_part', models.ForeignKey(orm[u'parts.part'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_part_id', 'to_part_id'])

        # Adding model 'Attribute'
        db.create_table(u'parts_attribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parts.Part'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('downvotes', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'parts', ['Attribute'])

        # Adding unique constraint on 'Attribute', fields ['part', 'key', 'value']
        db.create_unique(u'parts_attribute', ['part_id', 'key', 'value'])

        # Adding model 'PartImage'
        db.create_table(u'parts_partimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('album_cover', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'parts', ['PartImage'])


    def backwards(self, orm):
        # Removing unique constraint on 'Attribute', fields ['part', 'key', 'value']
        db.delete_unique(u'parts_attribute', ['part_id', 'key', 'value'])

        # Removing unique constraint on 'Part', fields ['number', 'company']
        db.delete_unique(u'parts_part', ['number', 'company_id'])

        # Deleting model 'Category'
        db.delete_table(u'parts_category')

        # Deleting model 'Part'
        db.delete_table(u'parts_part')

        # Removing M2M table for field categories on 'Part'
        db.delete_table(db.shorten_name(u'parts_part_categories'))

        # Removing M2M table for field images on 'Part'
        db.delete_table(db.shorten_name(u'parts_part_images'))

        # Removing M2M table for field cross_references on 'Part'
        db.delete_table(db.shorten_name(u'parts_part_cross_references'))

        # Deleting model 'Attribute'
        db.delete_table(u'parts_attribute')

        # Deleting model 'PartImage'
        db.delete_table(u'parts_partimage')


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
        u'parts.attribute': {
            'Meta': {'ordering': "('value',)", 'unique_together': "(('part', 'key', 'value'),)", 'object_name': 'Attribute'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'downvotes': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'part': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parts.Part']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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

    complete_apps = ['parts']