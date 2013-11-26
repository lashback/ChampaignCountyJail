# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Charge'
        db.create_table(u'prisoners_charge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('statute', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('crime_class', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'prisoners', ['Charge'])

        # Adding model 'Race'
        db.create_table(u'prisoners_race', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'prisoners', ['Race'])

        # Adding model 'City'
        db.create_table(u'prisoners_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'prisoners', ['City'])

        # Adding model 'Address'
        db.create_table(u'prisoners_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('attempted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_known', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('point_location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, geography=True)),
        ))
        db.send_create_signal(u'prisoners', ['Address'])

        # Adding model 'Inmate'
        db.create_table(u'prisoners_inmate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('jacket_number', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prisoners.Race'], null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6, null=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prisoners.Address'], null=True, blank=True)),
        ))
        db.send_create_signal(u'prisoners', ['Inmate'])

        # Adding model 'Booking'
        db.create_table(u'prisoners_booking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time_created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('identity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prisoners.Inmate'], null=True)),
            ('booking_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('booking_time', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('rough_release_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('booking_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('booking_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('housing_facility', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_bond', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
        ))
        db.send_create_signal(u'prisoners', ['Booking'])

        # Adding model 'BookingCharge'
        db.create_table(u'prisoners_bookingcharge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prisoners.Inmate'])),
            ('booking', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prisoners.Booking'], null=True)),
            ('charge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prisoners.Charge'])),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prisoners.Race'])),
        ))
        db.send_create_signal(u'prisoners', ['BookingCharge'])


    def backwards(self, orm):
        # Deleting model 'Charge'
        db.delete_table(u'prisoners_charge')

        # Deleting model 'Race'
        db.delete_table(u'prisoners_race')

        # Deleting model 'City'
        db.delete_table(u'prisoners_city')

        # Deleting model 'Address'
        db.delete_table(u'prisoners_address')

        # Deleting model 'Inmate'
        db.delete_table(u'prisoners_inmate')

        # Deleting model 'Booking'
        db.delete_table(u'prisoners_booking')

        # Deleting model 'BookingCharge'
        db.delete_table(u'prisoners_bookingcharge')


    models = {
        u'prisoners.address': {
            'Meta': {'object_name': 'Address'},
            'attempted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_known': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'point_location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'geography': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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