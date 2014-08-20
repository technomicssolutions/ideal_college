from django.db import models
from django.contrib.auth.models import User

ROLE = (
	('teacher', 'Teacher'),
	('admin', 'Admin'),
	('office_staff', 'Office Staff'),
)

class Designation(models.Model):
	designation = models.CharField('Designation Name', null=True, blank=True, max_length=200,unique=True)

	def __unicode__(self):
		return str(self.designation)

	class Meta:
		verbose_name = 'Designation'
		verbose_name_plural = 'Designation'

class Staff(models.Model):
	user = models.ForeignKey(User, null=True, blank=True)
	
	staff_id = models.CharField('Staff Id',unique=True, max_length=200)
	dob = models.DateField('Date of Birth',null=True, blank=True)
	address= models.CharField('Staff Address',null=True, blank=True, max_length=200)
	mobile_number= models.CharField('Mobile Number',null=True, blank=True, max_length=200)
	land_number= models.CharField('Land Number',null=True, blank=True, max_length=200)
	
	blood_group = models.CharField('Blood Group',null=True, blank=True, max_length=200)
	doj = models.DateField('Date of Join',null=True, blank=True)
	designation = models.ForeignKey(Designation, null=True, blank=True)
	qualifications = models.CharField('Qualifications',null=True, blank=True, max_length=200)
	experiance = models.CharField('Experiance',null=True, blank=True, max_length=200)
	photo = models.ImageField(upload_to = "uploads/photos/", null=True, blank=True)
	
	role = models.CharField('Role Of The Staff',null=True, blank=True, max_length=200, choices=ROLE)
	
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
	
	reference_name = models.CharField('Reference Name',null=True, blank=True, max_length=200)
	reference_address= models.CharField('Reference Address',null=True, blank=True, max_length=200)
	reference_mobile_number= models.CharField('Reference Mobile Number',null=True, blank=True, max_length=200)
	reference_land_number= models.CharField('Reference Land Number',null=True, blank=True, max_length=200)
	reference_email = models.CharField('Reference Email',null=True, blank=True, max_length=200)

	def __unicode__(self):
		return (self.staff_id)

	class Meta:
		verbose_name = 'Staff'
		verbose_name_plural = 'Staff'





