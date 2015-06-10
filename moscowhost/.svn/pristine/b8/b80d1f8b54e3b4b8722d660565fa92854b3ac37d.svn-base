# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LeftBlockMenuPage'
        db.create_table(u'page_leftblockmenupage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['page.LeftBlockMenuPage'], null=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'page', ['LeftBlockMenuPage'])

        # Adding model 'Send_mail'
        db.create_table('db_send_mail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('spis_file', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('status_mail', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sender_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'page', ['Send_mail'])

        # Adding model 'Sender'
        db.create_table(u'page_sender', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('stop_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('common_message', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('success_message', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('failed_message', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'page', ['Sender'])

        # Adding model 'UserFiles'
        db.create_table(u'page_userfiles', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['page.Sender'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'page', ['UserFiles'])


    def backwards(self, orm):
        # Deleting model 'LeftBlockMenuPage'
        db.delete_table(u'page_leftblockmenupage')

        # Deleting model 'Send_mail'
        db.delete_table('db_send_mail')

        # Deleting model 'Sender'
        db.delete_table(u'page_sender')

        # Deleting model 'UserFiles'
        db.delete_table(u'page_userfiles')


    models = {
        u'page.leftblockmenupage': {
            'Meta': {'object_name': 'LeftBlockMenuPage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['page.LeftBlockMenuPage']", 'null': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.message': {
            'Meta': {'object_name': 'Message', 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users_type': ('django.db.models.fields.CharField', [], {'max_length': '13'})
        },
        u'page.send_mail': {
            'Meta': {'object_name': 'Send_mail', 'db_table': "'db_send_mail'"},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'sender_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spis_file': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status_mail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'page.sender': {
            'Meta': {'object_name': 'Sender'},
            'common_message': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'failed_message': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'stop_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'success_message': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'page.userfiles': {
            'Meta': {'object_name': 'UserFiles'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['page.Sender']"})
        }
    }

    complete_apps = ['page']