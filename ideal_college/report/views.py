
import os
from datetime import datetime

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch,cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY, TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.conf import settings

from fees.models import Installment, FeesHead, FeesStructureHead, FeesStructure, FeesPaymentHead, FeesPayment, CommonFeesPayment
from college.models import College, Course, Batch
from academic.models import Student

style = [
    ('FONTSIZE', (0,0), (-1, -1), 12),
    ('FONTNAME',(0,0),(-1,-1),'Helvetica') 
]

para_style = ParagraphStyle('fancy')
para_style.fontSize = 12
para_style.fontName = 'Helvetica'


def header(canvas, y):

    try:
        college = College.objects.latest('id')
    except:
        college = ''
    canvas.setFont("Helvetica", 35)  
    if college:
        canvas.setFont('Times-Roman',20)  
        canvas.drawCentredString(500, y+45, college.name) 
        canvas.setFont('Times-Roman',14)  
        canvas.drawCentredString(500, y+25, college.address) 
        canvas.drawCentredString(500, y+5, college.district+","+college.state+",PIN-"+college.PIN)           
        canvas.drawCentredString(500, y-15, "PH: "+college.contact)   
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
    try:
        college = College.objects.latest('id')
    except:
        college = ''
    if not report_type:
        return render(request, 'report/id_card.html',{
            'report_type' : 'id_card',
            })
    else:
        filtering_option = request.GET.get('filtering_option','')
        course = request.GET.get('course','')
        batch = request.GET.get('batch', '')
        if filtering_option == 'student_wise':
            student_id = request.GET.get('student', '')
            student = Student.objects.get(id=student_id)
            p.rect(30,940,270,270)
            p.setFont('Times-Bold',10)  
            p.drawCentredString(160, y+40, college.name) 
            p.setFont('Times-Roman',10)  
            p.drawCentredString(160, y+25, college.address) 
            p.drawCentredString(160, y+10, college.district+","+college.state+",PIN-"+college.PIN)           
            p.drawCentredString(160, y-5, "PH: "+college.contact)
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
            p.drawString(120, j, student.dob.strftime('%d/%m/%Y'))
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
            x1 = 40
            x2 = 120
            c1 = 230
            for student in students:
                p.rect(m,n,270,270)
                p.setFont('Times-Bold',10)  
                p.drawCentredString(i, y + 40, college.name)   
                p.setFont('Times-Roman',10)  
                p.drawCentredString(i, y + 25, college.address)   
                p.drawCentredString(i, y + 10, college.district+","+college.state+",PIN-"+college.PIN)           
                p.drawCentredString(i, y - 5, "PH: "+college.contact)
                p.drawString(x1, y-30, "Name:")  
                p.drawString(x2, y-30, student.student_name);
                p.drawString(x1, y-45, "Guardian Name:")  
                p.drawString(x2, y-45, student.guardian_name);
                p.drawString(x1, y-60, "Course:")  
                if student.batch.branch:
                    branch_name = student.batch.branch.branch
                else:
                    branch_name = ''
                p.drawString(x2, y-60, student.course.course+" "+ branch_name);
                p.drawString(x1, y-75, "Batch:")  
                p.drawString(x2, y-75, str(student.batch.start_date)+"-"+str(student.batch.end_date))  
                address = str(student.address)
                p.drawString(x1, y-90,"Address:")
                i1 = 120
                j1 = 90
                for address_line in address.split(","):
                    p.drawString(x2, y-j1, address_line.lstrip())
                    j1 = j1+15
                j1 = y-j1
                p.drawString(x1, j1, "Date of Birth:")
                p.drawString(x2, j1, student.dob.strftime('%d/%m/%Y'))
                p.drawString(x1, j1-15, "Land Phone:")
                p.drawString(x2, j1-15, str(student.land_number))
                p.drawString(x1, j1-30, "Blood Group:")
                p.drawString(x2, j1-30, str(student.blood_group))
                try:
                    path = settings.PROJECT_ROOT.replace("\\", "/")+"/media/"+student.photo.name
                    p.drawImage(path, c1, j1-50, width=2*cm, height=2.5*cm, preserveAspectRatio=True)
                except:
                    pass
                c1 = c1 + 300
                x1 = x1 + 300
                x2 = x2 + 300
                i = i + 300
                if i > 760:
                    i = 160
                    y = y - 300
                    x1 = 40
                    x2 = 120
                    c1 = 230
                if y < 250:
                    y = 1150
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
                p.drawString(280, j, ":")
                p.drawString(300, j, str(datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-20, "To ")
                p.drawString(280, j-20, ":")
                p.drawString(300, j-20, str(datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-40, "Total count ")
                p.drawString(280, j-40, ":")
                p.drawString(300, j-40, str(tot_count))
                p.drawString(80, j-60, "Total amount ")
                p.drawString(280, j-60, ":")
                p.drawString(300, j-60, str(tot_amount))
                p.drawString(80, j-80, "Total amount collected ")
                p.drawString(280, j-80, ":")
                p.drawString(300, j-80, str(paid_amount))
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
                p.drawString(280, j, ":")
                p.drawString(300, j, str(datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-20, "To ")
                p.drawString(280, j-20, ":")
                p.drawString(300, j-20, str(datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(80, j-40, "Total count ")
                p.drawString(280, j-40, ":")
                p.drawString(300, j-40, str(tot_count))
                p.drawString(80, j-60, "Total amount ")
                p.drawString(280, j-60, ":")
                p.drawString(300, j-60, str(tot_amount))
                p.drawString(80, j-80, "Total amount collected ")
                p.drawString(280, j-80, ":")
                p.drawString(300, j-80, str(paid_amount))
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
                    p.drawString(200, y - 100, "Total amount")
                    p.drawString(300, y - 100, "Paid Amt")
                    p.drawString(400, y - 100, "Payment Type")
                    p.drawString(530, y - 100, "Start Date")
                    p.drawString(630, y - 100, "End Date")
                    p.drawString(730, y - 100, "Fine")
                    p.setFontSize(12)  
                    heads = student.applicable_fees_heads.all()
                    y1 = y - 130
                    for head in heads: 
                        new_y1 = y1
                        try:
                            fees_payment = FeesPayment.objects.get(fee_structure=fees_structure, student=student)
                            fees_payment_heads = fees_payment.payment_heads.filter(fees_head=head)
                            if fees_payment_heads.count() == 0:
                                installment = head.installments.filter(name='Late Payment')
                                if installment.count() == 0:
                                    installment = head.installments.filter(name='Standard Payment')
                                    if installment.count() == 0:
                                        installment = head.installments.filter(name='Early Payment')
                                if installment.count() > 0:
                                    if installment[0].end_date < current_date:
                                        data=[[Paragraph(head.name, para_style)]]
                                        table = Table(data, colWidths=[150], rowHeights=100, style=style)      
                                        table.wrapOn(p, 200, 400)
                                        table.drawOn(p, 45, y1-10)
                                        p.drawString(200, y1, str(head.amount))
                                        p.drawString(300, y1, str(0))
                                        for installment in head.installments.all():
                                            p.drawString(400, y1, installment.name)
                                            p.drawString(530, y1, installment.start_date.strftime('%d/%m/%Y'))
                                            p.drawString(630, y1, installment.end_date.strftime('%d/%m/%Y'))
                                            p.drawString(730, y1, str(installment.fine_amount))
                                            y1 = y1 - 15
                                            if y1 <= 135:
                                                y1 = y - 110
                                                p.showPage()
                                                p = header(p, y)
                                                p.setFontSize(12)
                            else:
                                if fees_payment_heads[0].paid_fee_amount != head.amount:
                                    installment = head.installments.filter(name='Late Payment')
                                    if installment.count() == 0:
                                        installment = head.installments.filter(name='Standard Payment')
                                        if installment.count() == 0:
                                            installment = head.installments.filter(name='Early Payment')
                                    if installment:
                                        if installment[0].end_date < current_date:
                                            data=[[Paragraph(head.name, para_style)]]
                                            table = Table(data, colWidths=[150], rowHeights=100, style=style)      
                                            table.wrapOn(p, 200, 400)
                                            table.drawOn(p, 45, y1-10)
                                            p.drawString(200, y1, str(head.amount))
                                            p.drawString(300, y1, str(fees_payment_heads[0].paid_fee_amount))
                                            for installment in head.installments.all():
                                                p.drawString(400, y1, installment.name)
                                                p.drawString(530, y1, installment.start_date.strftime('%d/%m/%Y'))
                                                p.drawString(630, y1, installment.end_date.strftime('%d/%m/%Y'))
                                                p.drawString(730, y1, str(installment.fine_amount))
                                                y1 = y1 - 15
                                                if y1 <= 135:
                                                    y1 = y - 110
                                                    p.showPage()
                                                    p = header(p, y)
                                                    p.setFontSize(12)

                        except Exception as ex:
                            installment = head.installments.filter(name='Late Payment')
                            if installment.count() == 0:
                                installment = head.installments.filter(name='Standard Payment')
                                if installment.count() == 0:
                                    installment = head.installments.filter(name='Early Payment')
                            if installment.count() > 0:
                                if installment[0].end_date < current_date:
                                    data=[[Paragraph(head.name, para_style)]]
                                    table = Table(data, colWidths=[150], rowHeights=100, style=style)      
                                    table.wrapOn(p, 200, 400)
                                    table.drawOn(p, 45, y1-10) 
                                    p.drawString(200, y1, str(head.amount))
                                    p.drawString(300, y1, str(0))
                                    for installment in head.installments.all():
                                        p.drawString(400, y1, installment.name)
                                        p.drawString(530, y1, installment.start_date.strftime('%d/%m/%Y'))
                                        p.drawString(630, y1, installment.end_date.strftime('%d/%m/%Y'))
                                        p.drawString(730, y1, str(installment.fine_amount))
                                        y1 = y1 - 25
                                        if y1 <= 135:
                                            y1 = y - 110
                                            p.showPage()
                                            p = header(p, y)
                                            p.setFontSize(12)
                        if new_y1 != y1:
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
                    p.drawString(130, y - 100, "Student")
                    p.drawString(250, y - 100, "Head")
                    p.drawString(450, y - 100, "Total amount")
                    p.drawString(550, y - 100, "Paid Amt")
                    p.drawString(620, y - 100, "Payment Type")
                    p.drawString(750, y - 100, "Start Date")
                    p.drawString(840, y - 100, "End Date")
                    p.drawString(920, y - 100, "Fine")
                    y1 = y - 130
                    new_y1 = y1
                    for student in students:
                        
                        y1 = y1 - 30
                        if y1 <= 135:
                            y1 = y - 130
                            p.showPage()
                            p = header(p, y)
                            p.setFontSize(12)
                        new_y1 = y1
                        p.drawString(50, y1, str(student.roll_number))
                        stud_name = [[Paragraph(student.student_name, para_style)]]
                        table = Table(stud_name, colWidths=[130], rowHeights=100, style=style)   
                        table.wrapOn(p, 200, 400)
                        table.drawOn(p, 125, y1-10)
                        heads = student.applicable_fees_heads.all()
                        for head in heads:
                            data = [[Paragraph(head.name, para_style)]]
                            table = Table(data, colWidths=[200], rowHeights=100, style=style)       
                            try:
                                fees_payment = FeesPayment.objects.get(fee_structure=fees_structure, student=student)
                                fees_payment_heads = fees_payment.payment_heads.filter(fees_head=head)
                                if fees_payment_heads.count() == 0:
                                    installment = head.installments.filter(name='Late Payment')
                                    if installment.count() == 0:
                                        installment = head.installments.filter(name='Standard Payment')
                                        if installment.count() == 0:
                                            installment = head.installments.filter(name='Early Payment')
                                    if installment.count() > 0:
                                        if installment[0].end_date < current_date:
                                            # p.drawString(250, y1, head.name)
                                            table.wrapOn(p, 200, 400)
                                            table.drawOn(p, 245, y1-10)
                                            p.drawString(450, y1, str(head.amount))
                                            p.drawString(550, y1, str(0))
                                            for installment in head.installments.all():
                                                p.drawString(620, y1, installment.name)
                                                p.drawString(750, y1, installment.start_date.strftime('%d/%m/%Y'))
                                                p.drawString(840, y1, installment.end_date.strftime('%d/%m/%Y'))
                                                p.drawString(920, y1, str(installment.fine_amount))
                                                y1 = y1 - 25
                                                if y1 <= 135:
                                                    y1 = y - 130
                                                    p.showPage()
                                                    p = header(p, y)
                                                    p.setFontSize(12)
                                else:
                                    if fees_payment_heads[0].paid_fee_amount != head.amount:
                                        installment = head.installments.filter(name='Late Payment')
                                        if installment.count() == 0:
                                            installment = head.installments.filter(name='Standard Payment')
                                            if installment.count() == 0:
                                                installment = head.installments.filter(name='Early Payment')
                                        if installment:
                                            if installment[0].end_date < current_date:
                                                table.wrapOn(p, 200, 400)
                                                table.drawOn(p, 245, y1-10)
                                                p.drawString(450, y1, str(head.amount))
                                                p.drawString(550, y1, str(fees_payment_heads[0].paid_fee_amount))
                                                for installment in head.installments.all():
                                                    p.drawString(620, y1, installment.name)
                                                    p.drawString(750, y1, installment.start_date.strftime('%d/%m/%Y'))
                                                    p.drawString(840, y1, installment.end_date.strftime('%d/%m/%Y'))
                                                    p.drawString(920, y1, str(installment.fine_amount))
                                                    y1 = y1 - 25
                                                    if y1 <= 135:
                                                        y1 = y - 130
                                                        p.showPage()
                                                        p = header(p, y)
                                                        p.setFontSize(12)
                            except Exception as ex:
                                installment = head.installments.filter(name='Late Payment')
                                if installment.count() == 0:
                                    installment = head.installments.filter(name='Standard Payment')
                                    if installment.count() == 0:
                                        installment = head.installments.filter(name='Early Payment')
                                if installment.count() > 0:
                                    if installment[0].end_date < current_date:
                                        # p.drawString(250, y1, head.name)
                                        table.wrapOn(p, 200, 400)
                                        table.drawOn(p, 245, y1-10)
                                        p.drawString(450, y1, str(head.amount))
                                        p.drawString(550, y1, str(0))
                                        for installment in head.installments.all():
                                            p.drawString(620, y1, installment.name)
                                            p.drawString(750, y1, installment.start_date.strftime('%d/%m/%Y'))
                                            p.drawString(840, y1, installment.end_date.strftime('%d/%m/%Y'))
                                            p.drawString(920, y1, str(installment.fine_amount))
                                            y1 = y1 - 25
                                            if y1 <= 135:
                                                y1 = y - 130
                                                p.showPage()
                                                p = header(p, y)
                                                p.setFontSize(12)
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
        report_type = request.GET.get('report_filtering_option', '')
        if not report_type:
            return render(request, 'report/fee_collected_report.html',{})
        else:
            if report_type == 'batch_wise':
                course = request.GET.get('course','')
                batch = request.GET.get('batch','')
                course = Course.objects.get(id=course)
                batch = Batch.objects.get(id=batch)
                from_date = request.GET.get('from', '')
                to_date = request.GET.get('to', '')
                p.drawCentredString(500, y-60, "Batch Wise Fee Report") 
                p.drawString(50, y - 100, "Course")
                p.drawString(100, y - 100, ":")
                if batch.branch:
                    branch_name = batch.branch.branch
                else:
                    branch_name = ''
                p.drawString(120, y - 100, course.course+" "+ branch_name)
                p.drawString(730, y - 100, "Batch")  
                p.drawString(780, y - 100, ":")
                p.drawString(800, y - 100, str(batch.start_date)+"-"+str(batch.end_date)) 
                p.drawString(50, y - 120, "From")
                p.drawString(100, y - 120, ":")
                p.drawString(120, y - 120, str(datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(50, y - 140, "To")  
                p.drawString(100, y - 140, ":")
                p.drawString(120, y - 140, str(datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                j = 170
                p.drawString(50, y - j, "UID")
                p.drawString(100, y - j, "Student Name")
                p.drawString(250, y - j, "Fee Head")
                p.drawString(400, y - j, "Payment Type")
                p.drawString(530, y - j, "Amount Paid")
                p.drawString(630, y - j, "Total Amount")
                p.drawString(730, y - j, "Fine")
                p.drawString(800, y - j, "Date of Payment")
                students = Student.objects.filter(course=course, batch=batch)
                j = 200     
                total_amount = 0
                for student in students:
                    try:
                        student_fees = FeesPaymentHead.objects.filter(student=student, paid_date__range=[from_date, to_date])
                        for fee_payment in student_fees:
                            total_amount = total_amount +  fee_payment.total_amount
                            p.drawString(50, y - j, str(student.unique_id))
                            p.drawString(100, y - j, str(student.student_name))
                            p.drawString(250, y - j, fee_payment.fees_head.name)   
                            p.drawString(400, y - j, fee_payment.installment.name)  
                            p.drawString(530, y - j, str(fee_payment.total_amount)) 
                            p.drawString(630, y - j, str(fee_payment.fees_head.amount))  
                            p.drawString(730, y - j, str(fee_payment.fine))  
                            p.drawString(800, y - j, str(fee_payment.paid_date.strftime('%d-%m-%Y'))) 
                            j = j + 30
                            if j > 1110:
                                j = 0
                                p.showPage()
                    except:
                        pass
                j = j + 20
                p.drawString(50, y - j, "Total amount collected ")
                p.drawString(200, y - j, ":")
                p.drawString(230, y - j, str(total_amount))

            elif report_type == 'all':
                from_date = request.GET.get('from', '')
                to_date = request.GET.get('to', '')
                p.drawCentredString(500, y-60, "Date Wise Fee Report") 
                p.drawString(50, y - 100, "From")
                p.drawString(100, y - 100, ":")
                p.drawString(120, y - 100, str(datetime.strptime(from_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                p.drawString(50, y - 120, "To")  
                p.drawString(100, y - 120, ":")
                p.drawString(120, y - 120, str(datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%m-%y')))
                j = 160
                p.drawString(50, y - j, "UID")
                p.drawString(100, y - j, "Student Name")
                p.drawString(250, y - j, "Fee Head")
                p.drawString(400, y - j, "Payment Type")
                p.drawString(530, y - j, "Amount Paid")
                p.drawString(630, y - j, "Total Amount")
                p.drawString(730, y - j, "Fine")
                p.drawString(800, y - j, "Date of Payment")
                total_amount = 0
                j = 190
                try:
                    student_fees = FeesPaymentHead.objects.filter(paid_date__range=[from_date, to_date]).order_by('paid_date')
                    for fee_payment in student_fees:
                        total_amount = total_amount + fee_payment.total_amount
                        p.drawString(50, y - j, str(fee_payment.student.unique_id))
                        p.drawString(100, y - j, str(fee_payment.student.student_name))
                        p.drawString(250, y - j, fee_payment.fees_head.name)   
                        p.drawString(400, y - j, fee_payment.installment.name)  
                        p.drawString(530, y - j, str(fee_payment.total_amount)) 
                        p.drawString(630, y - j, str(fee_payment.fees_head.amount))  
                        p.drawString(730, y - j, str(fee_payment.fine))  
                        p.drawString(800, y - j, str(fee_payment.paid_date.strftime('%d-%m-%Y'))) 
                        j = j + 30
                        if j > 1110:
                            j = 0
                            p.showPage()
                except:
                    pass
                j = j + 20
                p.drawString(50, y - j, "Total amount collected ")
                p.drawString(200, y - j, ":")
                p.drawString(230, y - j, str(total_amount))
            p.save()
            return response


   
           
