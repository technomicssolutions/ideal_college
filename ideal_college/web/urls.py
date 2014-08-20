from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib.auth.decorators import login_required

from web.views import *

urlpatterns = patterns('',
	
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$',  Login.as_view(), name='login'),
    url(r'logout/$', Logout.as_view(), name='logout'),
    
    url(r'^reset_password/(?P<user_id>\d+)/$', login_required(ResetPassword.as_view()), name="reset_password"),
	
)