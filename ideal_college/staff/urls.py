from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib.auth.decorators import login_required
from staff.views import AddStaff, AddDesignation, EditDesignation, ListStaff, ViewStaffDetails, GetDesignation,\
 EditStaffDetails, DeleteStaffDetails, DeleteDesignation, IsUsernameExists

urlpatterns = patterns('',
	url(r'^add_staff/$', login_required (AddStaff.as_view()), name='add_staff'),
	# url(r'^edit_staff/$', EditStaff.as_view(), name='edit_staff'),
	url(r'^add_designation/$', login_required (AddDesignation.as_view()), name='add_designation'),
	url(r'^edit_designation/(?P<designation_id>\d+)/$', login_required (EditDesignation.as_view()), name='edit_designation'),
	url(r'^list_staff/$',login_required( ListStaff.as_view()), name='list_staff'),
	url(r'^view_staff_details/(?P<staff_id>\d+)/$',login_required( ViewStaffDetails.as_view()), name="view_staff_details"),
	url(r'^get_designation/$',login_required( GetDesignation.as_view()), name="get_designation"),
	url(r'^edit_staff_details/(?P<staff_id>\d+)/$',login_required( EditStaffDetails.as_view()), name="edit_staff_details"),
	url(r'^delete_staff_details/(?P<staff_id>\d+)/$',login_required( DeleteStaffDetails.as_view()), name="delete_staff_details"),
	url(r'^delete_designation/(?P<designation_id>\d+)/$',login_required( DeleteDesignation.as_view()), name="delete_designation"),
	
	url(r'^is_username_exists/$', login_required(IsUsernameExists.as_view()), name='is_username_exists'), 
)