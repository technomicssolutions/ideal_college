
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from fees.models import Installment, FeesHead, FeesStructureHead, FeesStructure, FeesPaymentInstallment, FeesPayment, CommonFeesPayment
from college.models import College, Course, Batch
from academic.models import Student
from exam.models import Exam

def header(canvas, y):

    try:
        college = College.objects.latest('id')
    except:
        college = ''
    canvas.setFont("Helvetica", 35)  
    if college:
        canvas.drawString(80, y - 5, college.name)
    canvas.line(50, y - 30, 950, y - 30)
    return canvas


class OutstandingFeesListReport(View):

    def get(self, request, *args, **kwargs):
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y)
        p.setFont("Helvetica", 14)  
        current_date = datetime.now().date()
        report_type = request.GET.get('report_type', '')
        if not report_type:
            return render(request, 'report/outstanding_fees.html',{
                'report_type' : 'outstanding_fees',
                })
        else:
            filtering_option = request.GET.get('filtering_option','')
            fees_type = request.GET.get('fees_type','')
            course = request.GET.get('course','')
            batch = request.GET.get('batch', '')
            
            student_id = request.GET.get('student', '')
            if request.GET.get('fees_type','') == 'course':
                course = Course.objects.get(id=request.GET.get('course', ''))
                try:
                    fees_structure = FeesStructure.objects.get(course__id=request.GET.get('course', ''), batch__id=request.GET.get('batch', ''))
                except:
                    p.save()
                    return response
                if filtering_option == 'student_wise':
                    student = Student.objects.get(id=student_id)
                    batch = Batch.objects.get(id=request.GET.get('batch', ''))
                    batch_name = str(batch.start_date) + ' - ' + str(batch.end_date) + ((' - '+ str(batch.branch.branch)) if batch.branch else '')
                    heading = 'Student Wise Report' + ' - ' + course.course + ' - ' + batch_name + ' - '+ student.student_name +' - Roll no: '+str(student.roll_number)
                    p.drawCentredString(400, y - 70, heading)
                    p.setFontSize(13)
                    p.drawString(50, y - 100, "Head")
                    p.drawString(160, y - 100, "Total amount")
                    p.drawString(250, y - 100, "Inst. Name")
                    p.drawString(390, y - 100, "Inst. Amount")
                    p.drawString(490, y - 100, "Inst. Fine")
                    p.drawString(590, y - 100, "Inst. Due Date")
                    p.drawString(690, y - 100, "Inst. Paid")
                    p.drawString(790, y - 100, "Inst. Balance")
                    p.setFontSize(12)  
                    heads = fees_structure.head.all()
                    y1 = y - 110
                    for head in heads:
                        is_not_paid = False
                        i = 0
                        for installment in head.installments.all():
                            try:
                                fees_payment = FeesPayment.objects.get(fee_structure=fees_structure, student__id=student_id)
                                fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                                if fees_payment_installments.count() > 0:
                                    if fees_payment_installments[0].installment_amount < installment.amount:
                                        is_not_paid = True
                                        y1 = y1 - 30
                                        if y1 <= 135:
                                            y1 = y - 110
                                            p.showPage()
                                            p = header(p, y)
                                            p.setFontSize(12) 
                                        
                                        p.drawString(250, y1, str('installment'+str(i + 1)))
                                        p.drawString(390, y1, str(installment.amount))
                                        p.drawString(490, y1, str(installment.fine_amount))
                                        p.drawString(590, y1, installment.due_date.strftime('%d/%m/%Y'))
                                        p.drawString(690, y1, str(fees_payment_installments[0].installment_amount))
                                        p.drawString(790, y1, str(float(installment.amount) - float(fees_payment_installments[0].installment_amount)))
                                elif fees_payment_installments.count() == 0:
                                    is_not_paid = True
                                    y1 = y1 - 30
                                    if y1 <= 135:
                                        y1 = y - 110
                                        p.showPage()
                                        p = header(p, y)
                                        p.setFontSize(12) 

                                    p.drawString(250, y1, str('installment'+str(i + 1)))
                                    p.drawString(390, y1, str(installment.amount))
                                    p.drawString(490, y1, str(installment.fine_amount))
                                    p.drawString(590, y1, installment.due_date.strftime('%d/%m/%Y'))
                                    p.drawString(690, y1, str(0))
                                    p.drawString(790, y1, str(installment.amount))
                            except Exception as ex:
                                if current_date >= installment.due_date:
                                    is_not_paid = True
                                    y1 = y1 - 30
                                    if y1 <= 135:
                                        y1 = y - 110
                                        p.showPage()
                                        p = header(p, y)
                                        p.setFontSize(12) 

                                    p.drawString(250, y1, str('installment'+str(i + 1)))
                                    p.drawString(390, y1, str(installment.amount))
                                    p.drawString(490, y1, str(installment.fine_amount))
                                    p.drawString(590, y1, installment.due_date.strftime('%d/%m/%Y'))
                                    p.drawString(690, y1, str(0))
                                    p.drawString(790, y1, str(installment.amount))
                            i = i + 1
                        if is_not_paid:
                            p.drawString(50, y1, head.name)
                            p.drawString(180, y1, str(head.amount))
                        y1 = y1 - 30
                        if y1 <= 135:
                            y1 = y - 110
                            p.showPage()
                            p = header(p, y)
                            p.setFontSize(12) 
                        
                else:
                    students = Student.objects.filter(course__id=request.GET.get('course', ''), batch__id=request.GET.get('batch', '')).order_by('roll_number')
                    batch = Batch.objects.get(id=request.GET.get('batch', ''))
                    batch_name = str(batch.start_date) + ' - ' + str(batch.end_date) + ((' - '+ str(batch.branch.branch)) if batch.branch else '')
                    heading = 'Batch Wise Report' + ' - ' + course.course + ' - ' + batch_name 
                    p.drawCentredString(400, y - 70, heading)
                    p.setFontSize(13)
                    p.drawString(50, y - 100, "Roll Number")
                    p.drawString(150, y - 100, "Student")
                    p.drawString(250, y - 100, "Head")
                    p.drawString(350, y - 100, "Total amount")
                    p.drawString(450, y - 100, "Inst. Name")
                    p.drawString(550, y - 100, "Inst. Amount")
                    p.drawString(650, y - 100, "Inst. Fine")
                    p.drawString(730, y - 100, "Inst. Due Date")
                    p.drawString(830, y - 100, "Inst. Paid")
                    p.drawString(900, y - 100, "Inst. Balance")
                    y1 = y - 110
                    for student in students:
                        y1 = y1 - 30
                        if y1 <= 135:
                            y1 = y - 110
                            p.showPage()
                            p = header(p, y)
                            p.setFontSize(12) 
                        p.drawString(50, y1, str(student.roll_number))
                        p.drawString(150, y1, student.student_name)
                        heads = fees_structure.head.all()
                        for head in heads:
                            is_not_paid = False
                            i = 0
                            y1 = y1 - 30
                            if y1 <= 135:
                                y1 = y - 110
                                p.showPage()
                                p = header(p, y)
                                p.setFontSize(12) 
                            for installment in head.installments.all():
                                try:
                                    fees_payment = FeesPayment.objects.get(fee_structure=fees_structure, student=student)
                                    fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                                    if fees_payment_installments.count() > 0:
                                        if fees_payment_installments[0].installment_amount < installment.amount:
                                            is_not_paid = True
                                            y1 = y1 - 30
                                            if y1 <= 135:
                                                y1 = y - 110
                                                p.showPage()
                                                p = header(p, y)
                                                p.setFontSize(12) 
                                            
                                            p.drawString(450, y1, str('installment'+str(i + 1)))
                                            p.drawString(550, y1, str(installment.amount))
                                            p.drawString(650, y1, str(installment.fine_amount))
                                            p.drawString(730, y1, installment.due_date.strftime('%d/%m/%Y'))
                                            p.drawString(830, y1, str(fees_payment_installments[0].installment_amount))
                                            p.drawString(900, y1, str(float(installment.amount) - float(fees_payment_installments[0].installment_amount)))
                                    elif fees_payment_installments.count() == 0:
                                        is_not_paid = True
                                        y1 = y1 - 30
                                        if y1 <= 135:
                                            y1 = y - 110
                                            p.showPage()
                                            p = header(p, y)
                                            p.setFontSize(12) 

                                        p.drawString(450, y1, str('installment'+str(i + 1)))
                                        p.drawString(550, y1, str(installment.amount))
                                        p.drawString(650, y1, str(installment.fine_amount))
                                        p.drawString(730, y1, installment.due_date.strftime('%d/%m/%Y'))
                                        p.drawString(830, y1, str(0))
                                        p.drawString(900, y1, str(installment.amount))
                                except Exception as ex:
                                    is_not_paid = True
                                    if current_date >= installment.due_date:
                                        y1 = y1 - 30
                                        if y1 <= 135:
                                            y1 = y - 110
                                            p.showPage()
                                            p = header(p, y)
                                            p.setFontSize(12) 

                                        p.drawString(450, y1, str('installment'+str(i + 1)))
                                        p.drawString(550, y1, str(installment.amount))
                                        p.drawString(650, y1, str(installment.fine_amount))
                                        p.drawString(730, y1, installment.due_date.strftime('%d/%m/%Y'))
                                        p.drawString(830, y1, str(0))
                                        p.drawString(900, y1, str(installment.amount))
                                i = i + 1
                            if is_not_paid:
                                p.drawString(250, y1, head.name)
                                p.drawString(350, y1, str(head.amount))
            else:
                heads = FeesHead.objects.all()
                if filtering_option == 'student_wise':
                    student = Student.objects.get(id=student_id)
                    course = Course.objects.get(id=request.GET.get('course', ''))
                    batch = Batch.objects.get(id=request.GET.get('batch', ''))
                    batch_name = str(batch.start_date) + ' - ' + str(batch.end_date) + ((' - '+ str(batch.branch.branch)) if batch.branch else '')
                    heading = 'Student Wise Report' + ' - ' + course.course + ' - ' + batch_name + ' - '+ student.student_name+' - Roll no: '+str(student.roll_number)
                    p.drawCentredString(400, y - 70, heading)
                    p.setFontSize(13)
                    
                    p.drawString(150, y - 100, "Head Name")
                    p.drawString(320, y - 100, "Total Amount")
                    p.drawString(420, y - 100, "Paid")
                    p.drawString(520, y - 100, "Balance")
                    p.setFontSize(12) 
                    y1 = y - 110
                    for head in heads:
                        try:
                            fees_payment = CommonFeesPayment.objects.get(head=head, student__id=student_id)
                            if fees_payment.paid_amount < head.amount:
                                y1 = y1 - 30
                                if y1 <= 135:
                                    y1 = y - 110
                                    p.showPage()
                                    p = header(p, y)
                                    p.setFontSize(12) 
                                p.drawString(150, y1, str(head.name))
                                p.drawString(320, y1, str(head.amount))
                                p.drawString(420, y1, str(fees_payment.paid_amount))
                                p.drawString(520, y1, str(float(head.amount) - float(fees_payment.paid_amount)))
                        except:
                            y1 = y1 - 30
                            if y1 <= 135:
                                y1 = y - 110
                                p.showPage()
                                p = header(p, y)
                                p.setFontSize(12) 
                            p.drawString(150, y1, str(head.name))
                            p.drawString(320, y1, str(head.amount))
                            p.drawString(420, y1, str(0))
                            p.drawString(520, y1, str(float(head.amount)))
                else:
                    students = Student.objects.filter(course__id=request.GET.get('course', ''), batch__id=request.GET.get('batch', '')).order_by('roll_number')
                    course = Course.objects.get(id=request.GET.get('course', ''))
                    batch = Batch.objects.get(id=request.GET.get('batch', ''))
                    batch_name = str(batch.start_date) + ' - ' + str(batch.end_date) + ((' - '+ str(batch.branch.branch)) if batch.branch else '')
                    heading = 'Batch Wise Report' + ' - ' + course.course + ' - ' + batch_name
                    p.drawCentredString(400, y - 70, heading)
                    p.setFontSize(13)
                    p.drawString(50, y - 100, "Roll Number")
                    p.drawString(150, y - 100, "Student")
                    p.drawString(320, y - 100, "Head Name")
                    p.drawString(490, y - 100, "Total Amount")
                    p.drawString(590, y - 100, "Paid")
                    p.drawString(690, y - 100, "Balance")
                    p.setFontSize(12) 
                    y1 = y - 110
                    for student in students:
                        y1 = y1 - 30
                        if y1 <= 135:
                            y1 = y - 110
                            p.showPage()
                            p = header(p, y)
                            p.setFontSize(12) 
                        p.drawString(50, y1, str(student.roll_number))
                        p.drawString(150, y1, student.student_name)
                        for head in heads:
                            try:
                                fees_payment = CommonFeesPayment.objects.get(head=head, student__id=student_id)
                                if fees_payment.paid_amount < head.amount:
                                    y1 = y1 - 30
                                    if y1 <= 135:
                                        y1 = y - 110
                                        p.showPage()
                                        p = header(p, y)
                                        p.setFontSize(12) 
                                    p.drawString(320, y1, str(head.name))
                                    p.drawString(490, y1, str(head.amount))
                                    p.drawString(590, y1, str(fees_payment.paid_amount))
                                    p.drawString(690, y1, str(float(head.amount) - float(fees_payment.paid_amount))) 
                            except:
                                y1 = y1 - 30
                                if y1 <= 135:
                                    y1 = y - 110
                                    p.showPage()
                                    p = header(p, y)
                                    p.setFontSize(12) 
                                p.drawString(320, y1, str(head.name))
                                p.drawString(490, y1, str(head.amount))
                                p.drawString(590, y1, str(0))
                                p.drawString(690, y1, str(float(head.amount))) 
            p.save()
        return response

