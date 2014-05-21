# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repository'
        db.create_table(u'oaiharvests_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('base_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'oaiharvests', ['Repository'])

        # Adding model 'Community'
        db.create_table(u'oaiharvests_community', (
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=256, blank=True)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oaiharvests.Repository'])),
        ))
        db.send_create_signal(u'oaiharvests', ['Community'])

        # Adding model 'Collection'
        db.create_table(u'oaiharvests_collection', (
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oaiharvests.Community'], null=True, blank=True)),
        ))
        db.send_create_signal(u'oaiharvests', ['Collection'])

        # Adding model 'Record'
        db.create_table(u'oaiharvests_record', (
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('hdr_datestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('hdr_setSpec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oaiharvests.Collection'])),
        ))
        db.send_create_signal(u'oaiharvests', ['Record'])

        # Adding model 'MetadataElement'
        db.create_table(u'oaiharvests_metadataelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oaiharvests.Record'])),
            ('element_type', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('element_data', self.gf('django.db.models.fields.TextField')(default=' ')),
        ))
        db.send_create_signal(u'oaiharvests', ['MetadataElement'])

        # Adding model 'HarvestRegistration'
        db.create_table(u'oaiharvests_harvestregistration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oaiharvests.Collection'])),
        ))
        db.send_create_signal(u'oaiharvests', ['HarvestRegistration'])


    def backwards(self, orm):
        # Deleting model 'Repository'
        db.delete_table(u'oaiharvests_repository')

        # Deleting model 'Community'
        db.delete_table(u'oaiharvests_community')

        # Deleting model 'Collection'
        db.delete_table(u'oaiharvests_collection')

        # Deleting model 'Record'
        db.delete_table(u'oaiharvests_record')

        # Deleting model 'MetadataElement'
        db.delete_table(u'oaiharvests_metadataelement')

        # Deleting model 'HarvestRegistration'
        db.delete_table(u'oaiharvests_harvestregistration')


    models = {
        u'oaiharvests.collection': {
            'Meta': {'object_name': 'Collection'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Community']", 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'oaiharvests.community': {
            'Meta': {'object_name': 'Community'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '256', 'blank': 'True'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Repository']"})
        },
        u'oaiharvests.harvestregistration': {
            'Meta': {'object_name': 'HarvestRegistration'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Collection']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'oaiharvests.metadataelement': {
            'Meta': {'object_name': 'MetadataElement'},
            'element_data': ('django.db.models.fields.TextField', [], {'default': "' '"}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Record']"})
        },
        u'oaiharvests.record': {
            'Meta': {'object_name': 'Record'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'hdr_datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'hdr_setSpec': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Collection']"}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'oaiharvests.repository': {
            'Meta': {'object_name': 'Repository'},
            'base_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['oaiharvests']