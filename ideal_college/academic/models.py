
from django.db import models
from college.models import Course, Batch, QualifiedExam, TechnicalQualification


class Student(models.Model):
	student_name = models.CharField('Student Name', null=True, blank=True, max_length=200)
	roll_number = models.IntegerField('Roll Number', default=0, null=True, blank=True)
	address = models.CharField('Student Address', null=True, blank=True, max_length=200 )
	course = models.ForeignKey(Course, null=True, blank=True)
	batch = models.ForeignKey(Batch, null=True, blank=True)
	qualified_exam = models.ManyToManyField(QualifiedExam, null=True, blank=True)
	technical_qualification = models.ManyToManyField(TechnicalQualification, null=True, blank=True)
	dob = models.DateField('Date of Birth',null=True, blank=True)
	address= models.CharField('Student Address',null=True, blank=True, max_length=200)
	mobile_number= models.CharField('Mobile Number',null=True, blank=True, max_length=200)
	land_number= models.CharField('Land Number',null=True, blank=True, max_length=200)
	email = models.CharField('Email',null=True, blank=True, max_length=200)
	blood_group = models.CharField('Blood Group',null=True, blank=True, max_length=200)
	doj = models.DateField('Date of Join',null=True, blank=True)
	photo = models.ImageField(upload_to = "uploads/photos/", null=True, blank=True)
	certificates_submitted = models.CharField('Certificates',null=True, blank=True, max_length=200)
	certificates_remarks = models.CharField('Remarks',null=True, blank=True, max_length=200)
	certificates_file = models.CharField('File Number',null=True, blank=True, max_length=200)
	id_proofs_submitted = models.CharField('Id Proofs',null=True, blank=True, max_length=200)
	id_proofs_remarks = models.CharField('Remarks',null=True, blank=True, max_length=200)
	id_proofs_file = models.CharField('File Number',null=True, blank=True, max_length=200)
	guardian_name = models.CharField('Guardian Name',null=True, blank=True, max_length=200)
	guardian_address= models.CharField('Guardian Address',null=True, blank=True, max_length=200)
	relationship = models.CharField('Relationship',null=True, blank=True, max_length=200)
	guardian_mobile_number= models.CharField('Guardian Mobile Number',null=True, blank=True, max_length=200)
	guardian_land_number= models.CharField('Guardian Land Number',null=True, blank=True, max_length=200)
	guardian_email = models.CharField('Guardian Email',null=True, blank=True, max_length=200)

	def __unicode__(self):
		return str(self.student_name)
		
	class Meta:
		verbose_name = 'Student'
		verbose_name_plural = 'Student'

