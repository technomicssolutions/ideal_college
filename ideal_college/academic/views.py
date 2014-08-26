import simplejson
import ast
from datetime import datetime

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from college.models import Course, Branch, Batch, Semester, QualifiedExam, TechnicalQualification
from academic.models import Student
from fees.models import FeesStructureHead

class AddStudent(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            print request.POST
            try:
                course = Course.objects.get(id = request.POST['course'])
                batch = Batch.objects.get(id = request.POST['batch'])
                student, created = Student.objects.get_or_create(roll_number = request.POST['roll_number'], course=course, batch=batch)
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Student with this roll no already existing'
                    }
                else:
                    try:
                        qualified_exams = request.POST['qualified_exam'].split(',')
                        technical_exams = request.POST['technical_qualification'].split(',')
                        student.student_name = request.POST['student_name']
                        student.roll_number = request.POST['roll_number']
                        student.address = request.POST['address']
                        student.course=course
                        student.batch=batch
                        for exam in qualified_exams:
                            qualified_exam, created = QualifiedExam.objects.get_or_create(name=exam)
                            student.qualified_exam.add(qualified_exam)

                        for technical_exam in technical_exams:
                            tech_exam, created = TechnicalQualification.objects.get_or_create(name=technical_exam)
                            student.technical_qualification.add(tech_exam)
                    
                        student.dob = datetime.strptime(request.POST['dob'], '%d/%m/%Y')
                        student.address = request.POST['address']
                        student.mobile_number = request.POST['mobile_number']
                        student.land_number = request.POST['land_number']
                        student.email = request.POST['email']
                        student.blood_group = request.POST['blood_group']
                        student.doj = datetime.strptime(request.POST['doj'], '%d/%m/%Y')
                        student.photo = request.FILES.get('photo_img', '')                       
                        student.certificates_submitted = request.POST['certificates_submitted']
                        student.certificates_remarks = request.POST['certificates_remarks']
                        student.certificates_file = request.POST['certificates_file']
                        student.id_proofs_submitted = request.POST['id_proofs_submitted']
                        student.id_proofs_remarks = request.POST['id_proofs_remarks']
                        student.id_proofs_file = request.POST['id_proofs_file']
                        student.guardian_name = request.POST['guardian_name']
                        student.guardian_address = request.POST['guardian_address']
                        student.relationship = request.POST['relationship']
                        student.guardian_mobile_number = request.POST['guardian_mobile_number']
                        student.guardian_land_number = request.POST['guardian_land_number']
                        student.guardian_email = request.POST['guardian_email']  
                        student.save()
                        fees_heads = ast.literal_eval(request.POST['applicable_fee_heads']) 
                        for fee_head in fees_heads:
                            fees_head = FeesStructureHead.objects.get(id=fee_head) 
                            try:
                                student.applicable_fees_heads.add(fees_head) 
                            except Exception as ex:
                                print str(ex) 
                        student.save()
                    except Exception as ex:
                        print str(ex)
                        res = {
                            'result': 'error',
                            'message': str(ex)
                        }
                    
                    res = {
                        'result': 'ok',
                    }                     
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': str(ex)
                }
            status_code = 200 
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")
        return render(request, 'academic/list_student.html', {})

