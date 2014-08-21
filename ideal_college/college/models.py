from django.db import models

COURSE_TYPE = (
	('Distant', 'Distant'),
	('Regular', 'Regular')
)
REGISTRATION_TYPE = (
	('Registration Only', 'Registration Only'),
	('With Contact Classes', 'With Contact Classes'),
)

class College(models.Model):
	name = models.CharField('College Name', null=True, blank=True, max_length=200)
	logo = models.ImageField(upload_to = "uploads/logo/", null=True, blank=True)
	address = models.CharField('College Address', null=True, blank=True, max_length=200 )
	registration_number = models.CharField('College Registration Number', null=True, blank=True, max_length=200)
	def __unicode__(self):
		return (self.name)
	class Meta:
		verbose_name = 'College'
		verbose_name_plural = 'College'

class Branch(models.Model):
	branch = models.CharField('Branch Name', null=True, blank=True, max_length=200)
	address = models.CharField('College Address', null=True, blank=True, max_length=200)
	def __unicode__(self):
		return (self.branch)
	class Meta:
		verbose_name = 'College Branch'
		verbose_name_plural = 'College Branch'

class CourseBranch(models.Model):

	branch = models.CharField('Branch Name', null=True, blank=True, max_length=200)

	def __unicode__(self):
		return (self.branch)
	class Meta:
		verbose_name_plural = 'Branch'

class Semester(models.Model):
	semester = models.CharField('Semester Name', null=True, blank=True, max_length=200)
	def __unicode__(self):
		return (self.semester)
	class Meta:
		verbose_name = 'Semester'
		verbose_name_plural = 'Semester'
		
class Course(models.Model):
	course = models.CharField('Course Name', null=True, blank=True, max_length=200,unique=False)
	semester = models.ManyToManyField(Semester, null=True, blank=True)
	university = models.CharField('University', null=True, blank=True, max_length=200)
	course_type = models.CharField('Course type', null=True, blank=True, choices=COURSE_TYPE, max_length=200)
	registration_type = models.CharField('Registration Type', null=True, blank=True, choices=REGISTRATION_TYPE,max_length=200)
	def __unicode__(self):
		return (self.course)
	class Meta:
		verbose_name = 'Course'
		verbose_name_plural = 'Course'

class Batch(models.Model):
	course = models.ForeignKey(Course, null=True, blank=True)
	branch = models.ForeignKey(CourseBranch, null=True, blank=True)
	start_date = models.IntegerField('Start Dtae', null=True,blank=True)
	end_date = models.IntegerField('End Date', null=True,blank=True)	
	periods = models.IntegerField('Periods', null=True,blank=True)	

	def __unicode__(self):
		return str(self.start_date) + ' - ' + str(self.end_date) +( ' - ' + self.branch.branch if self.branch else '')
	class Meta:
		verbose_name = 'Batch'
		verbose_name_plural = 'Batch'

		
class QualifiedExam(models.Model):
	name = models.CharField('Qualified Exam Name', null=True, blank=True, max_length=200)
	authority = models.CharField('Authority', null=True, blank=True, max_length=200)
	def __unicode__(self):
		return (self.name)
	class Meta:
		verbose_name = 'QualifiedExam'
		verbose_name_plural = 'QualifiedExam'
		
class TechnicalQualification(models.Model):
	name = models.CharField('Technical Qualification Name', null=True, blank=True, max_length=30)
	authority = models.CharField('Authority', null=True, blank=True, max_length=30)
	def __unicode__(self):
		return (self.name)
	class Meta:
		verbose_name = 'TechnicalQualification'
		verbose_name_plural = 'TechnicalQualification'


