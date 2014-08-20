import sys
import simplejson
import ast
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from college.models import *
from academic.models import Student


class ListCollege(View):
    def get(self, request, *args, **kwargs):

        colleges = College.objects.all()
        
        ctx = {
            'colleges': colleges
        }
        return render(request, 'college/college.html',ctx)

class ListBranch(View):
    def get(self, request, *args, **kwargs):

        branches = Branch.objects.all()
        ctx = {
            'branches': branches
        }
        return render(request, 'college/branch.html',ctx)

class ListBatch(View):
    def get(self, request, *args, **kwargs):

        batches = Batch.objects.all()
        
        ctx = {
            'batches': batches
        }
        return render(request, 'college/batch.html',ctx)

class ListCourse(View):
    def get(self, request, *args, **kwargs):

        courses = Course.objects.all()
        ctx = {
            'courses': courses
        }
        if request.is_ajax():
            course_list = []
            for course in courses:
                course_list.append({
                    'course': course.course, 
                    'id': course.id                
                })
            res = {
                'result': 'ok',
                'courses': course_list,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        return render(request, 'college/course.html',ctx)

class ListSemester(View):
    def get(self, request, *args, **kwargs):

        semesters = Semester.objects.all()
        ctx_semester_data = []
        status = 200
        if request.is_ajax():
            for semester in semesters:
                ctx_semester_data.append({
                    'id': semester.id,
                    'semester': semester.semester,
                })
            res = {
                'result': 'ok',
                'semesters': ctx_semester_data,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        
        ctx = {
            'semesters': semesters
        }
        return render(request, 'college/semester.html',ctx)

class NewCollegeAdd(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:                
                college, created = College.objects.get_or_create(name=request.POST['college_name'])
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'College already existing'
                    }
                    status_code = 500
                else:
                    try:
                        college.name = request.POST['college_name']
                        college.address = request.POST['college_name']
                        college.registration_number = request.POST['registration_number']
                                  
                    except Exception as ex:
                        print str(ex), "Exception ===="
                    college.save()
                    res = {
                        'result': 'ok',
                    }  
                    status_code = 200 
            except Exception as ex:
                print str(ex), "Exception ===="
                res = {
                        'result': 'error',
                        'message': 'College Name already existing'
                    }
                status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class EditCollege(View):

    def get(self, request, *args, **kwargs):
        college_id = kwargs['college_id']
        context = {
            'college_id': college_id,
        }
        ctx_college_data = []
        if request.is_ajax():
            try:
                college = College.objects.get(id = college_id)
                ctx_college_data.append({
                    'college_name': college.name,
                    'address': college.address,
                    'registration_number': college.registration_number,                    
                })
                res = {
                    'result': 'ok',
                    'college': ctx_college_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                ctx_college_data = []
                res = {
                    'result': 'error',
                    'college': ctx_college_data,
                }
                status = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'college/edit_college.html',context)

    def post(self, request, *args, **kwargs):

        college_id = kwargs['college_id']
        college = College.objects.get(id = college_id)
        college_data = ast.literal_eval(request.POST['college'])
        try:
            college.name = college_data['college_name']
            college.address = college_data['address']
            college.registration_number = college_data['registration_number']
            college.save()
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print "Exception == ", str(Ex)
            res = {
                'result': 'error',
                'message': 'College with this name is already existing'
            }
            status = 500
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')


class EditBatch(View): 

    def get(self, request, *args, **kwargs):
        batch_id = kwargs['batch_id']
        context = {
            'batch_id': batch_id,
        }
        ctx_data = []
        if request.is_ajax():
            try:
                batch = Batch.objects.get(id = batch_id)
                ctx_data.append({
                    'course':batch.course.course,
                    'branch':batch.branch.branch if batch.branch else '',                  
                    'batch_start':batch.start_date,
                    'batch_end':batch.end_date,
                    'batch_periods':batch.periods,                                        
                })
                res = {
                    'result': 'ok',
                    'batch': ctx_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                res = {
                    'result': 'error: ' + str(ex),
                    'batch': ctx_data,
                }
                status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'college/edit_batch.html',context)

    def post(self, request, *args, **kwargs):        
        batch_id = kwargs['batch_id']
        batch = Batch.objects.get(id = batch_id)
        data = ast.literal_eval(request.POST['batch'])
        try:
            batch.start_date = data['batch_start']
            batch.end_date = data['batch_end']
            batch.periods = data['batch_periods']
            batch.save()
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print "Exception == ", str(Ex)
            res = {
                'result': 'error: '+ str(Ex),
                'message': 'Batch with this name is already existing'
            }
            status = 500
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class EditCourse(View):

    def get(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        context = {
            'course_id': course_id,
        }
        ctx_data = []
        semester_set = []
        if request.is_ajax():
            try:
                course = Course.objects.get(id = course_id)
                semester_list = course.semester.all()
                for semester in semester_list:
                    semester_set.append({
                        'semester_id': semester.id,
                        'semester_name': semester.semester,
                    })
                ctx_data.append({
                    'course': course.course,
                    'semester_details': semester_set,                                                        
                })
                res = {
                    'result': 'ok',
                    'course': ctx_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                res = {
                    'result': 'error: '+ str(ex),
                    'course': ctx_data,
                }
                status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        return render(request, 'college/edit_course.html',context)

    def post(self, request, *args, **kwargs):

        course_id = kwargs['course_id']        
        course = Course.objects.get(id = course_id)
        data = ast.literal_eval(request.POST['course'])     
        semester_details = ast.literal_eval(request.POST['semester_list']) 
        try:
            course.course = data['course']
            course.save()
            semester_remove = course.semester.all();
            for semester_id in semester_remove:              
                course.semester.remove(semester_id)
            for semester_id in semester_details:               
                semester = Semester.objects.get(id = semester_id)              
                course.semester.add(semester)
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print "Exception == ", str(Ex)
            res = {
                'result': 'error',
                'message': 'Course with this name is already existing'
            }
            status = 200
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class EditBranch(View):

    def get(self, request, *args, **kwargs):
        branch_id = kwargs['branch_id']
        context = {
            'branch_id': branch_id,
        }
        ctx_data = []
        if request.is_ajax():
            try:
                branch = Branch.objects.get(id = branch_id)
                ctx_data.append({
                    'branch': branch.branch,
                    'address': branch.address,
                })
                res = {
                    'result': 'ok',
                    'branch': ctx_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                res = {
                    'result': 'error: '+ str(ex),
                    'branch': ctx_data,
                }
                status = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        return render(request, 'college/edit_branch.html',context)

    def post(self, request, *args, **kwargs):

        branch_id = kwargs['branch_id']

        branch = Branch.objects.get(id = branch_id)
        data = ast.literal_eval(request.POST['branch'])
        try:
            branch.branch = data['branch']
            branch.address = data['address']
            branch.save()
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print "Exception == ", str(Ex)
            res = {
                'result': 'error',
                'message': 'Branch with this name is already existing'
            }
            status = 500
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')


class EditSemester(View):

    def get(self, request, *args, **kwargs):
        semester_id = kwargs['semester_id']
        context = {
            'semester_id': semester_id,
        }
        ctx_data = []
        if request.is_ajax():
            try:
                semester = Semester.objects.get(id = semester_id)
                ctx_data.append({
                    'semester': semester.semester,
                    
                                        
                })
                res = {
                    'result': 'ok',
                    'semester': ctx_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                ctx_college_data = []
                res = {
                    'result': 'error',
                    'semester': ctx_data,
                }
                status = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        return render(request, 'college/edit_semester.html',context)

    def post(self, request, *args, **kwargs):

        semester_id = kwargs['semester_id']

        semester = Semester.objects.get(id = semester_id)
        data = ast.literal_eval(request.POST['semester'])
        try:
            semester.semester = data['semester']
            semester.save()
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print "Exception == ", str(Ex)
            res = {
                'result': 'error',
                'message': 'Semester with this name is already existing'
            }
            status = 200
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')


class AddNewBranch(View):
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            try:
                
                branch, created = Branch.objects.get_or_create(branch=request.POST['name'])
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Branch already existing'
                    }
                    status_code = 500
                else:
                    try:
                        branch.branch = request.POST['name']
                        branch.address = request.POST['address']
                        
                    except Exception as ex:
                        print str(ex), "Exception ===="
                    branch.save()
                    res = {
                        'result': 'ok',
                    }  
                    status_code = 200 

            except Exception as ex:
                print str(ex), "Exception ===="
                res = {
                        'result': 'error',
                        'message': 'Branch Name already existing'
                    }
                status_code = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class AddNewBatch(View):
    def post(self, request, *args, **kwargs):
        status_code = 200
        if request.is_ajax():
            try:
                course = Course.objects.get(id = request.POST['course'])
                if request.POST['branch']:
                    branch = CourseBranch.objects.get(id = request.POST['branch'])
                    batch, created = Batch.objects.get_or_create(course=course, start_date=request.POST['batch_start'],end_date=request.POST['batch_end'],periods=request.POST['periods'],branch=branch)
                else:
                    batch, created = Batch.objects.get_or_create(course=course, start_date=request.POST['batch_start'],end_date=request.POST['batch_end'],periods=request.POST['periods'])
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Batch already exist'
                    }
                else:
                    batch.save()
                    res = {
                        'result': 'ok',
                    }  
            except Exception as ex:
                print str(ex), "Exception ===="
                res = {
                        'result': 'error: '+ str(ex),
                        'message': 'Batch Name already exist'
                    }
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class AddNewCourse(View):
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            semester_list = ast.literal_eval(request.POST['semester_list'])
            try:
        
                course, created = Course.objects.get_or_create(course=request.POST['course'])
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Course already existing'
                    }
                    status_code = 200
                else:
                    try:
                        course = Course.objects.get(id = request.POST['course'])
                    
                    except Exception as ex:
                        print str(ex), "Exception ===="
                    course.save()
                    for semester_id in semester_list:
                        course.semester.add(semester_id)
                    res = {
                        'result': 'ok',
                    }  
                    status_code = 200 

            except Exception as ex:
                print str(ex), "Exception ===="
                res = {
                        'result': 'error: ' + str(ex),
                        'message': 'Course Name already existing'
                    }
                status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class AddNewSemester(View):
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            try:

                semester, created = Semester.objects.get_or_create(semester=request.POST['name'])
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Semester already existing'
                    }
                    status_code = 500
                else:
                    try:
                        semester.semester = request.POST['name']
                    
                    except Exception as ex:
                        print str(ex), "Exception ===="
                    semester.save()
                    res = {
                        'result': 'ok',
                    }  
                    status_code = 200 

            except Exception as ex:
                print str(ex), "Exception ===="
                res = {
                        'result': 'error',
                        'message': 'Semester Name already existing'
                    }
                status_code = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")


class DeleteCollege(View):
    def get(self, request, *args, **kwargs):

        college_id = kwargs['college_id']       
        college = College.objects.filter(id=college_id)                          
        college.delete()
        return HttpResponseRedirect(reverse('list_college'))
class DeleteBranch(View):
    def get(self, request, *args, **kwargs):

        branch_id = kwargs['branch_id']       
        branch = Branch.objects.filter(id=branch_id)                          
        branch.delete()
        return HttpResponseRedirect(reverse('list_branch'))


class DeleteBatch(View):
    def get(self, request, *args, **kwargs):

        batch_id = kwargs['batch_id']       
        batch = Batch.objects.filter(id=batch_id)                          
        batch.delete()
        return HttpResponseRedirect(reverse('list_batch'))

class DeleteCourse(View):
    def get(self, request, *args, **kwargs):

        course_id = kwargs['course_id']       
        course = Course.objects.filter(id=course_id)                          
        course.delete()
        return HttpResponseRedirect(reverse('list_course'))

class DeleteSemester(View):
    def get(self, request, *args, **kwargs):

        semester_id = kwargs['semester_id']       
        semester = Semester.objects.filter(id=semester_id)                          
        semester.delete()
        return HttpResponseRedirect(reverse('list_semester'))

class BranchList(View):

    def get(self, request, *args, **kwargs):

        branch_list = CourseBranch.objects.all().order_by('branch')
        status = 200
        ctx_branch = []
        if request.is_ajax():
            for branch in branch_list:
                ctx_branch.append({
                    'branch': branch.branch,
                    'id': branch.id
                })
            res = {
                'branch_list': ctx_branch,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        context = {
            'branch_list': branch_list,
        }
        return render(request, 'college/branch_list.html', context)

class SaveBranch(View):

    def post(self, request, *args, **kwargs):

        status = 200
        branch_name = request.POST['branch_name']
        branch_id = request.POST['branch_id']
        if branch_id:
            branch = CourseBranch.objects.get(id=branch_id)
            try:
                branch.branch = branch_name
                branch.save()
                res = {
                    'result': 'ok',
                }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': 'Branch name already existing'
                }
        else:
            try:
                branch = CourseBranch.objects.get(branch=branch_name)
                res = {
                    'result': 'error',
                    'message': 'Branch name already existing',
                }
            except Exception as ex:
                print str(ex)

                branch = CourseBranch.objects.create(branch=branch_name)

                res = {
                    'result': 'ok',
                }

        response = simplejson.dumps(res)

        return HttpResponse(response, status=status, mimetype='application/json')

class EditCourseBranch(View):

    def get(self, request, *args, **kwargs):

        branch_id = kwargs['branch_id']
        status = 200
        branch = CourseBranch.objects.get(id=branch_id)
        if request.is_ajax():
            res = {
                'result': 'ok',
                'branch_id': branch.id,
                'branch_name': branch.branch
            }

            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        context = {
            'branch_id': branch.id,
        }
        return render(request, 'college/edit_cource_branch.html', context)

class DeleteCourseBranch(View):

    def get(self, request, *args, **kwargs):

        branch_id = kwargs['branch_id']

        branch = CourseBranch.objects.get(id=branch_id)

        branch.delete()

        return HttpResponseRedirect(reverse('branch_list'))

class GetBranch(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                branches = Branch.objects.all()
                branch_list = []
                for branch in branches:
                    branch_list.append({
                        'branch': branch.branch, 
                        'id': branch.id                
                    })
                res = {
                    'result': 'ok',
                    'branches': branch_list,
                }
            except Exception as ex:
                res = {
                    'result': 'error: '+ str(ex)
                }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class GetBatch(View):
    def get(self, request, *args, **kwargs):
        
        if request.is_ajax():
            try:
                course_id = kwargs['id']
                batches = Batch.objects.filter(course=course_id)
                batch_list = []
                for batch in batches:
                    batch_list.append({
                        'start_date':batch.start_date,
                        'end_date':batch.end_date,
                        'id': batch.id,
                        'branch': batch.branch.branch if batch.branch else '',   
                        'name': str(batch.start_date) + '-' + str(batch.end_date) + ' ' + (str(batch.branch) if batch.branch else ''),
                    })
                res = {
                    'result': 'ok',
                    'batches': batch_list,
                }
            except Exception as ex:
                res = {
                    'result': 'error'+ str(ex)
                }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class GetSemester(View):

    def get(self, request, *args, **kwargs):        
        semester_list = []
        if request.is_ajax():
            try:
                course = Course.objects.get(id=request.GET.get('id'))
                semesters = course.semester.all()
            except:
                try:
                    semesters = Semester.objects.all()
                except Exception as ex:
                    res = {
                        'result': 'error: '+ str(ex),
                    }
            for semester in semesters:
                semester_list.append({
                    'semester': semester.semester, 
                    'id': semester.id                
                })
            res = {
                'result': 'ok',
                'semesters': semester_list,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

