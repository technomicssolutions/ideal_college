
import simplejson
import ast
import datetime as dt

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from fees.models import *
from datetime import datetime

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
                'batch': fees.batch.branch.branch if fees.batch.branch else '' + ' ' + fees.batch.start_date + '-' + fees.batch.end_date,           
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
            fees_head = FeesStructureHead.objects.get(id=head['id'])
            fees_head.delete()
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
                fees_payment_head = FeesPaymentHead.objects.create(student=student, fees_head=fees_head)
                fees_payment_head.installment = Installment.objects.get(id=fees_payment_details['installment_id'])
                fees_payment_head.total_amount = fees_payment_details['total_amount']
                fees_payment_head.fine = fees_payment_details['fine']
                fees_payment_head.paid_date = datetime.strptime(fees_payment_details['paid_date'], '%d/%m/%Y')
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
                            })
                    except Exception as ex:
                        print str(ex)
                        ctx_heads_list.append({
                           'id': head.id,
                            'head': head.name,
                        })
            res = {
                'result': 'ok',
                'heads': ctx_heads_list,
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
                    heads = fees_structure.head.all()
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
                                        })
                        except Exception as ex:
                            print str(ex)
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
                        heads = fees_structure.head.all()
                        ctx_fees_head_details = []
                        for head in heads:
                            is_not_paid = False
                            ctx_installments = []
                            i = 0
                            for installment in head.installments.all():
                                try:
                                    fees_payment = FeesPayment.objects.get(fee_structure=fees_structure, student=student)
                                    fees_payment_installments = fees_payment.payment_installment.filter(installment=installment)
                                    if fees_payment_installments.count() > 0:
                                        if fees_payment_installments[0].installment_amount < installment.amount:
                                            is_not_paid = True
                                            ctx_installments.append({
                                                'id': installment.id,
                                                'amount':installment.amount,
                                                'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                                'fine_amount': installment.fine_amount,
                                                'name':'installment'+str(i + 1),
                                                'paid_installment_amount': fees_payment_installments[0].installment_amount,
                                                'balance': float(installment.amount) - float(fees_payment_installments[0].installment_amount),
                                            })
                                    elif fees_payment_installments.count() == 0:
                                        is_not_paid = True
                                        ctx_installments.append({
                                            'id': installment.id,
                                            'amount':installment.amount,
                                            'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                            'fine_amount': installment.fine_amount,
                                            'name':'installment'+str(i + 1),
                                            'paid_installment_amount': 0,
                                            'balance': float(installment.amount),
                                        })
                                except Exception:
                                    if current_date >= installment.due_date:
                                        is_not_paid = True
                                        ctx_installments.append({
                                            'id': installment.id,
                                            'amount':installment.amount,
                                            'due_date': installment.due_date.strftime('%d/%m/%Y'),
                                            'fine_amount': installment.fine_amount,
                                            'name':'installment'+str(i + 1),
                                            'paid_installment_amount': 0,
                                            'balance': float(installment.amount),
                                        })
                                i = i + 1
                            if is_not_paid:
                                ctx_fees_head_details.append({
                                    'head': head.name,
                                    'amount': head.amount,
                                    'no_installments': head.no_installments,
                                    'installments': ctx_installments,
                                })
                        ctx_student_fees_details.aGetFeeSppend({
                            'head_details':ctx_fees_head_details,
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
        paid_date = datetime.strptime(request.GET.get('paid_date', ''), '%d/%m/%Y').date()
        head = FeesStructureHead.objects.get(id=head_id)
        installments = head.installments.filter(start_date__lte=paid_date, end_date__gte=paid_date)
        head_installments = []
        if installments.count() > 0:
            for installment in installments:
                fine = 0
                if installment.name == 'Late Payment':
                    no_of_days = (paid_date - installment.start_date).days
                    fine = no_of_days*installment.fine_amount
                head_installments.append({
                    'name': installment.name,
                    'id': installment.id,
                    'fine': fine,
                    'message': 'ok'
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
                fine = no_of_days*installment[0].fine_amount
                head_installments.append({
                    'name': installment[0].name,
                    'id': installment[0].id,
                    'fine': fine,
                    'message': 'ok'
                })
        res = {
            'result': 'ok',
            'head_details': head_installments,
            'fees_amount': head.amount,
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')
        
            