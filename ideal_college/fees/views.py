
import simplejson
import ast
import datetime as dt

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from fees.models import *
from datetime import datetime
from report.views import header


class CreateFeesStructure(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'fees/fees_structure.html', {})

    def post(self, request, *args, **kwargs):
        status_code = 200
        if request.is_ajax():
            fees_structure_details = ast.literal_eval(request.POST['fee_structure'])
            course = Course.objects.get(id = fees_structure_details['course'])
            batch = Batch.objects.get(id = fees_structure_details['batch'])
            try:
                fee_structure = FeesStructure.objects.get(course=course,batch=batch)
                res = {
                    'result': 'error',
                    'message': 'Fees Structure already existing'
                }
            except Exception:
                fee_structure = FeesStructure.objects.create(course=course,batch=batch)
                fee_head_details = fees_structure_details['fees_head_details']
                for fee_head in fee_head_details:
                    fee_structure_head = FeesStructureHead()
                    fee_structure_head.name = fee_head['head']
                    fee_structure_head.amount = fee_head['amount']
                    fee_structure_head.save()
                    for installment_details in fee_head['payment']:
                        if installment_details['type']:
                            installment = Installment()
                            installment.name = installment_details['type']
                            installment.start_date = datetime.strptime(installment_details['start_date'], '%d/%m/%Y')
                            installment.end_date = datetime.strptime(installment_details['end_date'], '%d/%m/%Y')                        
                            if installment_details['fine']:
                                installment.fine_amount = installment_details['fine']
                            else:
                                installment.fine_amount = 0
                            installment.save()
                            fee_structure_head.installments.add(installment)
                    fee_structure.head.add(fee_structure_head)

                res = {
                    'result': 'ok',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class EditFeesStructure(View):
   
    def get(self, request, *args, **kwargs):
        
        fees_structure_id = kwargs['fees_structure_id']
        ctx_fees_structure = []
        ctx_fees_head = []
        status = 200
        if request.is_ajax():
            fees = FeesStructure.objects.get(id = fees_structure_id)
            heads = fees.head.all()
            i = 0
            for head in heads:
                ctx_installments = []
                j  = 0
                for installment in head.installments.all():
                    ctx_installments.append({
                        'id': installment.id,
                        'type': installment.name,
                        'start_date': installment.start_date.strftime('%d/%m/%Y') if installment.start_date else '',
                        'end_date': installment.end_date.strftime('%d/%m/%Y') if installment.end_date else '',
                        'fine_amount': installment.fine_amount,
                        'start_date_id': 'start_date'+str(i)+str(j),
                        'end_date_id': 'end_date'+str(i)+str(j),
                        'is_not_late_payment': 'false' if installment.name == 'Late Payment' else 'true',
                     })
                    j = j + 1

                ctx_fees_head.append({
                    'id': head.id,
                    'head': head.name,
                    'amount': head.amount,
                    'installments': ctx_installments,
                    'shrink': False,
                    'removed_installments': []
                })
                i = i + 1
            ctx_fees_structure.append({
                'course': fees.course.course,
                'batch': fees.batch.branch.branch if fees.batch.branch else '' + ' ' + str(fees.batch.start_date) + '-' + str(fees.batch.end_date),           
                'fees_head': ctx_fees_head,
            })
            res = {
                'result': 'ok',
                'fees_structure': ctx_fees_structure,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        context = {
            'fee_structure_id': fees_structure_id,
        }
        return render(request, 'fees/edit_fees_structure_details.html', context)

    def post(self, request, *args, **kwargs):

        status = 200
        fees_structure_id = kwargs['fees_structure_id']
        fee_structure = FeesStructure.objects.get(id=fees_structure_id)
        fees_structure_details = ast.literal_eval(request.POST['fee_structure'])
        removed_heads = fees_structure_details['removed_heads']
        for head in removed_heads:
            try:
                fees_head = FeesStructureHead.objects.get(id=head['id'])
                fees_head.delete()
            except: 
                pass
        fee_head_details = fees_structure_details['fees_head']
        for fee_head in fee_head_details:
            try:
                fee_structure_head = FeesStructureHead.objects.get(id=fee_head['id'])
            except:
                fee_structure_head = FeesStructureHead()
            removed_installments = fee_head['removed_installments']
            for installment in removed_installments:
                installment_obj = Installment.objects.get(id=installment['id'])
                installment_obj.delete()
            fee_structure_head.name = fee_head['head']
            fee_structure_head.amount = fee_head['amount']
            fee_structure_head.save()
            for installment_details in fee_head['installments']:
                if installment_details['type']:
                    try:
                        installment = Installment.objects.get(id=installment_details['id'])
                    except:
                        installment = Installment()
                    installment.name = installment_details['type']
                    installment.start_date = datetime.strptime(installment_details['start_date'], '%d/%m/%Y')
                    installment.end_date = datetime.strptime(installment_details['end_date'], '%d/%m/%Y')                        
                    if installment_details['fine_amount']:
                        installment.fine_amount = installment_details['fine_amount']
                    else:
                         installment.fine_amount = 0       
                    installment.save()
                    fee_structure_head.installments.add(installment)
            fee_structure.head.add(fee_structure_head)
        res = {
            'result': 'ok',
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class DeleteFeesStructure(View):
    def get(self, request, *args, **kwargs):

        fees_structure_id = kwargs['fees_structure_id']       
        fees = FeesStructure.objects.get(id=fees_structure_id)                          
        fees.delete()
        return HttpResponseRedirect(reverse('list_fees_structure'))

class ListFeesStructure(View):
    def get(self, request, *args, **kwargs):
        course = request.GET.get('course', '')
        batch = request.GET.get('batch', '')
        if course and batch:
            fees_structures = FeesStructure.objects.filter(course__id=course, batch__id=batch)  
        else:
            fees_structures = FeesStructure.objects.all()  
        if request.is_ajax():
            structure_list = []
            for fees_structure in fees_structures:
                structure_list.append({
                    'course': fees_structure.course.course,
                    'batch': str(fees_structure.batch.start_date) + ' - ' + str(fees_structure.batch.end_date) +( ' - ' + fees_structure.batch.branch.branch if fees_structure.batch and fees_structure.batch.branch else ''),
                    'id': fees_structure.id
                })
            res = {
                'result': 'ok',
                'fees_structures': structure_list
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

        ctx = {
            'fees_structures': fees_structures
        }
        return render(request, 'fees/list_fees_structure.html',ctx)
# Fees structure end

# Fees head start
class AddFeesHead(View):
    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, 'fees/add_fees_head.html',ctx)

    def post(self, request, *args, **kwargs):
        status_code = 200
        if request.is_ajax():
            fee_head_details = ast.literal_eval(request.POST['fee_head_details'])
            try:
                fees_head_id = request.POST['fees_head_id']
                fees_head = FeesHead.objects.get(id=fees_head_id)
                fees_head.amount = fee_head_details['amount']
                fees_head.name = fee_head_details['head']
                fees_head.save()
                res = {
                    'result': 'ok',
                }
            except Exception as ex:
                try:
                    head = FeesHead.objects.get(name=fee_head_details['head'])
                    res = {
                        'result': 'error: ' + str(ex),
                        'message': 'Head Already Existing'
                    }
                except Exception:
                    head = FeesHead.objects.create(name=fee_head_details['head'], amount=fee_head_details['amount'])
                    res = {
                        'result': 'ok',
                    }
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class EditFeesHead(View):
    def get(self, request, *args, **kwargs):
        status = 200
        fees_head = FeesHead.objects.get(id=kwargs['fees_head_id'])
        ctx_fees_head = []
        if request.is_ajax():
            ctx_fees_head.append({
                'id': fees_head.id,
                'head': fees_head.name,
                'amount': fees_head.amount,
            })
            res = {
                'result': 'ok',
                'fees_head': ctx_fees_head,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'fees/edit_fees_head.html', {'fees_head_id': kwargs['fees_head_id']})

class DeleteFeesHead(View):
    def get(self, request, *args, **kwargs):
        fees_head = FeesHead.objects.get(id=kwargs['fees_head_id'])
        fees_head.delete()
        return HttpResponseRedirect(reverse('fees_heads'))


class FeesHeadList(View):
    def get(self, request, *args, **kwargs):

        heads = FeesHead.objects.all()
        if request.is_ajax():
            head_list = []
            for head in heads:
                head_list.append({
                    'id': head.id,
                    'name': head.name,
                    'amount': head.amount
                })
            res = {
                    'result': 'Ok',
                    'fees_heads': head_list
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status = 200, mimetype="application/json")
        context = {
            'heads': heads
        }
        return render(request, 'fees/fee_head_list.html', context)

class FeesPaymentSave(View):

    def get(self, request, *args, **kwargs):
        current_date = dt.datetime.now().date()
        context = {
            
           'current_date': current_date.strftime('%d/%m/%Y'),

        }
        return render(request, 'fees/fees_payment.html',context)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            status_code = 200 
            try:
                fees_payment_details = ast.literal_eval(request.POST['fees_payment'])
                fees_structure = FeesStructure.objects.filter(course__id=fees_payment_details['course_id'], batch__id=fees_payment_details['batch_id'])
                student = Student.objects.get(id=fees_payment_details['student_id'])
                fees_payment, created = FeesPayment.objects.get_or_create(fee_structure=fees_structure[0], student=student)
                fees_head = FeesStructureHead.objects.get(id=fees_payment_details['head_id'])
                if float(fees_payment_details['paid_amount']) > 0:
                    fees_payment_head, created = FeesPaymentHead.objects.get_or_create(student=student, fees_head=fees_head)
                    fees_payment_head.installment = Installment.objects.get(id=fees_payment_details['installment_id'])
                    if created:
                        fees_payment_head.total_amount = fees_payment_details['paid_amount']
                        if float(fees_payment_details['fine']) > float(fees_payment_details['paid_amount']):
                            fees_payment_head.fine = float(fees_payment_details['paid_amount'])
                        else:
                            if float(fees_payment_details['fine']) > 0:
                                fees_amount = float(fees_payment_details['paid_amount']) - float(fees_payment_details['fine'])
                                fees_payment_head.fine = float(fees_payment_details['paid_amount']) - float(fees_amount)
                        paid_fees_amount = float(fees_payment_head.total_amount) - float(fees_payment_head.fine)
                        if paid_fees_amount > 0:
                            fees_payment_head.paid_fee_amount = paid_fees_amount 
                    else:
                        fees_payment_head.total_amount = float(fees_payment_details['paid_amount']) + float(fees_payment_head.total_amount)
                        if float(fees_payment_details['fine']) > float(fees_payment_details['paid_amount']):
                            fees_payment_head.fine = float(fees_payment_details['paid_amount']) + float(fees_payment_head.fine)
                        else:
                            if float(fees_payment_details['fine']) > 0:
                                fees_amount = float(fees_payment_details['paid_amount']) - float(fees_payment_details['fine'])
                                fees_payment_head.fine = float(fees_payment_head.fine) + (float(fees_payment_details['paid_amount']) - float(fees_amount))
                        paid_fees_amount = float(fees_payment_head.total_amount) - float(fees_payment_head.fine)
                        if paid_fees_amount > 0:
                            fees_payment_head.paid_fee_amount = paid_fees_amount
                    fees_payment_head.paid_date = datetime.strptime(fees_payment_details['paid_date'], '%d/%m/%Y')
                    try:
                        fee_paid = FeesPaid()
                        fee_paid.fees_payment = fees_payment_head
                        fee_paid.amount = float(fees_payment_details['paid_amount'])
                        fee_paid.paid_date = datetime.strptime(fees_payment_details['paid_date'], '%d/%m/%Y')
                        fee_paid.installment = Installment.objects.get(id=fees_payment_details['installment_id'])
                        fee_paid.fine = float(fees_payment_details['fine'])
                        fee_paid.save()
                    except Exception as Ex:
                        print str(Ex)
                    fees_payment_head.save()
                    fees_payment.payment_heads.add(fees_payment_head)
                    fees_payment.save()
                if student.unique_id != fees_payment_details['u_id']:
                    student.unique_id = fees_payment_details['u_id']
                    student.save()
                res = {
                    'result': 'ok',
                }
            except Exception as Ex:
                print str(Ex)
                res = {
                    'result': 'error: '+str(Ex),
                    'message': 'Already Paid',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class GetFeeStructureHeadList(View):

    def get(self, request, *args, **kwargs):

        course_id = kwargs['course_id']
        batch_id = kwargs['batch_id']
        student_id = kwargs['student_id']
        if request.is_ajax():
            fee_structure = FeesStructure.objects.filter(course__id=course_id, batch__id=batch_id)
            student = Student.objects.get(id=student_id)
            ctx_heads_list = []
            if fee_structure.count() > 0:
                heads = student.applicable_fees_heads.all()
                for head in heads:
                    try:
                        fees_payment = FeesPayment.objects.get(fee_structure=fee_structure, student__id=student_id)
                        fees_payment_heads = fees_payment.payment_heads.filter(fees_head=head)
                        if fees_payment_heads.count() == 0:
                            ctx_heads_list.append({
                                'id': head.id,
                                'head': head.name,
                                'paid_fee_amount': 0,
                                'balance': head.amount,
                                'head_amount': head.amount,
                            })
                        else:
                            if fees_payment_heads[0].paid_fee_amount != head.amount:
                               ctx_heads_list.append({
                                    'id': head.id,
                                    'head': head.name,
                                    'paid_fee_amount': fees_payment_heads[0].paid_fee_amount,
                                    'balance': head.amount - fees_payment_heads[0].paid_fee_amount,
                                    'head_amount': head.amount,
                                }) 
                    except Exception as ex:
                        ctx_heads_list.append({
                            'id': head.id,
                            'head': head.name,
                            'paid_fee_amount': 0,
                            'balance': head.amount,
                            'head_amount': head.amount,
                        })
            res = {
                'result': 'ok',
                'heads': ctx_heads_list,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')


class GetPaidFeeHeads(View):

    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('student','')
        try:
            payment_heads_list = []
            fees_payment = FeesPayment.objects.get(student__id=student_id)
            payment_heads = fees_payment.payment_heads.all()
            for payment_head in payment_heads:
                payment_heads_list.append({
                    'id': payment_head.fees_head.id,
                    'name': payment_head.fees_head.name,
                    })
            res = {
                'result': 'ok',
                'paid_heads': payment_heads_list,
            }
        except:
            res = {
                'result': 'error'
            }
        status = 200
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')


class ListOutStandingFees(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'fees/list_outstanding_fees.html',{})

class GetOutStandingFeesDetails(View):

    def get(self, request, *args, **kwargs):

        current_date = datetime.now().date()
        status = 200
        if request.is_ajax():
            filtering_option = request.GET.get('filtering_option','')
            try:
                fees_structure = FeesStructure.objects.get(course__id=request.GET.get('course', ''), batch__id=request.GET.get('batch', ''))
            except:
                res = {
                    'result': 'error',
                    'message': 'No Fees Structure for this batch',
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=status, mimetype='application/json')
            student_id = request.GET.get('student_id', '')
            ctx_fees_details = []
            if request.GET.get('fees_type','') == 'course':
                if filtering_option == 'student_wise':
                    student = Student.objects.get(id=student_id)
                    ctx_fees_head_details = []
                    ctx_heads_list = []
                    heads = student.applicable_fees_heads.all()
                    for head in heads:
                        ctx_installments = []
                        for installment in head.installments.all():
                            ctx_installments.append({
                                'type': installment.name,
                                'start_date': installment.start_date.strftime('%d/%m/%Y'),
                                'end_date': installment.end_date.strftime('%d/%m/%Y'),
                                'fine': installment.fine_amount,
                            })
                        try:
                            fees_payment = FeesPayment.objects.get(fee_structure=fees_structure, student__id=student_id)
                            fees_payment_heads = fees_payment.payment_heads.filter(fees_head=head)
                            if fees_payment_heads.count() == 0:
                                installment = head.installments.filter(name='Late Payment')
                                if installment.count() == 0:
                                    installment = head.installments.filter(name='Standard Payment')
                                    if installment.count() == 0:
                                        installment = head.installments.filter(name='Early Payment')
                                if installment.count() > 0:
                                    if installment[0].end_date < current_date:
                                        ctx_heads_list.append({
                                            'id': head.id,
                                            'head': head.name,
                                            'amount': head.amount,
                                            'installments': ctx_installments,
                                            'paid_fee_amount': 0,
                                            'balance': head.amount,
                                        })
                            else:
                                if fees_payment_heads[0].paid_fee_amount != head.amount:
                                    installment = head.installments.filter(name='Late Payment')
                                    if installment.count() == 0:
                                        installment = head.installments.filter(name='Standard Payment')
                                        if installment.count() == 0:
                                            installment = head.installments.filter(name='Early Payment')
                                    if installment:
                                        ctx_heads_list.append({
                                            'id': head.id,
                                            'head': head.name,
                                            'amount': head.amount,
                                            'installments': ctx_installments,
                                            'paid_fee_amount': fees_payment_heads[0].paid_fee_amount,
                                            'balance': head.amount - fees_payment_heads[0].paid_fee_amount,
                                        }) 
                        except Exception as ex:
                            installment = head.installments.filter(name='Late Payment')
                            if installment.count() == 0:
                                installment = head.installments.filter(name='Standard Payment')
                                if installment.count() == 0:
                                    installment = head.installments.filter(name='Early Payment')
                            if installment.count() > 0:
                                if installment[0].end_date < current_date:
                                    ctx_heads_list.append({
                                        'id': head.id,
                                        'head': head.name,
                                        'amount': head.amount,
                                        'installments': ctx_installments,
                                        'paid_fee_amount': 0,
                                        'balance': head.amount,
                                    })
                    ctx_fees_details.append({
                        'head_details': ctx_heads_list,
                        'student_name': student.student_name,
                        'roll_no': student.roll_number,
                    })
                else:
                    students = Student.objects.filter(course__id=request.GET.get('course', ''), batch__id=request.GET.get('batch', '')).order_by('roll_number')
                    ctx_student_fees_details = []
                    for student in students:
                        ctx_fees_head_details = []
                        ctx_heads_list = []
                        heads = student.applicable_fees_heads.all()
                        for head in heads:
                            ctx_installments = []
                            for installment in head.installments.all():
                                ctx_installments.append({
                                    'type': installment.name,
                                    'start_date': installment.start_date.strftime('%d/%m/%Y'),
                                    'end_date': installment.end_date.strftime('%d/%m/%Y'),
                                    'fine': installment.fine_amount,
                                })
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
                                            ctx_heads_list.append({
                                                'id': head.id,
                                                'head': head.name,
                                                'amount': head.amount,
                                                'installments': ctx_installments,
                                                'paid_fee_amount': 0,
                                                'balance': head.amount,
                                            })
                                else:
                                    if fees_payment_heads[0].paid_fee_amount != head.amount:
                                        installment = head.installments.filter(name='Late Payment')
                                        if installment.count() == 0:
                                            installment = head.installments.filter(name='Standard Payment')
                                            if installment.count() == 0:
                                                installment = head.installments.filter(name='Early Payment')
                                        if installment:
                                            ctx_heads_list.append({
                                                'id': head.id,
                                                'head': head.name,
                                                'amount': head.amount,
                                                'installments': ctx_installments,
                                                'paid_fee_amount': fees_payment_heads[0].paid_fee_amount,
                                                'balance': head.amount - fees_payment_heads[0].paid_fee_amount,
                                            }) 
                            except Exception as ex:
                                installment = head.installments.filter(name='Late Payment')
                                if installment.count() == 0:
                                    installment = head.installments.filter(name='Standard Payment')
                                    if installment.count() == 0:
                                        installment = head.installments.filter(name='Early Payment')
                                if installment.count() > 0:
                                    if installment[0].end_date < current_date:
                                        ctx_heads_list.append({
                                            'id': head.id,
                                            'head': head.name,
                                            'amount': head.amount,
                                            'installments': ctx_installments,
                                            'paid_fee_amount': 0,
                                            'balance': head.amount,
                                        })
                        if len(ctx_heads_list) != 0:
                            ctx_student_fees_details.append({
                                'head_details': ctx_heads_list,
                                'name': student.student_name,
                                'roll_no': student.roll_number,
                            })
                    ctx_fees_details.append({
                        'students': ctx_student_fees_details,
                    })    
            else:
                heads = FeesHead.objects.all()
                if filtering_option == 'student_wise':
                    ctx_fees_head_details = []
                    for head in heads:
                        try:
                            student = Student.objects.get(id=student_id)
                            fees_payment = CommonFeesPayment.objects.get(head=head, student__id=student_id)
                            if fees_payment.paid_amount < head.amount:
                                ctx_fees_head_details.append({
                                    'id': head.id,
                                    'name': head.name,
                                    'amount': head.amount,
                                    'balance': float(head.amount) - float(fees_payment.paid_amount),
                                    'paid_head_amount': fees_payment.paid_amount,
                                })
                        except:
                            ctx_fees_head_details.append({
                                'id': head.id,
                                'name': head.name,
                                'amount': head.amount,
                                'balance': float(head.amount),
                                'paid_head_amount': 0,
                            })
                    ctx_fees_details.append({
                        'head_details': ctx_fees_head_details,
                        'student_name': student.student_name,
                        'roll_no': student.roll_number
                    })
                else:
                    students = Student.objects.filter(course__id=request.GET.get('course', ''), batch__id=request.GET.get('batch', '')).order_by('roll_number')
                    ctx_student_fees_details = []
                    for student in students:
                        ctx_fees_head_details = []
                        for head in heads:
                            try:
                                fees_payment = CommonFeesPayment.objects.get(head=head, student__id=student_id)
                                if fees_payment.paid_amount < head.amount:
                                    ctx_fees_head_details.append({
                                        'id': head.id,
                                        'name': head.name,
                                        'amount': head.amount,
                                        'balance': float(head.amount) - float(fees_payment.paid_amount),
                                        'paid_head_amount': fees_payment.paid_amount,
                                    })
                            except:
                                ctx_fees_head_details.append({
                                    'id': head.id,
                                    'name': head.name,
                                    'amount': head.amount,
                                    'balance': float(head.amount),
                                    'paid_head_amount': 0,
                                })
                        ctx_student_fees_details.append({
                            'head_details':ctx_fees_head_details,
                            'name': student.student_name,
                            'roll_no': student.roll_number,
                        })
                    ctx_fees_details.append({
                        'students': ctx_student_fees_details,
                    })
            res = {
                'result':'ok',
                'fees_details': ctx_fees_details,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class CommonFeesPaymentSave(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'fees/common_fees_payment.html',{'current_date': datetime.now().date().strftime('%d/%m/%Y')})

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            status_code = 200 
            try:
                fees_payment_details = ast.literal_eval(request.POST['fees_payment']) 
                head = FeesHead.objects.get(id=fees_payment_details['head_id'])
                fees_payment = CommonFeesPayment()
                fees_payment.head = head
                fees_payment.paid_amount = fees_payment_details['paid_amount']
                fees_payment.student = fees_payment_details['name']
                fees_payment.paid_date = datetime.strptime(fees_payment_details['paid_date'], '%d/%m/%Y')
                fees_payment.save()
                res = {
                    'result': 'ok',
                }
            except Exception as Ex:
                res = {
                    'result': 'error: '+str(Ex),
                    'message': 'Already Paid',
                }

            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class GetFeesHeadList(View):

    def get(self, request, *args, **kwargs):

        student_id = kwargs['student_id']
        if request.is_ajax():
            heads = FeesHead.objects.all()
            ctx_fees_head_details = []
            for head in heads:
                try:
                    fees_payment = CommonFeesPayment.objects.get(head=head, student__id=student_id)
                    if fees_payment.paid_amount < head.amount:
                        ctx_fees_head_details.append({
                            'id': head.id,
                            'name': head.name,
                            'amount': head.amount,
                            'balance': float(head.amount) - float(fees_payment.paid_amount),
                            'paid_head_amount': fees_payment.paid_amount,
                        })
                except:
                    ctx_fees_head_details.append({
                        'id': head.id,
                        'name': head.name,
                        'amount': head.amount,
                        'balance': float(head.amount),
                        'paid_head_amount': 0,
                    })
            res = {
                'result': 'ok',
                'heads': ctx_fees_head_details,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class IsFeesStructureExists(View):

    def get(self, request, *args, **kwargs):

        course_id = kwargs['course_id']
        batch_id = kwargs['batch_id']
        status = 200
        if request.is_ajax():
            try:
                FeesStructure.objects.get(course__id=course_id, batch__id=batch_id)
                res = {
                    'result': 'error',
                    'message': 'Fees Structure already exists',
                }
            except Exception as ex:
                res = {
                    'result': 'ok'
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class GetApplicableFeeStructureHeads(View):
    def get(self, request, *args, **kwargs):

        course_id = kwargs['course_id']
        batch_id = kwargs['batch_id']
        if request.is_ajax():
            fee_structure = FeesStructure.objects.filter(course__id=course_id, batch__id=batch_id)
            heads_list = []
            if fee_structure.count() > 0:
                heads = fee_structure[0].head.all()
                for head in heads:
                    heads_list.append({
                        'head': head.name,
                        'amount':head.amount, 
                        'id': head.id ,            
                    })
            res = {
                'result': 'ok',
                'heads': heads_list,
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class GetFeesHeadDateRanges(View):

    def get(self, request, *args, **kwargs):

        head_id = request.GET.get('head_id', '')
        student_id = request.GET.get('student_id', '')
        student = Student.objects.get(id=student_id, applicable_to_special_fees= True)
        paid_date = datetime.strptime(request.GET.get('paid_date', ''), '%d/%m/%Y').date()
        head = FeesStructureHead.objects.get(id=head_id)
        installments = head.installments.filter(start_date__lte=paid_date, end_date__gte=paid_date)
        head_installments = []
        try:
            fees_payment_heads = FeesPaymentHead.objects.filter(fees_head=head, student__id=student_id)
            if fees_payment_heads.count() == 0:
                paid_fee_amount = 0
                balance = head.amount
                start_date = None
                paid_fine = 0
            else:
                paid_fee_amount = fees_payment_heads[0].paid_fee_amount
                balance = head.amount - fees_payment_heads[0].paid_fee_amount
                paid_fine = fees_payment_heads[0].fine
                paid_installment_details = head.installments.filter(start_date__lte=fees_payment_heads[0].paid_date, end_date__gte=fees_payment_heads[0].paid_date)
        except Exception as ex:
            print str(ex)
            paid_fee_amount = 0
            balance = head.amount
            start_date = None
            paid_fine = 0
        if installments.count() > 0:
            for installment in installments:
                fine = 0
                if installment.name == 'Late Payment':
                    no_of_days = (paid_date - installment.start_date).days
                    if no_of_days >= 0:
                        no_of_days = no_of_days + 1
                        fine_amount = no_of_days*installment.fine_amount
                        fine = fine_amount - paid_fine
                head_installments.append({
                    'name': installment.name,
                    'id': installment.id,
                    'fine': fine,
                    'message': 'ok',
                    'balance': float(balance) + float(fine),
                    'paid_head_amount': paid_fee_amount,
                })
        else:
            try:
                installment = head.installments.filter(end_date__lte=paid_date, name='Late Payment')
                if installment.count() == 0:
                    installment = head.installments.filter(end_date__lte=paid_date, name='Standard Payment')
                    if installment.count() == 0:
                        installment = head.installments.filter(end_date__lte=paid_date, name='Early Payment')
            except Exception as ex:
                try:
                    installment = head.installments.filter(end_date__lte=paid_date, name='Standard Payment')
                except Exception as ex:
                    installment = head.installments.filter(end_date__lte=paid_date, name='Early Payment')
            if installment:
                no_of_days = (paid_date - installment[0].start_date).days
                if no_of_days >= 0:
                    no_of_days = no_of_days + 1
                    fine = no_of_days*installment[0].fine_amount
                    fine = fine - paid_fine
                    head_installments.append({
                        'name': installment[0].name,
                        'id': installment[0].id,
                        'fine': fine,
                        'message': 'ok',
                        'balance': float(balance) + float(fine),
                        'paid_head_amount': paid_fee_amount,
                    })
        res = {
            'result': 'ok',
            'head_details': head_installments,
            'fees_amount': balance,
            'head_amount': head.amount,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
        

class FeesReceipt(View):

    def get(self, request, *args, **kwargs):
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1250))
        y = 1150
        p = header(p, y)
        p.setFont("Helvetica", 14)  
        current_date = datetime.now().date()
        head = request.GET.get('head', '')
        if not head:
            return render(request, 'fees/fee_receipt.html',{})
        else:
            student_id = request.GET.get('student','')
            student = Student.objects.get(id=student_id)
            p.setFontSize(15)
            p.drawCentredString(500, y-60, "Fee Payment Receipt")  
            p.setFontSize(13)
            p.drawString(300, y - 100, "Student Name")
            p.drawString(450, y - 100, ":")
            p.drawString(550, y - 100, student.student_name)
            p.drawString(300, y - 120, "Unique ID")  
            p.drawString(450, y - 120, ":")          
            p.drawString(550, y - 120, str(student.unique_id))
            p.drawString(300, y - 140, "Roll Number")
            p.drawString(450, y - 140, ":")          
            p.drawString(550, y - 140, str(student.roll_number))
            p.drawString(300, y - 160, "Course")
            p.drawString(450, y - 160, ":") 
            if student.batch.branch:
                branch_name = student.batch.branch.branch
            else:
                branch_name = ''
            p.drawString(550, y - 160, student.course.course+" "+ branch_name);
            p.drawString(300, y - 180, "Batch")
            p.drawString(450, y - 180, ":")
            p.drawString(550, y - 180, str(student.batch.start_date)+"-"+str(student.batch.end_date))
            if head == 'All':
                student_fee = FeesPayment.objects.get(student=student)
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
            elif request.GET.get('amount',''):
                fee_payment = FeesPaymentHead.objects.get(student = student,fees_head__id=head)
                p.drawString(300, y - 220, "Fee Head")
                p.drawString(450, y - 220, ":")
                p.drawString(550, y - 220, fee_payment.fees_head.name)  
                p.drawString(300, y - 240, "Payment Type")
                p.drawString(450, y - 240, ":")
                p.drawString(550, y - 240, fee_payment.installment.name) 
                if request.GET.get('amount',''):
                    p.drawString(300, y - 260, "Amount Paid")
                    p.drawString(450, y - 260, ":")
                    p.drawString(550, y - 260, str(request.GET.get('amount','')))
                    p.drawString(300, y - 280, "Total Amount Paid")
                    p.drawString(450, y - 280, ":")
                    p.drawString(550, y - 280, str(fee_payment.total_amount))
                    y = y - 280
                else:
                    p.drawString(300, y - 260, "Amount Paid")
                    p.drawString(450, y - 260, ":")
                    p.drawString(550, y - 260, str(fee_payment.total_amount))
                    y = y - 260
                p.drawString(300, y - 20, "Fee Amount")
                p.drawString(450, y - 20, ":")
                p.drawString(550, y - 20, str(fee_payment.fees_head.amount))
                p.drawString(300, y - 40, "Fine")
                p.drawString(450, y - 40, ":")
                p.drawString(550, y - 40, str(request.GET.get('fine','')))
                p.drawString(300, y - 60, "Date of Payment")
                p.drawString(450, y - 60, ":")
                p.drawString(550, y - 60, str(fee_payment.paid_date.strftime('%d-%m-%Y')))
            else:
                student_fee = FeesPayment.objects.get(student=student)
                fee_payment = FeesPaymentHead.objects.get(student = student,fees_head__id=head)
                print fee_payment
                p.drawString(300, y - 200, "Fee Head")
                p.drawString(450, y - 200, ":")          
                p.drawString(550, y - 200, fee_payment.fees_head.name)
                p.drawString(300, y - 220, "Total Amount")
                p.drawString(450, y - 220, ":")          
                p.drawString(550, y - 220, str(fee_payment.fees_head.amount))
                p.drawString(300, y - 240, "Amount Paid")
                p.drawString(450, y - 240, ":")          
                p.drawString(550, y - 240, str(fee_payment.total_amount))
                p.setFontSize(15)
                p.drawCentredString(500, y-280, "Fee Payment History")  
                p.setFontSize(13)
                p.drawString(50, y - 320, "#")
                p.drawString(150, y - 320, "Payment Type")
                p.drawString(420, y - 320, "Fine")
                p.drawString(550, y - 320, "Amount Paid")
                p.drawString(800, y - 320, "Date of Payment")
                j = 340
                tot_count = 0
                total_amount = 0
                fees_paids = FeesPaid.objects.filter(fees_payment=fee_payment)
                for fees_paid in fees_paids:
                    tot_count = tot_count + 1
                    total_amount = total_amount + fees_paid.amount
                    p.drawString(50, y - j, str(tot_count))
                    p.drawString(150, y - j, fees_paid.installment.name)   
                    p.drawString(420, y - j, str(fees_paid.fine)) 
                    p.drawString(550, y - j, str(fees_paid.amount))  
                    p.drawString(800, y - j, str(fees_paid.paid_date.strftime('%d-%m-%Y'))) 
                    j = j + 20
                    if j > 1110:
                        j = 0
                        p.showPage()
                j = j + 20
                p.drawString(50, y - j, "Total Amount Paid:")   
                p.drawString(200, y - j, ":") 
                p.drawString(250, y - j, str(total_amount)) 




            p.save()
            return response
