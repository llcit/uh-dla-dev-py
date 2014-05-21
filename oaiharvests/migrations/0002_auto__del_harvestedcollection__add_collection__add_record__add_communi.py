# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HarvestedCollection'
        db.delete_table(u'oaiharvests_harvestedcollection')

        # Adding model 'Collection'
        db.create_table(u'oaiharvests_collection', (
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('community', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oaiharvests.Community'], null=True, blank=True)),
        ))
        db.send_create_signal(u'oaiharvests', ['Collection'])

        # Adding model 'Record'
        db.create_table(u'oaiharvests_record', (
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('hdr_datestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'oaiharvests', ['Record'])

        # Adding M2M table for field hdr_setSpec on 'Record'
        m2m_table_name = db.shorten_name(u'oaiharvests_record_hdr_setSpec')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm[u'oaiharvests.record'], null=False)),
            ('collection', models.ForeignKey(orm[u'oaiharvests.collection'], null=False))
        ))
        db.create_unique(m2m_table_name, ['record_id', 'collection_id'])

        # Adding M2M table for field metadata on 'Record'
        m2m_table_name = db.shorten_name(u'oaiharvests_record_metadata')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm[u'oaiharvests.record'], null=False)),
            ('metadataelement', models.ForeignKey(orm[u'oaiharvests.metadataelement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['record_id', 'metadataelement_id'])

        # Adding model 'Community'
        db.create_table(u'oaiharvests_community', (
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('repository', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oaiharvests.Repository'])),
        ))
        db.send_create_signal(u'oaiharvests', ['Community'])

        # Adding model 'Repository'
        db.create_table(u'oaiharvests_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('base_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'oaiharvests', ['Repository'])

        # Adding model 'MetadataElement'
        db.create_table(u'oaiharvests_metadataelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('element_type', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('element_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'oaiharvests', ['MetadataElement'])


    def backwards(self, orm):
        # Adding model 'HarvestedCollection'
        db.create_table(u'oaiharvests_harvestedcollection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'oaiharvests', ['HarvestedCollection'])

        # Deleting model 'Collection'
        db.delete_table(u'oaiharvests_collection')

        # Deleting model 'Record'
        db.delete_table(u'oaiharvests_record')

        # Removing M2M table for field hdr_setSpec on 'Record'
        db.delete_table(db.shorten_name(u'oaiharvests_record_hdr_setSpec'))

        # Removing M2M table for field metadata on 'Record'
        db.delete_table(db.shorten_name(u'oaiharvests_record_metadata'))

        # Deleting model 'Community'
        db.delete_table(u'oaiharvests_community')

        # Deleting model 'Repository'
        db.delete_table(u'oaiharvests_repository')

        # Deleting model 'MetadataElement'
        db.delete_table(u'oaiharvests_metadataelement')


    models = {
        u'oaiharvests.collection': {
            'Meta': {'object_name': 'Collection'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Community']", 'null': 'True', 'blank': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'oaiharvests.community': {
            'Meta': {'object_name': 'Community'},
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'repository': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Repository']"})
        },
        u'oaiharvests.metadataelement': {
            'Meta': {'object_name': 'MetadataElement'},
            'element_data': ('django.db.models.fields.TextField', [], {}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'oaiharvests.record': {
            'Meta': {'object_name': 'Record'},
            'hdr_datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'hdr_setSpec': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oaiharvests.Collection']", 'symmetrical': 'False'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oaiharvests.MetadataElement']", 'symmetrical': 'False'})
        },
        u'oaiharvests.repository': {
            'Meta': {'object_name': 'Repository'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['oaiharvests']