class ListStudent(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('batch_id', ''):
            students = Student.objects.filter(batch__id=request.GET.get('batch_id', '')).order_by('roll_number')
        else:
            students = Student.objects.all().order_by('roll_number')   
        if request.is_ajax():
            student_list = []
            for student in students:
                student_list.append({
                    'id': student.id,
                    'name': student.student_name,
                    'roll_number': student.roll_number,
                })            
            response = simplejson.dumps({
                'result': 'Ok',
                'students': student_list
            })
            return HttpResponse(response, status = 200, mimetype="application/json")
        ctx = {
            'students': students
        }
        return render(request, 'academic/list_student.html',ctx)



class GetStudent(View):

    def get(self, request, *args, **kwargs):
        course_id = kwargs['course_id']
        batch_id = kwargs['batch_id']
        if request.is_ajax():
            try:
                students = Student.objects.filter(course__id=course_id, batch__id=batch_id)
                student_list = []
                for student in students:
                    student_list.append({
                        'student': student.student_name,
                        'id' :student.id 
                    })
                res = {
                    'result': 'ok',
                    'students': student_list,
                }
            except Exception as ex:
                res = {
                    'result': 'error: '+ str(ex),
                }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class ViewStudentDetails(View):  

    def get(self, request, *args, **kwargs):
        
        student_id = kwargs['student_id']
        ctx_student_data = []
        if request.is_ajax():
            try:
                student = Student.objects.get(id = student_id)
                qualified_exam = ''
                technical_qualification = ''
                fees_heads = ''
                for exam in student.qualified_exam.all():
                    qualified_exam = qualified_exam + exam.name + ', ' 
                qualified_exam = qualified_exam[:-1]
                
                for exam in student.technical_qualification.all():
                    technical_qualification = technical_qualification + exam.name + ', '
                for head in student.applicable_fees_heads.all():
                    fees_heads = fees_heads + head.name + ', ' 
                fees_heads = fees_heads[:-1]
                ctx_student_data.append({
                    'student_name': student.student_name if student.student_name else '',
                    'roll_number': student.roll_number if student.roll_number else '',
                    'dob': student.dob.strftime('%d/%m/%Y') if student.dob else '',
                    'address': student.address if student.address else '',
                    'course': student.course.course if student.course.course else '',
                    'course_id': student.course.id if student.course.course else '',
                    'name': str(student.batch.start_date) + '-' + str(student.batch.end_date) + ' ' + (str(student.batch.branch) if student.batch.branch else ''),     
                    'batch_start_date': student.batch.start_date if student.batch.start_date else '',
                    'batch_end_date': student.batch.end_date if student.batch.end_date else '',
                    'mobile_number': student.mobile_number if student.mobile_number else '',
                    'land_number': student.land_number if student.land_number else '',
                    'email': student.email if student.email else '',
                    'blood_group': student.blood_group if student.blood_group else '',
                    'doj': student.doj.strftime('%d/%m/%Y') if student.doj else '',
                    'photo': student.photo.name if student.photo.name else '',
                    'certificates_submitted': student.certificates_submitted if student.certificates_submitted else '',
                    'certificates_remarks': student.certificates_remarks if student.certificates_remarks else '',
                    'certificates_file': student.certificates_file if student.certificates_file else '',
                    'id_proofs_submitted': student.id_proofs_submitted if student.id_proofs_submitted else '',
                    'id_proofs_remarks': student.id_proofs_remarks if student.id_proofs_remarks else '',
                    'id_proofs_file': student.id_proofs_file if student.id_proofs_file else '',
                    'guardian_name': student.guardian_name if student.guardian_name else '',
                    'guardian_address': student.guardian_address if student.guardian_address else '',
                    'relationship': student.relationship if student.relationship else '',
                    'guardian_mobile_number': student.guardian_mobile_number if student.guardian_mobile_number else '',
                    'guardian_land_number': student.guardian_land_number if student.guardian_land_number else '',
                    'guardian_email': student.guardian_email if student.guardian_email else '',
                    'qualified_exam': qualified_exam if qualified_exam else 'xxx',
                    'technical_qualification': technical_qualification if technical_qualification else 'xxx',
                    'fees_head': fees_heads if fees_heads else 'xxx',
                })
                res = {
                    'result': 'ok',
                    'student': ctx_student_data,
                }
            except Exception as ex:
                res = {
                    'result': 'error: ' + str(ex),
                    'student': ctx_student_data,
                }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class EditStudentDetails(View):
   
    def get(self, request, *args, **kwargs):
        
        student_id = kwargs['student_id']
        context = {
            'student_id': student_id,
        }
        ctx_student_data = []
        qualified_exam = ''
        technical_qualification = ''
        if request.is_ajax():
            try:
                course =  request.GET.get('course', '')
                batch =  request.GET.get('batch', '')
                semester =  request.GET.get('semester', '')              

                if course:
                    course = Course.objects.get(id=course)
                if batch:
                    batch = Batch.objects.get(id=batch)
                if semester:
                    semester = Semester.objects.get(id=semester)
                student = Student.objects.get(id = student_id)

                for exam in student.qualified_exam.all():
                    qualified_exam = qualified_exam + exam.name + ',' 
                qualified_exam = qualified_exam[:-1]
                
                for exam in student.technical_qualification.all():
                    technical_qualification = technical_qualification + exam.name + ',' 
                technical_qualification = technical_qualification[:-1]
                ctx_fee_heads = []
                for fees_head in student.applicable_fees_heads.all():
                    ctx_fee_heads.append({
                        'head': fees_head.name,
                        'id': fees_head.id,
                    })
                ctx_student_data.append({
                    'student_name': student.student_name if student.student_name else '',
                    'roll_number': student.roll_number if student.roll_number else '',
                    'dob': student.dob.strftime('%d/%m/%Y') if student.dob else '',
                    'address': student.address if student.address else '',
                    'course': student.course.id if student.course.course else '',
                    'course_id': student.course.id if student.course.course else '',
                    'name': str(student.batch.start_date) + '-' + str(student.batch.end_date) + ' ' + (str(student.batch.branch) if student.batch.branch else ''),     
                    'batch': student.batch.id if student.batch else '',
                    'mobile_number': student.mobile_number if student.mobile_number else '',
                    'land_number': student.land_number if student.land_number else '',
                    'email': student.email if student.email else '',
                    'blood_group': student.blood_group if student.blood_group else '',
                    'doj': student.doj.strftime('%d/%m/%Y') if student.doj else '',
                    'photo': student.photo.name if student.photo.name else '',
                    'certificates_submitted': student.certificates_submitted if student.certificates_submitted else '',
                    'certificates_remarks': student.certificates_remarks if student.certificates_remarks else '',
                    'certificates_file': student.certificates_file if student.certificates_file else '',
                    'id_proofs_submitted': student.id_proofs_submitted if student.id_proofs_submitted else '',
                    'id_proofs_remarks': student.id_proofs_remarks if student.id_proofs_remarks else '',
                    'id_proofs_file': student.id_proofs_file if student.id_proofs_file else '',
                    'guardian_name': student.guardian_name if student.guardian_name else '',
                    'guardian_address': student.guardian_address if student.guardian_address else '',
                    'relationship': student.relationship if student.relationship else '',
                    'guardian_mobile_number': student.guardian_mobile_number if student.guardian_mobile_number else '',
                    'guardian_land_number': student.guardian_land_number if student.guardian_land_number else '',
                    'guardian_email': student.guardian_email if student.guardian_email else '',
                    'qualified_exams': qualified_exam if qualified_exam else '',
                    'technical_exams': technical_qualification if technical_qualification else '',
                    'applicable_fees_heads': ctx_fee_heads,
                })
                res = {
                    'result': 'ok',
                    'student': ctx_student_data,
                }
            except Exception as ex:
                res = {
                    'result': 'error: '+ str(ex),
                    'student': ctx_student_data,
                }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'academic/edit_student_details.html',context)

    def post(self, request, *args, **kwargs):

        student_id = kwargs['student_id']
        student = Student.objects.get(id = student_id)
        student_data = ast.literal_eval(request.POST['student'])
        print student_data
        try:
            student.student_name = student_data['student_name']
            student.roll_number = student_data['roll_number']
            student.address = student_data['address']
            course = Course.objects.get(id = student_data['course'])
            student.course=course
            batch = Batch.objects.get(id = student_data['batch'])
            student.batch=batch
            for exam in student.qualified_exam.all():
                student.qualified_exam.remove(exam)
            for exam in student.technical_qualification.all():
                student.technical_qualification.remove(exam)
            qualified_exams = student_data['qualified_exams'].split(',')
            for exam in qualified_exams:
                qualified_exam, created = QualifiedExam.objects.get_or_create(name=exam)
                student.qualified_exam.add(qualified_exam)

            technical_exams = student_data['technical_exams'].split(',')

            for technical_exam in technical_exams:
                tech_exam, created = TechnicalQualification.objects.get_or_create(name=technical_exam)
                student.technical_qualification.add(tech_exam)

            student.dob = datetime.strptime(student_data['dob'], '%d/%m/%Y')
            student.address = student_data['address']
            student.mobile_number = student_data['mobile_number']
            student.land_number = student_data['land_number']
            student.email = student_data['email']
            student.blood_group = student_data['blood_group']
            student.doj = datetime.strptime(student_data['doj'], '%d/%m/%Y')
            student.photo = request.FILES.get('photo_img', '')                       
            student.certificates_submitted = student_data['certificates_submitted']
            student.certificates_remarks = student_data['certificates_remarks']
            student.certificates_file = student_data['certificates_file']
            student.id_proofs_submitted = student_data['id_proofs_submitted']
            student.id_proofs_remarks = student_data['id_proofs_remarks']
            student.id_proofs_file = student_data['id_proofs_file']
            student.guardian_name = student_data['guardian_name']
            student.guardian_address = student_data['guardian_address']
            student.relationship = student_data['relationship']
            student.guardian_mobile_number = student_data['guardian_mobile_number']
            student.guardian_land_number = student_data['guardian_land_number']
            student.guardian_email = student_data['guardian_email']   
            student.save()
            fees_heads = ast.literal_eval(student_data['fee_heads'])
            if student.applicable_fees_heads.count() > 0 :
                student.applicable_fees_heads.clear()
            for fees_head in fees_heads:
                if fees_head not in student.applicable_fees_heads.all():
                    fee_head = FeesStructureHead.objects.get(id=fees_head)
                    student.applicable_fees_heads.add(fee_head)
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            res = {
                'result': 'error',
                'message': str(Ex)
            }
            status = 500
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class DeleteStudentDetails(View):
    def get(self, request, *args, **kwargs):
        student_id = kwargs['student_id']       
        student = Student.objects.filter(id=student_id)                          
        student.delete()
        return HttpResponseRedirect(reverse('list_student'))