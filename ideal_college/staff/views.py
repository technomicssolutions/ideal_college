
import simplejson
import ast

from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from staff.models import *
from datetime import datetime

class AddStaff(View):    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            status = 200            
            staff_details = ast.literal_eval(request.POST['staff'])
            try:
                staff = Staff.objects.get(staff_id=staff_details['staff_id'])
                res = {
                    'result': 'error',
                    'message': 'Staff already exists',
                }                
            except:
                try:
                    user = User.objects.get(username=staff_details['username'])
                    res = {
                        'result': 'error',
                        'message': 'Username already exists',
                    }
                    staff.delete()
                    response = simplejson.dumps(res)
                    return HttpResponse(response, status = status, mimetype="application/json")
                except Exception:
                    user = User.objects.create(username=staff_details['username'])
                    user.email = staff_details['email']
                    user.first_name = staff_details['first_name']
                    user.last_name = staff_details['last_name']
                    user.set_password(staff_details['password'])
                    user.save()
                staff = Staff.objects.create(staff_id=staff_details['staff_id'])                
                staff.user = user
                staff.dob = datetime.strptime(staff_details['dob'], '%d/%m/%Y')
                staff.address = staff_details['address']
                staff.mobile_number = staff_details['mobile_number']
                staff.land_number = staff_details['land_number']                
                staff.blood_group = staff_details['blood_group']
                staff.doj = datetime.strptime(staff_details['doj'], '%d/%m/%Y')
                designation = Designation.objects.get(id=staff_details['designation'])
                staff.designation=designation
                
                staff.qualifications = staff_details['qualifications']
                staff.photo = request.FILES.get('photo_img', '')
                staff.experiance = staff_details['experiance']
                staff.role = staff_details['role']
                if staff_details['role'] == 'admin':
                    user.is_superuser = True
                elif staff_details['role'] == 'office_staff' or staff_details['role'] == 'teacher':
                    user.is_staff = True
                user.save()
                staff.certificates_submitted = staff_details['certificates_submitted']
                staff.certificates_remarks = staff_details['certificates_remarks']
                staff.certificates_file = staff_details['certificates_file']
                staff.id_proofs_submitted = staff_details['id_proof']
                staff.id_proofs_remarks = staff_details['id_proof_remarks']
                staff.id_proofs_file = staff_details['id_proof_file']
                staff.guardian_name = staff_details['guardian_name']
                staff.guardian_address = staff_details['guardian_address']
                staff.relationship = staff_details['relationship']
                staff.guardian_mobile_number = staff_details['guardian_mobile_number']
                staff.guardian_land_number = staff_details['guardian_land_number']
                staff.guardian_email = staff_details['guardian_email']
                staff.reference_name = staff_details['reference_name']
                staff.reference_address = staff_details['reference_address']
                staff.reference_mobile_number = staff_details['reference_mobile_number']
                staff.reference_land_number = staff_details['reference_land_number']
                staff.reference_email = staff_details['reference_email']                   
               
                staff.save()
                res = {
                    'result': 'ok',
                }  

            response = simplejson.dumps(res)
            return HttpResponse(response, status = status, mimetype="application/json")

