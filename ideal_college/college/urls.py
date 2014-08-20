
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from college.views import *

urlpatterns = patterns('',
	url(r'^list_college/$',login_required (ListCollege.as_view()), name='list_college'),
	url(r'^list_branch/$',login_required (ListBranch.as_view()), name='list_branch'),
	url(r'^list_batch/$',login_required (ListBatch.as_view()), name='list_batch'),
	url(r'^list_course/$',login_required (ListCourse.as_view()), name='list_course'),
	url(r'^list_semester/$',login_required (ListSemester.as_view()), name='list_semester'),
	url(r'^add_new_college/$',login_required (NewCollegeAdd.as_view()), name='add_new_college'),
	url(r'^add_new_branch/$',login_required (AddNewBranch.as_view()), name='add_new_branch'),
	url(r'^add_new_batch/$',login_required (AddNewBatch.as_view()), name='add_new_batch'),
	url(r'^add_new_course/$',login_required (AddNewCourse.as_view()), name='add_new_course'),
	url(r'^add_new_semester/$',login_required (AddNewSemester.as_view()), name='add_new_semester'),
	url(r'^edit_college/(?P<college_id>\d+)/$',login_required (EditCollege.as_view()), name="edit_college"),
	url(r'^delete_college/(?P<college_id>\d+)/$',login_required (DeleteCollege.as_view()), name="delete_college"),
	url(r'^edit_branch/(?P<branch_id>\d+)/$',login_required (EditBranch.as_view()), name="edit_branch"),
	url(r'^delete_branch/(?P<branch_id>\d+)/$',login_required (DeleteBranch.as_view()), name="delete_branch"),
	url(r'^edit_batch/(?P<batch_id>\d+)/$',login_required (EditBatch.as_view()), name="edit_batch"),
	url(r'^delete_batch/(?P<batch_id>\d+)/$',login_required (DeleteBatch.as_view()), name="delete_batch"),
	url(r'^edit_course/(?P<course_id>\d+)/$',login_required (EditCourse.as_view()), name="edit_course"),
	url(r'^delete_course/(?P<course_id>\d+)/$',login_required (DeleteCourse.as_view()), name="delete_course"),
	url(r'^edit_semester/(?P<semester_id>\d+)/$',login_required (EditSemester.as_view()), name="edit_semester"),
	url(r'^delete_semester/(?P<semester_id>\d+)/$',login_required (DeleteSemester.as_view()), name="delete_semester"),
	url(r'^save_new_branch/$', login_required(SaveBranch.as_view()), name='save_new_branch'),
	url(r'^branch_list/$', login_required(BranchList.as_view()), name='branch_list'),
	url(r'^edit_course_branch/(?P<branch_id>\d+)/$', login_required(EditCourseBranch.as_view()), name="edit_course_branch"),
	url(r'^delete_course_branch/(?P<branch_id>\d+)/$', login_required(DeleteCourseBranch.as_view()), name="delete_course_branch"),
    url(r'^get_branch/$',login_required (GetBranch.as_view()), name="get_branch"),
    url(r'^get_batch/(?P<id>\d+)/$',login_required (GetBatch.as_view()), name="get_batch"),
    url(r'^get_semester/$',login_required (GetSemester.as_view()), name="get_semester"),  

)