from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from report.views import OutstandingFeesListReport, IdcardReport, CommonFeeReport

urlpatterns = patterns('',
	url(r'^outstanding_fees_report/$',login_required(OutstandingFeesListReport.as_view()), name='outstanding_fees_report'),
	url(r'^id_card/$',login_required(IdcardReport.as_view()), name='id_card'),
	url(r'^common_fee_report/$',login_required(CommonFeeReport.as_view()), name='common_fee_report'),
)
