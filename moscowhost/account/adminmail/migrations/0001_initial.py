# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomVar'
        db.create_table(u'adminmail_customvar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'adminmail', ['CustomVar'])

        # Adding model 'CustomVarValue'
        db.create_table(u'adminmail_customvarvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('custom_var', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adminmail.CustomVar'])),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'adminmail', ['CustomVarValue'])

        # Adding model 'Letter'
        db.create_table(u'adminmail_letter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('texttemplate', self.gf('django.db.models.fields.TextField')()),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'adminmail', ['Letter'])

        # Adding model 'Attachment'
        db.create_table(u'adminmail_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adminmail.Letter'])),
            ('attached', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('mime', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'adminmail', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'CustomVar'
        db.delete_table(u'adminmail_customvar')

        # Deleting model 'CustomVarValue'
        db.delete_table(u'adminmail_customvarvalue')

        # Deleting model 'Letter'
        db.delete_table(u'adminmail_letter')

        # Deleting model 'Attachment'
        db.delete_table(u'adminmail_attachment')


    models = {
        u'adminmail.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attached': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adminmail.Letter']"}),
            'mime': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'adminmail.customvar': {
            'Meta': {'object_name': 'CustomVar'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'adminmail.customvarvalue': {
            'Meta': {'object_name': 'CustomVarValue'},
            'custom_var': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adminmail.CustomVar']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'adminmail.letter': {
            'Meta': {'object_name': 'Letter'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'texttemplate': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['adminmail']