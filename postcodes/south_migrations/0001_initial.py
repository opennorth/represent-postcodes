# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Postcode'
        db.create_table('postcodes_postcode', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6, primary_key=True)),
            ('centroid', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
        ))
        db.send_create_signal('postcodes', ['Postcode'])

        # Adding model 'PostcodeConcordance'
        db.create_table('postcodes_postcodeconcordance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postcodes.Postcode'])),
            ('boundary', self.gf('django.db.models.fields.TextField')()),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('postcodes', ['PostcodeConcordance'])

        # Adding unique constraint on 'PostcodeConcordance', fields ['code', 'boundary']
        db.create_unique('postcodes_postcodeconcordance', ['code_id', 'boundary'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'PostcodeConcordance', fields ['code', 'boundary']
        db.delete_unique('postcodes_postcodeconcordance', ['code_id', 'boundary'])

        # Deleting model 'Postcode'
        db.delete_table('postcodes_postcode')

        # Deleting model 'PostcodeConcordance'
        db.delete_table('postcodes_postcodeconcordance')


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
            'source': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['postcodes']
