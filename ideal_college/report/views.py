
import os
from datetime import datetime

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch,cm, mm

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from fees.models import Installment, FeesHead, FeesStructureHead, FeesStructure, FeesPaymentHead, FeesPayment, CommonFeesPayment
from college.models import College, Course, Batch
from academic.models import Student
from django.conf import settings

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


class IdcardReport(View):
   def get(self, request, *args, **kwargs):
    status_code = 200
    response = HttpResponse(content_type='application/pdf')
    p = canvas.Canvas(response, pagesize=(1000, 1250))
    y = 1150
    current_date = datetime.now().date()
    report_type = request.GET.get('report_type', '')
    if not report_type:
        return render(request, 'report/id_card.html',{
            'report_type' : 'id_card',
            })
    else:
        filtering_option = request.GET.get('filtering_option','')
        course = request.GET.get('course','')
        batch = request.GET.get('batch', '')
        if filtering_option == 'student_wise':
            p.rect(30,940,270,270)
            p.setFont('Times-Bold',10)  
            student_id = request.GET.get('student', '')
            student = Student.objects.get(id=student_id)
            heading = 'IDEAL ARTS AND SCIENCE COLLEGE'
            p.drawCentredString(160, y+40, heading)   
            p.setFont('Times-Roman',10)  
            heading = "Karumanamkurussi(PO), Cherupulassery"  
            p.drawCentredString(160, y+25, heading)   
            heading = "Palakkad(Dt),Kerala,PIN-679504"  
            p.drawCentredString(160, y+10, heading)  
            heading = "PH:466-2280111,2280112,2207585"  
            p.drawCentredString(160, y-5, heading)  
            p.drawString(40, y-30, "Name:")  
            p.drawString(120, y-30, student.student_name);
            p.drawString(40, y-45, "Guardian Name:")  
            p.drawString(120, y-45, student.guardian_name);
            p.drawString(40, y-60, "Course:")  
            if student.batch.branch:
                branch_name = student.batch.branch.branch
            else:
                branch_name = ''
            p.drawString(120, y-60, student.course.course+" "+ branch_name);
            p.drawString(40, y-75, "Batch:")  
            p.drawString(120, y-75, str(student.batch.start_date)+"-"+str(student.batch.end_date))  
            address = str(student.address)
            p.drawString(40,y-90,"Address:")
            i = 120
            j = 90
            for address_line in address.split(","):
                p.drawString(120, y-j, address_line.lstrip())
                j = j+15
            j = y-j
            p.drawString(40, j, "Date of Birth:")
            p.drawString(120, j, str(student.dob))
            p.drawString(40, j-15, "Land Phone:")
            p.drawString(120, j-15, str(student.land_number))
            p.drawString(40, j-30, "Blood Group:")
            p.drawString(120, j-30, str(student.blood_group))
            try:
                path = settings.PROJECT_ROOT.replace("\\", "/")+"/media/"+student.photo.name
                p.drawImage(path, 230, j-50, width=2*cm, height=2.5*cm, preserveAspectRatio=True)
            except:
                pass
        else:
            students = Student.objects.filter(course__id=course, batch__id=batch).order_by('roll_number')
            m = 30
            n = 940
            i = 160
            for student in students:
                p.rect(m,n,270,270)
                p.setFont('Times-Bold',10)  
                heading = 'IDEAL ARTS AND SCIENCE COLLEGE'
                p.drawCentredString(i, y+40, heading)   
                # p.setFont('Times-Roman',10)  
                # heading = "Karumanamkurussi(PO), Cherupulassery"  
                # p.drawCentredString(i, y+25, heading)   
                # heading = "Palakkad(Dt),Kerala,PIN-679504"  
                # p.drawCentredString(i, y+10, heading)  
                # heading = "PH:466-2280111,2280112,2207585"  
                # p.drawCentredString(i, y-5, heading)  
                print i
                m = m+300
                if m > 630:
                    m = 30
                    n = n-300
                if n < 40:
                    m = 30
                    n = 940
                    p.showPage()
        p.save()
        return response


