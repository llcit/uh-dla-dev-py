# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HarvestRegistration.harvest_date'
        db.add_column(u'oaiharvests_harvestregistration', 'harvest_date',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 27, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HarvestRegistration.harvest_date'
        db.delete_column(u'oaiharvests_harvestregistration', 'harvest_date')


    models = {
        u'oaiharvests.collection': {
            'Meta': {'object_name': 'Collection'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Community']", 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256', 'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
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
            'harvest_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'oaiharvests.metadataelement': {
            'Meta': {'object_name': 'MetadataElement'},
            'element_data': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oaiharvests.Record']", 'null': 'True'})
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