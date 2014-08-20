# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Designation'
        db.create_table(u'staff_designation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'staff', ['Designation'])

        # Adding model 'Staff'
        db.create_table(u'staff_staff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('staff_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('land_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('blood_group', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('doj', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('designation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['staff.Designation'], null=True, blank=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('qualifications', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('experiance', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('certificates_submitted', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('certificates_remarks', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('certificates_file', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('id_proofs_submitted', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('id_proofs_remarks', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('id_proofs_file', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('guardian_address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('guardian_mobile_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('guardian_land_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('guardian_email', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('reference_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('reference_address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('reference_mobile_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('reference_land_number', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('reference_email', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'staff', ['Staff'])

    def backwards(self, orm):
        # Deleting model 'Designation'
        db.delete_table(u'staff_designation')

        # Deleting model 'Staff'
        db.delete_table(u'staff_staff')

    models = {
        u'staff.designation': {
            'Meta': {'object_name': 'Designation'},
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'staff.staff': {
            'Meta': {'object_name': 'Staff'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'blood_group': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_file': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_remarks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_submitted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'designation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['staff.Designation']", 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doj': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'experiance': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_land_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_proofs_file': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id_proofs_remarks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id_proofs_submitted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'land_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qualifications': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'reference_address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'reference_email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'reference_land_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'reference_mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'reference_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'staff_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'staff_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['staff']