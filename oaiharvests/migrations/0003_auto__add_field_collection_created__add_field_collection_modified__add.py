# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Collection.created'
        db.add_column(u'oaiharvests_collection', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Collection.modified'
        db.add_column(u'oaiharvests_collection', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Record.created'
        db.add_column(u'oaiharvests_record', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Record.modified'
        db.add_column(u'oaiharvests_record', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Community.created'
        db.add_column(u'oaiharvests_community', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Community.modified'
        db.add_column(u'oaiharvests_community', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Repository.created'
        db.add_column(u'oaiharvests_repository', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Repository.modified'
        db.add_column(u'oaiharvests_repository', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding unique constraint on 'Repository', fields ['base_url']
        db.create_unique(u'oaiharvests_repository', ['base_url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Repository', fields ['base_url']
        db.delete_unique(u'oaiharvests_repository', ['base_url'])

        # Deleting field 'Collection.created'
        db.delete_column(u'oaiharvests_collection', 'created')

        # Deleting field 'Collection.modified'
        db.delete_column(u'oaiharvests_collection', 'modified')

        # Deleting field 'Record.created'
        db.delete_column(u'oaiharvests_record', 'created')

        # Deleting field 'Record.modified'
        db.delete_column(u'oaiharvests_record', 'modified')

        # Deleting field 'Community.created'
        db.delete_column(u'oaiharvests_community', 'created')

        # Deleting field 'Community.modified'
        db.delete_column(u'oaiharvests_community', 'modified')

        # Deleting field 'Repository.created'
        db.delete_column(u'oaiharvests_repository', 'created')

        # Deleting field 'Repository.modified'
        db.delete_column(u'oaiharvests_repository', 'modified')


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
        u'oaiharvests.metadataelement': {
            'Meta': {'object_name': 'MetadataElement'},
            'element_data': ('django.db.models.fields.TextField', [], {}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'oaiharvests.record': {
            'Meta': {'object_name': 'Record'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'hdr_datestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'hdr_setSpec': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oaiharvests.Collection']", 'symmetrical': 'False'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['oaiharvests.MetadataElement']", 'symmetrical': 'False'}),
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