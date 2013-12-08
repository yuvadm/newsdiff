# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HaaretzArticle'
        db.create_table(u'core_haaretzarticle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'core', ['HaaretzArticle'])

        # Adding model 'HaaretzImage'
        db.create_table(u'core_haaretzimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.HaaretzArticle'])),
            ('origin_url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['HaaretzImage'])


    def backwards(self, orm):
        # Deleting model 'HaaretzArticle'
        db.delete_table(u'core_haaretzarticle')

        # Deleting model 'HaaretzImage'
        db.delete_table(u'core_haaretzimage')


    models = {
        u'core.haaretzarticle': {
            'Meta': {'object_name': 'HaaretzArticle'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'core.haaretzimage': {
            'Meta': {'object_name': 'HaaretzImage'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.HaaretzArticle']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'origin_url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']