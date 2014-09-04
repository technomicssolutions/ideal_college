from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf import settings

from academic.views import GetStudent, AddStudent, ListStudent, ViewStudentDetails, EditStudentDetails, \
DeleteStudentDetails, CheckUidExists, SearchStudent, ConductCertificate

urlpatterns = patterns('',
	url(r'^get_student/(?P<course_id>\d+)/(?P<batch_id>\d+)/$',login_required(GetStudent.as_view()), name="get_student"),
	url(r'^add_student/$',login_required (AddStudent.as_view()), name='add_student'),
	url(r'^list_student/$',login_required (ListStudent.as_view()), name='list_student'),
	url(r'^view_student_details/(?P<student_id>\d+)/$',login_required (ViewStudentDetails.as_view()), name="view_student_details"),
	url(r'^edit_student_details/(?P<student_id>\d+)/$',login_required (EditStudentDetails.as_view()), name="edit_student_details"),
	url(r'^delete_student_details/(?P<student_id>\d+)/$',login_required (DeleteStudentDetails.as_view()), name="delete_student_details"),
	url(r'^check_student_uid_exists/$', login_required(CheckUidExists.as_view()), name="check_student_uid_exists"),
	url(r'^student_search/$', login_required(SearchStudent.as_view()), name="student_search"),
	url(r'^conduct_certifcate/$', login_required(ConductCertificate.as_view()), name="conduct_certifcate"),
)