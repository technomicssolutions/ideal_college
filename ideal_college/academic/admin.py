from django.contrib import admin
from academic.models import *

class StudentAdmin(admin.ModelAdmin):
	search_fields = ['course__course']

admin.site.register(Student, StudentAdmin)
admin.site.register(StudentFees)
