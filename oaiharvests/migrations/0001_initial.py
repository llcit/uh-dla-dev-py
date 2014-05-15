# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HarvestedCollection'
        db.create_table(u'oaiharvests_harvestedcollection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'oaiharvests', ['HarvestedCollection'])


    def backwards(self, orm):
        # Deleting model 'HarvestedCollection'
        db.delete_table(u'oaiharvests_harvestedcollection')


    models = {
        u'oaiharvests.harvestedcollection': {
            'Meta': {'object_name': 'HarvestedCollection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['oaiharvests']