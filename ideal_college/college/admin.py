from django.contrib import admin
from college.models import *

admin.site.register(College)
admin.site.register(Branch)
admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(Semester)
admin.site.register(QualifiedExam)
admin.site.register(TechnicalQualification)