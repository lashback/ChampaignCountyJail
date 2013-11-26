# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Address.verified'
        db.delete_column(u'prisoners_address', 'verified')

        # Deleting field 'Address.attempted'
        db.delete_column(u'prisoners_address', 'attempted')


    def backwards(self, orm):
        # Adding field 'Address.verified'
        db.add_column(u'prisoners_address', 'verified',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Address.attempted'
        db.add_column(u'prisoners_address', 'attempted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'prisoners.address': {
            'Meta': {'object_name': 'Address'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_known': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'point_location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'geography': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'prisoners.booking': {
            'Meta': {'object_name': 'Booking'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'block': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'booking_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'booking_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'booking_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'booking_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'housing_facility': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prisoners.Inmate']", 'null': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'rough_release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'total_bond': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'prisoners.bookingcharge': {
            'Meta': {'object_name': 'BookingCharge'},
            'booking': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prisoners.Booking']", 'null': 'True'}),
            'charge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prisoners.Charge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prisoners.Inmate']"}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prisoners.Race']"})
        },
        u'prisoners.charge': {
            'Meta': {'object_name': 'Charge'},
            'crime_class': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'statute': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'prisoners.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'prisoners.inmate': {
            'Meta': {'object_name': 'Inmate'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prisoners.Address']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jacket_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['prisoners.Race']", 'null': 'True'})
        },
        u'prisoners.race': {
            'Meta': {'object_name': 'Race'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['prisoners']