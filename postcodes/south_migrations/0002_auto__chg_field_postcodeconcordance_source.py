# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'PostcodeConcordance.source'
        db.alter_column('postcodes_postcodeconcordance', 'source', self.gf('django.db.models.fields.CharField')(max_length=30))


    def backwards(self, orm):
        
        # Changing field 'PostcodeConcordance.source'
        db.alter_column('postcodes_postcodeconcordance', 'source', self.gf('django.db.models.fields.CharField')(max_length=20))


    models = {
        'postcodes.postcode': {
            'Meta': {'object_name': 'Postcode'},
            'centroid': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        'postcodes.postcodeconcordance': {
            'Meta': {'unique_together': "(('code', 'boundary'),)", 'object_name': 'PostcodeConcordance'},
            'boundary': ('django.db.models.fields.TextField', [], {}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postcodes.Postcode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['postcodes']
