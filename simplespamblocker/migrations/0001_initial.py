# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Option'
        db.create_table('simplespamblocker_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('block_author', self.gf('simplespamblocker.fields.ValidRegexField')(blank=True)),
            ('block_content', self.gf('simplespamblocker.fields.ValidRegexField')(blank=True)),
            ('block_email', self.gf('simplespamblocker.fields.ValidRegexField')(blank=True)),
            ('block_url', self.gf('simplespamblocker.fields.ValidRegexField')(blank=True)),
            ('block_remote_addr', self.gf('simplespamblocker.fields.ValidRegexField')(blank=True)),
            ('block_http_referer', self.gf('simplespamblocker.fields.ValidRegexField')(blank=True)),
            ('block_http_user_agent', self.gf('simplespamblocker.fields.ValidRegexField')(blank=True)),
        ))
        db.send_create_signal('simplespamblocker', ['Option'])


    def backwards(self, orm):
        # Deleting model 'Option'
        db.delete_table('simplespamblocker_option')


    models = {
        'simplespamblocker.option': {
            'Meta': {'object_name': 'Option'},
            'block_author': ('simplespamblocker.fields.ValidRegexField', [], {'blank': 'True'}),
            'block_content': ('simplespamblocker.fields.ValidRegexField', [], {'blank': 'True'}),
            'block_email': ('simplespamblocker.fields.ValidRegexField', [], {'blank': 'True'}),
            'block_http_referer': ('simplespamblocker.fields.ValidRegexField', [], {'blank': 'True'}),
            'block_http_user_agent': ('simplespamblocker.fields.ValidRegexField', [], {'blank': 'True'}),
            'block_remote_addr': ('simplespamblocker.fields.ValidRegexField', [], {'blank': 'True'}),
            'block_url': ('simplespamblocker.fields.ValidRegexField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['simplespamblocker']