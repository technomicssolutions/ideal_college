from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from report.views import OutstandingFeesListReport

urlpatterns = patterns('',
	url(r'^outstanding_fees_report/$',login_required(OutstandingFeesListReport.as_view()), name='outstanding_fees_report'),
)
