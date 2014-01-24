# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'HaaretzImage.origin_url'
        db.alter_column(u'core_haaretzimage', 'origin_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250))

        # Changing field 'HaaretzArticle.subtitle'
        db.alter_column(u'core_haaretzarticle', 'subtitle', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))

        # Changing field 'HaaretzArticle.title'
        db.alter_column(u'core_haaretzarticle', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'HaaretzArticle.url'
        db.alter_column(u'core_haaretzarticle', 'url', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'HaaretzArticle.author'
        db.alter_column(u'core_haaretzarticle', 'author', self.gf('django.db.models.fields.CharField')(max_length=60))

    def backwards(self, orm):

        # Changing field 'HaaretzImage.origin_url'
        db.alter_column(u'core_haaretzimage', 'origin_url', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True))

        # Changing field 'HaaretzArticle.subtitle'
        db.alter_column(u'core_haaretzarticle', 'subtitle', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))

        # Changing field 'HaaretzArticle.title'
        db.alter_column(u'core_haaretzarticle', 'title', self.gf('django.db.models.fields.CharField')(max_length=140))

        # Changing field 'HaaretzArticle.url'
        db.alter_column(u'core_haaretzarticle', 'url', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'HaaretzArticle.author'
        db.alter_column(u'core_haaretzarticle', 'author', self.gf('django.db.models.fields.CharField')(max_length=30))

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.haaretzarticle': {
            'Meta': {'object_name': 'HaaretzArticle'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'haaretz_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'core.haaretzimage': {
            'Meta': {'object_name': 'HaaretzImage'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['core.HaaretzArticle']"}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'origin_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        u'core.newsdiffuser': {
            'Meta': {'object_name': 'NewsDiffUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['core']