from django.db import models
from college.models import Branch, Batch, Course 

DATE_RANGE_NAME = (
	('Early Payment', 'Early Payment'),
	('Standard Payment', 'Standard Payment'),
	('Late Payment', 'Late Payment')
)

class Installment(models.Model):

	name = models.CharField('Name', null=True, blank=True, max_length=200, choices=DATE_RANGE_NAME)
	start_date = models.DateField('Start Date', null=True, blank=True)
	end_date = models.DateField('End Date', null=True, blank=True)
	fine_amount = models.IntegerField('Fine Amount', null=True, blank=True)

	def __unicode__(self):

		return str(self.name)
	
	class Meta:

		verbose_name_plural = 'Installment'

class FeesHead(models.Model):
	
	name = models.CharField('Head Name', max_length=200, null=True, blank=True)
	amount = models.DecimalField('Amount', max_digits=14, decimal_places=2, default=0)

	def __unicode__(self):

		return str(self.name)
	
	class Meta:

		verbose_name_plural = 'Fees Head'

class FeesStructureHead(models.Model):
	
	name = models.CharField('Head Name', max_length=200, null=True, blank=True)
	amount = models.DecimalField('Amount', max_digits=14, decimal_places=2, default=0)
	installments = models.ManyToManyField(Installment, null=True, blank=True)

	def __unicode__(self):

		return str(self.name)
	
	class Meta:

		verbose_name_plural = 'Fees Structure Head'


class FeesStructure(models.Model):
	course = models.ForeignKey(Course, null=True, blank=True)
	batch = models.ForeignKey(Batch, null=True, blank=True)
	head = models.ManyToManyField(FeesStructureHead, null=True, blank=True)
	
	def __unicode__(self):

		return str(self.course.course) + ' - ' + str(self.batch.start_date) + ' - ' + str(self.batch.end_date)  
	
	class Meta:

		verbose_name_plural = 'Fees Structure'
from academic.models import Student

# class FeesPaymentInstallment(models.Model):
# 	student = models.ForeignKey(Student, null=True, blank=True)
# 	total_amount = models.DecimalField('Total Amount', max_digits=14, decimal_places=2, default=0)
# 	installment = models.ForeignKey(Installment, null=True, blank=True)
# 	paid_date = models.DateField('Paid Date', null=True, blank=True)
# 	paid_amount = models.DecimalField('Amount', max_digits=14, decimal_places=2, default=0)
# 	installment_amount = models.DecimalField('Installment Amount', max_digits=14, decimal_places=2, default=0)
# 	installment_fine = models.DecimalField('Installment Fine Amount', max_digits=14, decimal_places=2, default=0)

# 	def __unicode__(self):

# 		return str(self.total_amount)

# 	class Meta:

# 		verbose_name_plural = 'Fees Payment Installment'

class FeesPaymentHead(models.Model):
	student = models.ForeignKey(Student, null=True, blank=True)
	fees_head = models.ForeignKey(FeesStructureHead, null=True, blank=True)
	installment = models.ForeignKey(Installment, null=True, blank=True)
	total_amount = models.DecimalField('Total Amount', max_digits=14, decimal_places=2, default=0)
	# fine = models.DecimalField('Fine Amount', max_digits=14, decimal_places=2, default=0)
	paid_date = models.DateField('Paid Date', null=True, blank=True)
	
	def __unicode__(self):

		return str(self.total_amount)

	class Meta:

		verbose_name_plural = 'Fees Payment Head'


class FeesPayment(models.Model):
	
	fee_structure = models.ForeignKey(FeesStructure, null=True, blank=True)
	student = models.ForeignKey(Student, null=True, blank=True)
	# payment_installment = models.ManyToManyField(FeesPaymentInstallment, null=True, blank=True)
	payment_heads = models.ManyToManyField(FeesPaymentHead, null=True, blank=True)
	
	def __unicode__(self):
		return str(self.fee_structure)

	class Meta:

		verbose_name_plural = 'Fees Payment'

class CommonFeesPayment(models.Model):

	student = models.ForeignKey(Student, null=True, blank=True)
	head = models.ForeignKey(FeesHead, null=True, blank=True)
	paid_date = models.DateField('Paid Date', null=True, blank=True)
	paid_amount = models.DecimalField('Paid Amount', max_digits=14, decimal_places=2, default=0)

	def __unicode__(self):
		return str(self.student.student_name) + ' - '+ str(self.head.name)

	class Meta:
		verbose_name_plural = 'Common Fees Payment'