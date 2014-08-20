
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'', include('web.urls')),
	url(r'^college/', include('college.urls')),
	url(r'^academic/', include('academic.urls')),
	url(r'^staff/', include('staff.urls')),
	url(r'^fees/', include('fees.urls')),
	url(r'^exam/', include('exam.urls')),

	url(r'^attendance/', include('attendance.urls')),
	url(r'^report/', include('report.urls')),
	url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

)