class ExamScheduleReport(View):

    def get(self, request, *args, **kwargs):

        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y)
        p.setFont("Helvetica", 14)  
        report_type = request.GET.get('report_type', '')
        if not report_type:
            return render(request, 'report/exam_schedule.html',{
                'report_type' : 'exam_schedule',
                })
        else:
            exam_id = request.GET.get('exam_id', '')
            exam = Exam.objects.get(id=exam_id)
            batch_name = str(exam.batch.start_date)+ ' - '+str(exam.batch.end_date) +(' - '+exam.batch.branch.branch if exam.batch.branch else '')
            # heading = exam.course.course+ ' - ' + batch_name + ' - ' +exam.exam_name 
            # p.drawCentredString(400, y - 70, heading)
            p.setFontSize(14)
            p.drawString(50, y - 100, "Exam")
            p.drawString(50, y - 120, "Course ")
            p.drawString(50, y - 140, "Batch")
            p.drawString(50, y - 160, "Semester")
            p.drawString(50, y - 180, "Start Date ")
            p.drawString(50, y - 200, "End Date")
            p.drawString(50, y - 220, "Exam Total")
            p.drawString(50, y - 240, "No. of Subjects")
            p.drawString(150, y - 100, "-")
            p.drawString(150, y - 120, "-")
            p.drawString(150, y - 140, "-")
            p.drawString(150, y - 160, "-")
            p.drawString(150, y - 180, "-")
            p.drawString(150, y - 200, "-")
            p.drawString(150, y - 220, "-")
            p.drawString(150, y - 240, "-")
            p.drawString(175, y - 100, exam.exam_name)
            p.drawString(175, y - 120, exam.course.course)
            p.drawString(175, y - 140, batch_name)
            p.drawString(175, y - 160, exam.semester.semester if exam.semester else '')
            p.drawString(175, y - 180, exam.start_date.strftime('%d/%m/%Y') if exam.start_date else '')
            p.drawString(175, y - 200, exam.end_date.strftime('%d/%m/%Y') if exam.end_date else '')
            p.drawString(175, y - 220, str(exam.exam_total))
            p.drawString(175, y - 240, str(exam.no_subjects))
            p.drawString(50, y - 280, 'Subject')
            p.drawString(250, y - 280, 'Date')
            p.drawString(350, y - 280, 'Start Time')
            p.drawString(450, y - 280, 'End Time')
            p.drawString(550, y - 280, 'Total Mark')
            p.drawString(650, y - 280, 'Pass Mark')
            y1 = y - 300
            for subject in exam.subjects.all():
                p.drawString(50, y1, subject.subject_name)
                p.drawString(250, y1, subject.date.strftime('%d/%m/%Y'))
                p.drawString(350, y1, str(subject.start_time))
                p.drawString(450, y1, str(subject.end_time))
                p.drawString(550, y1, str(subject.total_mark))
                p.drawString(650, y1, str(subject.pass_mark))
                y1 = y1 - 30
                if y1 <= 270:
                    y1 = y - 100
                    p.showPage()
                    p = header(p, y)
            p.showPage()
            p.save()
            return response