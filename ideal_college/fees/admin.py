from django.contrib import admin
from fees.models import *

admin.site.register(FeesPayment)
admin.site.register(FeesStructure)
admin.site.register(FeesStructureHead)
admin.site.register(FeesHead)
admin.site.register(Installment)
admin.site.register(FeesPaymentInstallment)
admin.site.register(CommonFeesPayment)
