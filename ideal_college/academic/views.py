import simplejson
import ast
from datetime import datetime

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from college.models import Course, Branch, Batch, Semester, QualifiedExam, TechnicalQualification, College
from academic.models import Student, StudentFees
from fees.models import FeesStructureHead

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch,cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle

from num2words import num2words

class AddStudent(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
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
                        if request.POST['applicable_to_special_fees'] != 'undefined':
                            student.applicable_to_special_fees = True
                        else:
                            student.applicable_to_special_fees = False
                        student.save()
                        fees_heads = ast.literal_eval(request.POST['applicable_fee_heads']) 
                        for fee_head in fees_heads:
                            fees_head = FeesStructureHead.objects.get(id=fee_head) 
                            try:
                                student.applicable_fees_heads.add(fees_head) 
                            except Exception as ex:
                                print str(ex) 
                                res = {
                                    'result': 'error',
                                    'message': str(ex)
                                }
                        if  student.applicable_to_special_fees:
                            student_fees = ast.literal_eval(request.POST['student_fees'])
                            for student_fee in student_fees:
                                studentfee = StudentFees()
                                studentfee.feeshead = FeesStructureHead.objects.get(id=student_fee['id'])
                                studentfee.amount = student_fee['amount']
                                studentfee.save()
                                try:
                                    student.student_fees.add(studentfee) 
                                except Exception as ex:
                                    print str(ex) 
                                    res = {
                                        'result': 'error',
                                        'message': str(ex)
                                    }
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
                students = Student.objects.filter(course__id=course_id, batch__id=batch_id).order_by('roll_number')
                student_list = []
                for student in students:
                    student_list.append({
                        'student': student.student_name,
                        'id' : student.id,
                        'u_id': student.unique_id if student and student.unique_id else '',
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
                    'uid': student.unique_id,
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
                ctx_student_fees = []
                for student_fee in student.student_fees.all():
                    ctx_student_fees.append({
                        'id':student_fee.feeshead.id,
                        'head': student_fee.feeshead.name,
                        'amount': student_fee.amount,
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
                    'uid': student.unique_id,
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
            if request.FILES.get('photo_img', ''):
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

class CheckUidExists(View):

    def get(self, request, *args, **kwargs):

        uid = request.GET.get('uid', '')
        try:
            student = Student.objects.get(unique_id=uid)
            res = {
                'result': 'error',
                'message': 'This student unique ID is already existing',
            }
        except Exception as ex:
            res = {
                'result': 'ok',                
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class SearchStudent(View):

    def get(self, request, *args, **kwargs):

        student_name = request.GET.get('student_name', '')
        course = request.GET.get('course', '')
        batch = request.GET.get('batch', '')
        students = Student.objects.filter(student_name__istartswith=student_name, course__id=course, batch__id=batch).order_by('roll_number')
        ctx_student_data = []
        for student in students:
            ctx_student_data.append({
                'student': student.student_name + str(' - ') + str(student.roll_number),
                'student_name': student.student_name,
                'id' : student.id,
                'u_id': student.unique_id if student and student.unique_id else '',
            })
        res = {
            'result': 'ok',
            'students': ctx_student_data,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')


class ConductCertificate(View):

    def get(self, request, *args, **kwargs):
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        report_type = request.GET.get('report_type', '')
        print report_type,"asdas"
        print request.GET.get('conduct_type', '')
        try:
            college = College.objects.latest('id')
            college_name = college.name 
        except:
            college = ''
            college_name = ''
        print college_name
        if not report_type:
            return render(request, 'academic/conduct_certificate.html',{
                'report_type' : 'conduct',
                'college_name': college_name if college else '',
            })
        else:
            conduct_type = request.GET.get('conduct_type', '')
            print conduct_type
            if request.GET.get('course', ''):
                course = Course.objects.get(id=request.GET.get('course', ''))
            if request.GET.get('batch', ''):
                batch = Batch.objects.get(id=request.GET.get('batch', ''))
            if request.GET.get('student', ''):
                student = Student.objects.get(id=request.GET.get('student', ''))
            if conduct_type == 'type1':
                p.setFont('Times-Bold',35)
                if request.GET.get('college_name',''):
                    college_name = request.GET.get('college_name','')
                    p.drawCentredString(500, y , college_name)
                else:
                    p.drawCentredString(500, y , (college.name if college else ''))
                p.setFont('Times-Roman',15)
                p.drawCentredString(500,y-30,"Karumanamkurussi P .O, Cheruplassery,Palakkad(Dt.)")
                p.setFont('Times-Bold',30)
                p.drawCentredString(500,y-60, "Course & Conduct Certificate")
                p.setFont('Times-Roman',20)
                p.drawString(120,y-110,"This is to certify Mr./Mrs./Kum..................................................is/was a Student of this institution")
                p.drawString(420,y-107,student.student_name)
                p.drawString(80,y-150,"for BA/B.Com/B.Sc Degree Course (Sub:.......................)")
                p.drawString(540,y-150,"during the academic year 20   - 20  ")
                p.drawString(140,y-210,"His/Her conduct and character are/were...................")
                p.drawString(560,y-210,"during the period .")
                p.drawString(80,y-290,"Place:.....................")
                p.drawString(660,y-290,"Principal")
                p.drawString(80,y-320,"Date:.....................")
                p.drawCentredString(500,y-380, "(Seal)")
            elif conduct_type == 'type2':
                p.setFont('Times-Bold',35)
                if request.GET.get('college_name',''):
                    college_name = request.GET.get('college_name','')
                    p.drawCentredString(500, y , college_name)
                else:
                    p.drawCentredString(500, y , (college.name if college else ''))
                p.setFont('Times-Roman',15)
                p.drawCentredString(500,y-30,"Karumanamkurussi P .O, Cheruplassery,PIN:679504")
                p.setFont('Times-Bold',30)
                p.drawCentredString(500,y-60, "Course & Conduct Certificate")
                p.setFont('Times-Roman',20)
                p.drawString(120,y-110,"This is to certify Sri/Smt_________________________________________________________")
                p.drawString(420,y-107,student.student_name)
                p.drawString(120,y-140,"was the student of the college for the________________________________________________")
                p.drawString(120,y-170,"Course during the period from___________________________to_________________________")
                p.drawString(120,y-200,"and his/her conduct and character are/were___________________________________________")
                p.drawString(80,y-290,"Remarks:")
                p.drawString(660,y-350,"Principal")
                p.drawString(80,y-350,"Date:.....................")
                p.drawCentredString(350,y-400, "(Seal)")
            elif conduct_type == 'type3':
                p.setFont('Times-Bold',35)
                if request.GET.get('college_name',''):
                    college_name = request.GET.get('college_name','')
                    p.drawCentredString(500, y , college_name)
                else:
                    p.drawCentredString(500, y , (college.name if college else ''))
                p.setFont('Times-Italic',20)
                p.drawCentredString(500, y - 30 , "(Affiliated to National Council for Vocational Training)")
                p.setFont('Times-Roman',20)
                p.drawCentredString(500, y - 60, "KARUMANAMKURUSSI P.O, PALAKKAD (Dt.) Pin: 679504, Ph: 0466-2207585,2280111")
                p.setFont('Times-Bold',25)
                p.drawCentredString(500, y - 120, "COURSE AND CONDUCT CERTIFICATE")
                p.setFont('Times-Roman',20)
                p.drawString(50, y - 120, "SL No .......................")
                p.drawString(120, y - 180,"This is to certify that....................................................................................................................")
                p.drawString(60, y - 220,"Son of/Daughter of ........................................................................................................... is/was trainee")
                p.drawString(60, y - 260,"in the trade ............................................................in this institution during the term Aug......................")
                p.drawString(60, y - 300,"to July ......................with admission number.....................................and his/her conduct and character")
                p.drawString(60, y - 340,"have been ..........................................")
                p.drawString(60, y - 420, "Cheruplassery")
                p.drawString(60, y - 460, "Date: ..........................")
                p.setFont('Times-Bold',20)
                p.drawString(750, y - 460, "Principal")
                p.setFont('Times-Roman',20)
                p.drawCentredString(500, y - 520, '(Seal)')
            p.save()
        return response


class PrintTC(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150

        report_type = request.GET.get('report_type', '')
        college_name = ''
        try:
            college = College.objects.latest('id')
            college_name = college.name + ' , '+ college.district
        except:
            college = ''
            college_name = ''
        if not report_type:
            return render(request, 'academic/print_tc.html',{
                'report_type' : 'tc',
                'college_name': college_name if college else '',
            })
        else:
            tc_type = request.GET.get('tc_type', '')
            if request.GET.get('student', ''):
                student = Student.objects.get(id=request.GET.get('student', ''))
            college_name = request.GET.get('college', '')
            college_name = college_name.replace('_', ' ')
            if tc_type == 'type1':
                p.drawCentredString(500, y - 20, ('Form-5')) 
                p.drawCentredString(500, y - 35, ('[See Rule VI - 17(1)]')) 
                p.drawString(50, y - 35, ('No. .......................................'))
                p.setFont('Times-Bold',25)  
                p.drawCentredString(500, y - 65, ('Transfer Certificate'))
                p.setFont('Helvetica',14)
                p.drawString(50, y - 95, ('Name of Institute : '))
                p.setFont('Helvetica-Bold',11) 
                p.drawString(170, y - 95, (college_name))
                p.setFont('Helvetica',14)
                p.drawString(50, y - 125, ('whether the institute is government, Aided or Recognised : '))
                p.setFont('Helvetica-Bold',12) 
                p.drawString(415, y - 125, ('SELF FINANCING'))
                p.setFont('Helvetica',14)
                p.drawString(50, y - 155, ('Name of Pupil : '))
                p.drawString(140, y - 155, (student.student_name))
                p.drawString(50, y - 185, ('Date of Birth according to admission register : '))
                p.drawString(340, y - 185, (student.dob.strftime('%d-%m-%Y')))
                dob_month = student.dob.strftime('%B')
                dob_date = num2words(student.dob.day).title() 
                dob_year = num2words(student.dob.year).title()   
                dob_words = ' ( ' + dob_date + ' ' + dob_month + ' ' +dob_year + ' ) '
                p.drawString(410, y - 185, (dob_words))
                p.drawString(50, y - 215, ('Class in which the pupil was Admitted'))
                p.drawString(290, y - 215, (' : ...................................................................................................................................'))
                p.drawString(50, y - 245, ('Date of Admission : '))
                p.drawString(180, y - 245, (student.doj.strftime('%d-%m-%Y')))
                p.drawString(50, y - 275, ('whether the pupil has paid all the fee due to the institute : '))
                p.drawString(410, y - 275, ('.......................................................................................................'))
                p.drawString(50, y - 315, ('whether the pupil was in receipt of fee concession : '))
                p.drawString(370, y - 315, ('.................................................................................................................'))
                p.drawString(50, y - 345, ("Date of the pupil's last attendance at institute : "))
                p.drawString(340, y - 345, ('.........................................................................................................................'))
                p.drawString(50, y - 375, ("Reason for leaving : "))
                p.drawString(190, y - 375, ('...............................................................................................................................................................'))
                p.drawString(50, y - 405, ("Date of application for certificate : "))
                p.drawString(270, y - 405, ('...........................................................................................................................................'))
                p.drawString(50, y - 435, ("Date of issue of the certificate : "))
                p.drawString(250, y - 435, ('................................................................................................................................................'))
                p.drawString(650, y - 515, ("Head of the Institution "))
                
            elif tc_type == 'type2':
                p.drawCentredString(500, y - 20, ('Form-5')) 
                p.drawCentredString(500, y - 35, ('[See Rule VI - 17(1)]')) 
                p.drawString(50, y - 35, ('No. .......................................'))
                p.setFont('Times-Bold',25)  
                p.drawCentredString(500, y - 65, ('Transfer Certificate'))
                p.setFont('Helvetica',12)
                p.drawString(50, y - 105, ('Name of Institute : '))
                p.setFont('Helvetica-Bold',11) 
                p.drawString(155, y - 105, (college_name))
                p.setFont('Helvetica',12)
                p.drawString(50, y - 135, ('whether the institute is government, Aided or Recognised : '))
                p.setFont('Helvetica-Bold',10) 
                p.drawString(370, y - 135, ('Affiliated to University of Calicut'))
                p.setFont('Helvetica',12)
                p.drawString(50, y - 165, ('Name of Student : '))
                p.drawString(155, y - 165, student.student_name)
                p.drawString(50, y - 195, ('Date of Birth according to admission Register : '))
                dob_month = student.dob.strftime('%B')
                dob_date = num2words(student.dob.day).title() 
                dob_year = num2words(student.dob.year).title()   
                dob_words = ' ( ' + dob_date + ' ' + dob_month + ' ' +dob_year + ' ) '
                p.drawString(305, y - 195, str(student.dob.strftime('%d-%m-%Y'))+" "+dob_words)
                p.drawString(50, y - 225, ('Class & Subject :  '))
                if student.batch.branch:
                    branch_name = student.batch.branch.branch
                else:
                    branch_name = ''
                p.drawString(150, y - 225, student.course.course+" "+ branch_name)
                p.drawString(400, y - 225, 'Year : ')
                p.drawString(450, y - 225, str(student.batch.start_date)+"-"+str(student.batch.end_date))
                p.drawString(50, y - 255, 'Date of admission : ')
                p.drawString(160, y - 255, str(student.doj.strftime('%d-%m-%Y')))
                p.drawString(400, y - 255, 'Admission No : ................................')
                p.drawString(50, y - 285, 'Whether the student has paid all the fee due to the institution : ...............................................................')
                p.drawString(50, y - 315, 'Whether the student was in receipt of fee concession : ...........................................................................')
                p.drawString(50, y - 345, 'Date of Student'+"'"+'s last attendence at the institute : ....................................................................................')                
                p.drawString(50, y - 375, 'Reason for leaving : .........................................')
                p.drawString(50, y - 405, 'Date of application for T.C : ...................................')
                p.drawString(50, y - 435, 'Date of issue of the T.C : ......................................')
                p.drawString(50, y - 500, 'Date : ')
                p.drawString(50, y - 550, 'Seal : ')
                p.setFont('Helvetica-Bold',16)
                p.drawString(600, y - 525, 'Principal')
            p.showPage()
            p.save()
        return response

class PrintTCConductCertificate(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150

        report_type = request.GET.get('report_type', '')
        college_name = ''
        try:
            college = College.objects.latest('id')
            college_name = college.name + ' , '+ college.district
        except:
            college = ''
            college_name = ''
        if not report_type:
            return render(request, 'academic/print_tc_conduct_certificate.html',{
                'report_type' : 'tc',
                'college_name': college_name if college else '',
            })
        else:
            # IDEAL TEACHER TRAINING COLLEGE, CHERPULASSERY
            try:
                student = Student.objects.get(id=request.GET.get('student', ''))
            except:
                student = None
            p.setFont('Times-Bold',20) 
            college_name = request.GET.get('college', '').replace('_', ' ')
            p.drawCentredString(500, y - 20, (college_name)) 
            p.setFont('Times-Bold',12) 
            p.drawCentredString(500, y - 40, ('KARUMANAMKURUSSI. (P.O), PALAKKAD(DT.), PIN:679504'))
            p.drawCentredString(500, y - 60, ('( Affiliated to University of Calicut )'))  
            p.drawString(100, y - 80, ('No: ........................................'))  
            p.roundRect(350, y - 120, 300 , 25, 0.1*inch)
            p.setFont('Times-Bold',14)
            p.drawString(362, y - 112, ('TRANSFER & CONDUCT CERTIFICATE')) 
            p.setFont('Times-Roman',14)
            p.drawString(100, y - 170, ('1.  Name of Student:....................................................................................................................................................................................................... ')) 
            p.drawString(100, y - 200, ('2.  Date of Birth as entered in the Admission Register:................................................................................................................................................. ')) 
            p.drawString(100, y - 230, ('3.  Admission No: .........................................................')) 
            p.drawString(400, y - 230, ('  Date of Admission: .................................................................................................................')) 
            p.drawString(100, y - 260, ('4.  Class in which the student was admitted:................................................................................................................................................................... ')) 
            p.drawString(100, y - 290, ('5.  Whether all dues to the college have been paid: ........................................................................................................................................................'))
            p.drawString(100, y - 320, ('6.  Whether the student was in receipt of any scholarship or Concession : ....................................................................................................................'))
            p.drawString(100, y - 350, ('7.  Whether the student has appeared for the Examination:.............................................................................................................................................'))
            p.drawString(100, y - 380, ('8.  Register No:............................................................. '))
            p.drawString(400, y - 380, ('  Year:......................................................................................................................................... '))
            p.drawString(100, y - 410, ('9.  Whether qualified for promotion:............................................................................................................................................................................... '))
            p.drawString(100, y - 440, ('10.  Reason for leaving:................................................................................................................................................................................................... '))
            p.drawString(100, y - 470, ('11.  Date of application for Transfer Certificate:............................................................................................................................................................. '))
            p.drawString(100, y - 500, ('12.  Date of Issue of Transfer Certificate:........................................................................................................................................................................ '))
            p.drawString(100, y - 530, ('13.  Conduct during the period:........................................................................................................................................................................................ '))
            p.drawString(120, y - 630, ('Date: '))
            p.drawString(820, y - 630, ('Principal'))
            if student:
                p.drawString(250, y - 165, (student.student_name)) 
                p.drawString(420, y - 195, (student.dob.strftime('%d/%m/%Y')))
                p.drawString(550, y - 225, (student.doj.strftime('%d/%m/%Y')))  

        p.showPage()
        p.save()
        return response
