from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from report.views import OutstandingFeesListReport, IdcardReport

urlpatterns = patterns('',
	url(r'^outstanding_fees_report/$',login_required(OutstandingFeesListReport.as_view()), name='outstanding_fees_report'),
	url(r'^id_card/$',login_required(IdcardReport.as_view()), name='id_card'),
)