class CommonFeeReport(View):

    def get(self, request, *args, **kwargs):    
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y-10)
        p.setFont("Helvetica", 14)  
        current_date = datetime.now().date()
        report_type = request.GET.get('type', '')
        if not report_type:
            return render(request, 'report/common_fee_report.html',{
                'report_type' : 'common_fees',
                })
        else:
            from_date = request.GET.get('from', '')
            to_date = request.GET.get('to', '')
            p.setFont('Times-Roman',20)  
            heading = 'IDEAL ARTS AND SCIENCE COLLEGE'
            p.drawCentredString(500, y+35, heading)   
            p.setFont('Times-Roman',14)  
            heading = "Karumanamkurussi(PO), Cherupulassery"  
            p.drawCentredString(500, y+15, heading)   
            heading = "Palakkad(Dt),Kerala,PIN-679504"  
            p.drawCentredString(500, y-5, heading)  
            heading = "PH:466-2280111,2280112,2207585"  
            p.drawCentredString(500, y-25, heading)  
            p.setFontSize(15)
            p.drawCentredString(500, y-60, "Common Fee Payment Report")  
            p.drawString(50, y - 120, "#")
            p.drawString(80, y - 120, "Name")
            p.drawString(250, y - 120, "Fee Head")
            p.drawString(420, y - 120, "Date")
            p.drawString(550, y - 120, "Total Amount")
            p.drawString(700, y - 120, "Amount Paid")
            if report_type == 'All':
                tot_amount = 0
                paid_amount = 0
                tot_count = 0
                j = 150
                commonfeepayments = CommonFeesPayment.objects.filter(paid_date__range=[from_date, to_date]).order_by('student')
                for commonfeepayment in commonfeepayments:
                    tot_amount = tot_amount + commonfeepayment.head.amount
                    paid_amount = paid_amount + commonfeepayment.paid_amount
                    tot_count = tot_count + 1
                    p.setFontSize(13)
                    p.drawString(50, y - j, str(tot_count))
                    p.drawString(80, y - j, commonfeepayment.student)
                    p.drawString(250, y - j, commonfeepayment.head.name)
                    p.drawString(420, y - j, str(commonfeepayment.paid_date.strftime('%d-%m-%Y')))
                    p.drawString(550, y - j, str(commonfeepayment.head.amount))
                    p.drawString(700, y - j, str(commonfeepayment.paid_amount))
                    j = j+30
                    if j > 1110:
                        j = 0
                        p.showPage()
                if j > 1020:
                    j = 0
                    p.showPage()
                j = y-j-10
                p.drawString(80, j, "From ")
                p.drawString(230, j, ":")
                p.drawString(250, j, str(datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-20, "To ")
                p.drawString(230, j-20, ":")
                p.drawString(250, j-20, str(datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-40, "Total count ")
                p.drawString(230, j-40, ":")
                p.drawString(250, j-40, str(tot_count))
                p.drawString(80, j-60, "Total amount ")
                p.drawString(230, j-60, ":")
                p.drawString(250, j-60, str(tot_amount))
                p.drawString(80, j-80, "Total amount collected ")
                p.drawString(230, j-80, ":")
                p.drawString(250, j-80, str(paid_amount))
            else:
                tot_amount = 0
                paid_amount = 0
                tot_count = 0
                j = 150
                commonfeepayments = CommonFeesPayment.objects.filter(paid_date__range=[from_date, to_date], head__id=report_type).order_by('student')
                for commonfeepayment in commonfeepayments:
                    tot_amount = tot_amount + commonfeepayment.head.amount
                    paid_amount = paid_amount + commonfeepayment.paid_amount
                    tot_count = tot_count + 1
                    p.setFontSize(13)
                    p.drawString(50, y - j, str(tot_count))
                    p.drawString(80, y - j, commonfeepayment.student)
                    p.drawString(250, y - j, commonfeepayment.head.name)
                    p.drawString(420, y - j, str(commonfeepayment.paid_date.strftime('%d-%m-%Y')))
                    p.drawString(550, y - j, str(commonfeepayment.head.amount))
                    p.drawString(700, y - j, str(commonfeepayment.paid_amount))
                    j = j+30
                    if j > 1110:
                        j = 0
                        p.showPage()
                if j > 1020:
                    j = 0
                    p.showPage()
                j = y-j-10
                p.drawString(80, j, "From ")
                p.drawString(230, j, ":")
                p.drawString(250, j, str(datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-20, "To ")
                p.drawString(230, j-20, ":")
                p.drawString(250, j-20, str(datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-40, "Total count ")
                p.drawString(230, j-40, ":")
                p.drawString(250, j-40, str(tot_count))
                p.drawString(80, j-60, "Total amount ")
                p.drawString(230, j-60, ":")
                p.drawString(250, j-60, str(tot_amount))
                p.drawString(80, j-80, "Total amount collected ")
                p.drawString(230, j-80, ":")
                p.drawString(250, j-80, str(paid_amount))
            p.save()
            return response



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

class FeeCollectedReport(View):
    
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
            return render(request, 'report/fee_collected_report.html',{
                'report_type' : 'fee_collected',
                })
        else:
            course = request.GET.get('course','')
            batch = request.GET.get('batch','')
            student_id = request.GET.get('student','')
            student = Student.objects.get(id=student_id)
            p.setFont('Times-Roman',20)  
            heading = 'IDEAL ARTS AND SCIENCE COLLEGE'
            p.drawCentredString(500, y+35, heading)   
            p.setFont('Times-Roman',14)  
            heading = "Karumanamkurussi(PO), Cherupulassery"  
            p.drawCentredString(500, y+15, heading)   
            heading = "Palakkad(Dt),Kerala,PIN-679504"  
            p.drawCentredString(500, y-5, heading)  
            heading = "PH:466-2280111,2280112,2207585"  
            p.drawCentredString(500, y-25, heading)  
            p.setFontSize(15)
            p.drawCentredString(500, y-60, "Fee Payment Report")  
            p.setFontSize(13)
            p.drawString(50, y - 100, "Student Name")
            p.drawString(200, y - 100, ":")
            p.drawString(350, y - 100, student.student_name)
            p.drawString(50, y - 120, "Unique ID")  
            p.drawString(200, y - 120, ":")          
            p.drawString(350, y - 120, str(student.unique_id))
            p.drawString(50, y - 140, "Roll Number")
            p.drawString(200, y - 140, ":")          
            p.drawString(350, y - 140, str(student.roll_number))
            p.drawString(50, y - 160, "Course")
            p.drawString(200, y - 160, ":") 
            if student.batch.branch:
                branch_name = student.batch.branch.branch
            else:
                branch_name = ''
            p.drawString(350, y - 160, student.course.course+" "+ branch_name);
            p.drawString(50, y - 180, "Batch")
            p.drawString(200, y - 180, ":")
            p.drawString(350, y - 180, str(student.batch.start_date)+"-"+str(student.batch.end_date))   
            try:
                student_fee = FeesPayment.objects.get(student__id=student_id)
                fee_payments = student_fee.payment_heads.all()
                p.drawString(50, y - 220, "#")
                p.drawString(80, y - 220, "Fee Head")
                p.drawString(250, y - 220, "Payment Type")
                p.drawString(420, y - 220, "Amount Paid")
                p.drawString(550, y - 220, "Total Amount")
                p.drawString(700, y - 220, "Fine")
                p.drawString(800, y - 220, "Date of Payment")
                j = 260
                tot_count = 0
                total_amount = 0
                for fee_payment in fee_payments:
                    tot_count = tot_count + 1
                    total_amount = total_amount + fee_payment.total_amount
                    p.drawString(50, y - j, str(tot_count))
                    p.drawString(80, y - j, fee_payment.fees_head.name)   
                    p.drawString(250, y - j, fee_payment.installment.name)  
                    p.drawString(420, y - j, str(fee_payment.total_amount)) 
                    p.drawString(550, y - j, str(fee_payment.fees_head.amount))  
                    p.drawString(700, y - j, str(fee_payment.fine))  
                    p.drawString(800, y - j, str(fee_payment.paid_date.strftime('%d-%m-%Y'))) 
                    j = j + 30
                    if j > 1110:
                        j = 0
                        p.showPage()
                j = j + 20
                p.drawString(50, y - j, "Total Amount Paid:")   
                p.drawString(200, y - j, ":") 
                p.drawString(250, y - j, str(total_amount)) 
            except:
                p.drawString(50, y - 220, "No fee history found for this student")
            p.save()
            return response


   
           
