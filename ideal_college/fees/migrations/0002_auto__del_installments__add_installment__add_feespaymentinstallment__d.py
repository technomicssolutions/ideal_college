# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Installments'
        db.delete_table(u'fees_installments')

        # Adding model 'Installment'
        db.create_table(u'fees_installment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('fine_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'fees', ['Installment'])

        # Adding model 'FeesPaymentInstallment'
        db.create_table(u'fees_feespaymentinstallment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paid_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('installment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fees.Installment'], null=True, blank=True)),
            ('paid_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fine', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal(u'fees', ['FeesPaymentInstallment'])

        # Deleting field 'FeesPayment.course'
        db.delete_column(u'fees_feespayment', 'course_id')

        # Deleting field 'FeesPayment.amount'
        db.delete_column(u'fees_feespayment', 'amount')

        # Deleting field 'FeesPayment.head'
        db.delete_column(u'fees_feespayment', 'head_id')

        # Deleting field 'FeesPayment.balance'
        db.delete_column(u'fees_feespayment', 'balance')

        # Deleting field 'FeesPayment.fine'
        db.delete_column(u'fees_feespayment', 'fine')

        # Deleting field 'FeesPayment.batch'
        db.delete_column(u'fees_feespayment', 'batch_id')

        # Adding field 'FeesPayment.fee_structure'
        db.add_column(u'fees_feespayment', 'fee_structure',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fees.FeesStructure'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field payment_installment on 'FeesPayment'
        db.create_table(u'fees_feespayment_payment_installment', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feespayment', models.ForeignKey(orm[u'fees.feespayment'], null=False)),
            ('feespaymentinstallment', models.ForeignKey(orm[u'fees.feespaymentinstallment'], null=False))
        ))
        db.create_unique(u'fees_feespayment_payment_installment', ['feespayment_id', 'feespaymentinstallment_id'])

        # Deleting field 'FeesHead.course'
        db.delete_column(u'fees_feeshead', 'course_id')

        # Deleting field 'FeesHead.head'
        db.delete_column(u'fees_feeshead', 'head')

        # Deleting field 'FeesHead.batch'
        db.delete_column(u'fees_feeshead', 'batch_id')

        # Adding field 'FeesHead.name'
        db.add_column(u'fees_feeshead', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'FeesHead.amount'
        db.add_column(u'fees_feeshead', 'amount',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2),
                      keep_default=False)

        # Adding field 'FeesHead.no_installments'
        db.add_column(u'fees_feeshead', 'no_installments',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field installments on 'FeesHead'
        db.create_table(u'fees_feeshead_installments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feeshead', models.ForeignKey(orm[u'fees.feeshead'], null=False)),
            ('installment', models.ForeignKey(orm[u'fees.installment'], null=False))
        ))
        db.create_unique(u'fees_feeshead_installments', ['feeshead_id', 'installment_id'])

        # Deleting field 'FeesStructure.head'
        db.delete_column(u'fees_feesstructure', 'head_id')

        # Deleting field 'FeesStructure.total_fees'
        db.delete_column(u'fees_feesstructure', 'total_fees')

        # Deleting field 'FeesStructure.no_installments'
        db.delete_column(u'fees_feesstructure', 'no_installments')

        # Removing M2M table for field installments on 'FeesStructure'
        db.delete_table('fees_feesstructure_installments')

        # Adding M2M table for field head on 'FeesStructure'
        db.create_table(u'fees_feesstructure_head', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feesstructure', models.ForeignKey(orm[u'fees.feesstructure'], null=False)),
            ('feeshead', models.ForeignKey(orm[u'fees.feeshead'], null=False))
        ))
        db.create_unique(u'fees_feesstructure_head', ['feesstructure_id', 'feeshead_id'])

    def backwards(self, orm):
        # Adding model 'Installments'
        db.create_table(u'fees_installments', (
            ('fine_amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'fees', ['Installments'])

        # Deleting model 'Installment'
        db.delete_table(u'fees_installment')

        # Deleting model 'FeesPaymentInstallment'
        db.delete_table(u'fees_feespaymentinstallment')

        # Adding field 'FeesPayment.course'
        db.add_column(u'fees_feespayment', 'course',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Course'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'FeesPayment.amount'
        db.add_column(u'fees_feespayment', 'amount',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2),
                      keep_default=False)

        # Adding field 'FeesPayment.head'
        db.add_column(u'fees_feespayment', 'head',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fees.FeesHead'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'FeesPayment.balance'
        db.add_column(u'fees_feespayment', 'balance',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2),
                      keep_default=False)

        # Adding field 'FeesPayment.fine'
        db.add_column(u'fees_feespayment', 'fine',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2),
                      keep_default=False)

        # Adding field 'FeesPayment.batch'
        db.add_column(u'fees_feespayment', 'batch',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Batch'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'FeesPayment.fee_structure'
        db.delete_column(u'fees_feespayment', 'fee_structure_id')

        # Removing M2M table for field payment_installment on 'FeesPayment'
        db.delete_table('fees_feespayment_payment_installment')

        # Adding field 'FeesHead.course'
        db.add_column(u'fees_feeshead', 'course',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Course'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'FeesHead.head'
        db.add_column(u'fees_feeshead', 'head',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'FeesHead.batch'
        db.add_column(u'fees_feeshead', 'batch',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['college.Batch'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'FeesHead.name'
        db.delete_column(u'fees_feeshead', 'name')

        # Deleting field 'FeesHead.amount'
        db.delete_column(u'fees_feeshead', 'amount')

        # Deleting field 'FeesHead.no_installments'
        db.delete_column(u'fees_feeshead', 'no_installments')

        # Removing M2M table for field installments on 'FeesHead'
        db.delete_table('fees_feeshead_installments')

        # Adding field 'FeesStructure.head'
        db.add_column(u'fees_feesstructure', 'head',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fees.FeesHead'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'FeesStructure.total_fees'
        db.add_column(u'fees_feesstructure', 'total_fees',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=14, decimal_places=2),
                      keep_default=False)

        # Adding field 'FeesStructure.no_installments'
        db.add_column(u'fees_feesstructure', 'no_installments',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding M2M table for field installments on 'FeesStructure'
        db.create_table(u'fees_feesstructure_installments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feesstructure', models.ForeignKey(orm[u'fees.feesstructure'], null=False)),
            ('installments', models.ForeignKey(orm[u'fees.installments'], null=False))
        ))
        db.create_unique(u'fees_feesstructure_installments', ['feesstructure_id', 'installments_id'])

        # Removing M2M table for field head on 'FeesStructure'
        db.delete_table('fees_feesstructure_head')

    models = {
        u'academic.student': {
            'Meta': {'object_name': 'Student'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Batch']", 'null': 'True', 'blank': 'True'}),
            'blood_group': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_file': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_remarks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'certificates_submitted': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doj': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'qualified_exam': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['college.QualifiedExam']", 'null': 'True', 'blank': 'True'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'roll_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'student_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'technical_qualification': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['college.TechnicalQualification']", 'null': 'True', 'blank': 'True'})
        },
        u'college.batch': {
            'Meta': {'object_name': 'Batch'},
            'batch': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.CourseBranch']", 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'college.course': {
            'Meta': {'object_name': 'Course'},
            'course': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'college.coursebranch': {
            'Meta': {'object_name': 'CourseBranch'},
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'college.qualifiedexam': {
            'Meta': {'object_name': 'QualifiedExam'},
            'authority': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'college.technicalqualification': {
            'Meta': {'object_name': 'TechnicalQualification'},
            'authority': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'})
        },
        u'fees.feeshead': {
            'Meta': {'object_name': 'FeesHead'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['fees.Installment']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'no_installments': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'fees.feespayment': {
            'Meta': {'object_name': 'FeesPayment'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fee_structure': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fees.FeesStructure']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_installment': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['fees.FeesPaymentInstallment']", 'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['academic.Student']", 'null': 'True', 'blank': 'True'})
        },
        u'fees.feespaymentinstallment': {
            'Meta': {'object_name': 'FeesPaymentInstallment'},
            'fine': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fees.Installment']", 'null': 'True', 'blank': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'paid_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'fees.feesstructure': {
            'Meta': {'object_name': 'FeesStructure'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Batch']", 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['college.Course']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'head': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['fees.FeesHead']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'fees.installment': {
            'Meta': {'object_name': 'Installment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fine_amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '14', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fees']