class EditStaffDetails(View):
   
    def get(self, request, *args, **kwargs):
        
        staff_id = kwargs['staff_id']
        
        designation = Designation.objects.all()
        context = {
            'staff_id': staff_id,
            'designations': designation,
        }
        ctx_staff_data = []
        if request.is_ajax():
            try:
                designation =  request.GET.get('designation', '')
               
                if designation:
                    designation = Designation.objects.get(id=designation)
                staff = Staff.objects.get(id = staff_id)
                ctx_staff_data.append({
                    'staff_id': staff.staff_id if staff.staff_id else '',
                    'first_name': staff.user.first_name if staff.user else '',
                    'last_name': staff.user.last_name if staff.user else '',
                    'username': staff.user.username if staff.user else '',
                    'dob': staff.dob.strftime('%d/%m/%Y') if staff.dob else '',
                    'address': staff.address if staff.address else '',
                    'mobile_number': staff.mobile_number if staff.mobile_number else '',
                    'land_number': staff.land_number if staff.land_number else '',
                    'email': staff.user.email if staff.user else '',
                    'blood_group': staff.blood_group if staff.blood_group else '',
                    'doj': staff.doj.strftime('%d/%m/%Y') if staff.doj else '',
                    'designation': staff.designation.designation if staff.designation else '',
                    'qualifications': staff.qualifications if staff.qualifications else '',
                    'experiance': staff.experiance if staff.experiance else '',
                    'photo': staff.photo.name if staff.photo.name else '',
                    'role': staff.role if staff.role else '',
                    'certificates_submitted': staff.certificates_submitted if staff.certificates_submitted else '',
                    'certificates_remarks': staff.certificates_remarks if staff.certificates_remarks else '',
                    'certificates_file': staff.certificates_file if staff.certificates_file else '',
                    'id_proofs_submitted': staff.id_proofs_submitted if staff.id_proofs_submitted else '',
                    'id_proofs_remarks': staff.id_proofs_remarks if staff.id_proofs_remarks else '',
                    'id_proofs_file': staff.id_proofs_file if staff.id_proofs_file else '',
                    'guardian_name': staff.guardian_name if staff.staff_id else '',
                    'guardian_address': staff.guardian_address if staff.guardian_address else '',
                    'relationship': staff.relationship if staff.relationship else '',
                    'guardian_mobile_number': staff.guardian_mobile_number if staff.guardian_mobile_number else '',
                    'guardian_land_number': staff.guardian_land_number if staff.guardian_land_number else '',
                    'guardian_email': staff.guardian_email if staff.guardian_email else '',
                    'reference_name': staff.reference_name if staff.reference_name else '',
                    'reference_address': staff.reference_address if staff.reference_address else '',
                    'reference_mobile_number': staff.reference_mobile_number if staff.reference_mobile_number else '',
                    'reference_land_number': staff.reference_land_number if staff.reference_land_number else '',
                    'reference_email': staff.reference_email if staff.reference_email else '',
                   
                })
                res = {
                    'result': 'ok',
                    'staff': ctx_staff_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                ctx_item_data = []
                res = {
                    'result': 'error',
                    'staff': ctx_staff_data,
                    
                }
                status = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        return render(request, 'staff/edit_staff_details.html',context)

    def post(self, request, *args, **kwargs):

        staff_id = kwargs['staff_id']
        staff = Staff.objects.get(id = staff_id)
        staff_data = ast.literal_eval(request.POST['staff'])
        try:
            staff.staff_id = staff_data['staff_id']
            staff.user.first_name = staff_data['first_name']
            staff.user.last_name = staff_data['last_name']
            staff.dob = datetime.strptime(staff_data['dob'],'%d/%m/%Y')
            staff.address = staff_data['address']
            mobile_number = staff_data['mobile_number']
            staff.land_number = staff_data['land_number']
            staff.user.email = staff_data['email']
            staff.user.save()
            staff.blood_group = staff_data['blood_group']
            staff.doj = datetime.strptime(staff_data['doj'],'%d/%m/%Y')
            designation = Designation.objects.get(designation = staff_data['designation'])
            staff.designation = designation
            staff.qualifications = staff_data['qualifications']
            staff.experiance = staff_data['experiance']
            print request.FILES.get('photo_img', '')
            if request.FILES.get('photo_img', ''):
                staff.photo = request.FILES.get('photo_img', '') 
            staff.role = staff_data['role']
            if staff_data['role'] == 'admin':
                staff.user.is_superuser = True
            elif staff_data['role'] == 'teacher' or staff_data['role'] == 'office_staff':
                staff.user.is_staff = True
            staff.user.save()
            staff.certificates_submitted = staff_data['certificates_submitted']
            staff.certificates_remarks = staff_data['certificates_remarks']
            staff.certificates_file = staff_data['certificates_file']
            staff.id_proofs_submitted = staff_data['id_proofs_submitted']
            staff.id_proofs_remarks = staff_data['id_proofs_remarks']
            staff.id_proofs_file = staff_data['id_proofs_file']
            staff.guardian_name = staff_data['guardian_name']
            staff.guardian_address = staff_data['guardian_address']
            staff.relationship = staff_data['relationship']
            staff.guardian_mobile_number = staff_data['guardian_mobile_number']
            staff.guardian_land_number = staff_data['guardian_land_number']
            staff.guardian_email = staff_data['guardian_email']
            staff.reference_name = staff_data['reference_name']
            staff.reference_address = staff_data['reference_address']
            staff.reference_mobile_number = staff_data['reference_mobile_number']
            staff.reference_land_number = staff_data['reference_land_number']
            staff.reference_email = staff_data['reference_email']
            staff.save()
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print "Exception == ", str(Ex)
            res = {
                'result': 'error',
                'message': str(Ex)
            }
            status = 500
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')


class ListStaff(View):

    def get(self, request, *args, **kwargs):

        staffs = Staff.objects.all()
        if request.is_ajax():
            staff_list = []
            for staff in staffs:
                staff_list.append({
                    'id': staff.id,
                    'name': staff.user.first_name+ ' '+staff.user.last_name if staff.user else '',
                    'designation': staff.designation.designation if staff.designation else '',
                    'role': staff.role,
                    'staff_id': staff.staff_id
                })
            res = {
                'result': 'Ok',
                'staffs': staff_list
            }
            status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        ctx = {
            'staffs': staffs
        }
        return render(request, 'staff/list_staff.html',ctx)

class ViewStaffDetails(View):

    def get(self, request, *args, **kwargs):
        
        staff_id = kwargs['staff_id']
        ctx_staff_data = []
        if request.is_ajax():
            try:
                staff = Staff.objects.get(id = staff_id)
               
                ctx_staff_data.append({
                    'staff_id': staff.staff_id if staff.staff_id else '',
                    'staff_name': staff.user.first_name +' '+staff.user.last_name if staff.user else '',
                    'dob': staff.dob.strftime('%d/%m/%Y') if staff.dob else '',
                    'address': staff.address if staff.address else '',
                    'mobile_number': staff.mobile_number if staff.mobile_number else '',
                    'land_number': staff.land_number if staff.land_number else '',
                    'email': staff.user.email if staff.user else '',
                    'blood_group': staff.blood_group if staff.blood_group else '',
                    'doj': staff.doj.strftime('%d/%m/%Y') if staff.doj else '',
                    'designation': staff.designation.designation if staff.designation.designation else '',
                    'qualifications': staff.qualifications if staff.qualifications else '',
                    'experiance': staff.experiance if staff.experiance else '',
                    'photo': staff.photo.name if staff.photo.name else '',
                    'role': staff.role if staff.role else '',
                    'certificates_submitted': staff.certificates_submitted if staff.certificates_submitted else '',
                    'certificates_remarks': staff.certificates_remarks if staff.certificates_remarks else '',
                    'certificates_file': staff.certificates_file if staff.certificates_file else '',
                    'id_proofs_submitted': staff.id_proofs_submitted if staff.id_proofs_submitted else '',
                    'id_proofs_remarks': staff.id_proofs_remarks if staff.id_proofs_remarks else '',
                    'id_proofs_file': staff.id_proofs_file if staff.id_proofs_file else '',
                    'guardian_name': staff.guardian_name if staff.staff_id else '',
                    'guardian_address': staff.guardian_address if staff.guardian_address else '',
                    'relationship': staff.relationship if staff.relationship else '',
                    'guardian_mobile_number': staff.guardian_mobile_number if staff.guardian_mobile_number else '',
                    'guardian_land_number': staff.guardian_land_number if staff.guardian_land_number else '',
                    'guardian_email': staff.guardian_email if staff.guardian_email else '',
                    'reference_name': staff.reference_name if staff.reference_name else '',
                    'reference_address': staff.reference_address if staff.reference_address else '',
                    'reference_mobile_number': staff.reference_mobile_number if staff.reference_mobile_number else '',
                    'reference_land_number': staff.reference_land_number if staff.reference_land_number else '',
                    'reference_email': staff.reference_email if staff.reference_email else '',
                   
                })
                res = {
                    'result': 'ok',
                    'staff': ctx_staff_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
                ctx_item_data = []
                res = {
                    'result': 'error',
                    'staff': ctx_staff_data,
                }
                status = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

class GetDesignation(View):

    def get(self, request, *args, **kwargs):
        designations = Designation.objects.all()
        designation_list = []
        ctx={
            'designations':designations,
        }
        
        if request.is_ajax():
            try:
                for designation in designations:
                    designation_list.append({
                        'designation': designation.designation, 
                        'id': designation.id                
                    })
                designation_list.append({
                    'designation': 'other', 
                    'id': 'other'               
                })

                res = {
                    'result': 'ok',
                    'designations': designation_list,
                }
                status = 200
            except Exception as ex:
                res = {
                    'result': 'error',
                }
                status = 500
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')
        return render(request, 'staff/designation.html',ctx)

class DeleteStaffDetails(View):
    def get(self, request, *args, **kwargs):

        staff_id = kwargs['staff_id']       
        staff = Staff.objects.filter(id=staff_id)                          
        staff.delete()
        return HttpResponseRedirect(reverse('list_staff'))

class DeleteDesignation(View):
    def get(self, request, *args, **kwargs):

        designation_id = kwargs['designation_id']       
        designation = Designation.objects.get(id=designation_id)                          
        designation.delete()
        return HttpResponseRedirect(reverse('get_designation'))

class AddDesignation(View):
    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            try:
                
                designation, created = Designation.objects.get_or_create(designation=request.POST['designation'])
                if not created:
                    res = {
                        'result': 'error',
                        'message': 'Designation already existing'
                    }
                    status_code = 200
                else:
                    try:
                        designation = Designation.objects.get(id = request.POST['designation'])
                    
                    except Exception as ex:
                        print str(ex), "Exception ===="
                    designation.save()
                    res = {
                        'result': 'ok',
                        'id': designation.id
                    }  
                    status_code = 200 

            except Exception as ex:
                print str(ex), "Exception ===="
                res = {
                        'result': 'error',
                        'message': 'Designation Name already existing'
                    }
                status_code = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status = status_code, mimetype="application/json")

class EditDesignation(View):

    def get(self, request, *args, **kwargs):
        designation_id = kwargs['designation_id']
        print designation_id
        context = {
            'designation_id': designation_id,
        }
        ctx_data = []
        if request.is_ajax():
            try:
                designation = Designation.objects.get(id = designation_id)
                ctx_data.append({
                    'designation': designation.designation,
                    
                                        
                })
                res = {
                    'result': 'ok',
                    'designation': ctx_data,
                }
                status = 200
            except Exception as ex:
                print "Exception == ", str(ex)
              
                res = {
                    'result': 'error',
                    'designation': ctx_data,

                }
                status = 200
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')

        return render(request, 'staff/edit_designation.html',context)

    def post(self, request, *args, **kwargs):

        designation_id = kwargs['designation_id']

        designation = Designation.objects.get(id = designation_id)
        data = ast.literal_eval(request.POST['designation'])
        try:
            designation.designation = data['designation']
            designation.save()
            res = {
                'result': 'ok',
            }
            status = 200
        except Exception as Ex:
            print "Exception == ", str(Ex)
            res = {
                'result': 'error',
                'message': 'Designation with this name is already existing'
            }
            status = 200
        response = simplejson.dumps(res)
        return HttpResponse(response, status=status, mimetype='application/json')

class IsUsernameExists(View):

    def get(self, request, *args, **kwargs):

        if request.is_ajax():
            status = 200
            username = request.GET.get('username', '')
            print username , 'username'
            try:
                user = User.objects.get(username=username)
                res = {
                    'result': 'error',
                    'message': 'Username already existing',
                }
            except Exception as ex:
                print "ex == ", str(ex)
                res = {
                    'result': 'ok',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status, mimetype='application/json')