function reset_staff($scope) {
    $scope.staff = {
        'staff_id': '',
        'first_name': '',
        'last_name': '',
        'username': '',
        'password': '',
        'dob': '',
        'address': '',
        'mobile_number': '',
        'land_number': '',
        'email':'',
        'blood_group': '',
        'doj': '',
        'designation': '',
        'department': '',
        'qualifications': '',
        'experiance':'',
        'role': '',
        'certificates_submitted': '',
        'certificates_remarks': '',
        'certificates_file': '',
        'id_proof_remarks': '',
        'id_proof_file': '',
        'id_proof': '',
        'guardian_name': '',
        'guardian_address':'',
        'relationship': '',
        'guardian_mobile_number': '',
        'guardian_land_number': '',
        'guardian_email': '',
        'reference_name': '',
        'reference_address':'',
        'reference_mobile_number': '',
        'reference_land_number': '',
        'reference_email': '',
    }

}

function StaffController($scope, $element, $http, $timeout, share, $location) {
    
    $scope.designation_popup = '';
    $scope.is_user_exists = false;
    
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.popup = '';
        $scope.get_staffs();
        reset_staff($scope);
        var date_pick = new Picker.Date($$('#dob'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        console.log(date_pick);
        new Picker.Date($$('#doj'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.select_page = function(page){
        select_page(page, $scope.staffs, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.hide_popup_windows = function(){
        $('#staff_details_view')[0].setStyle('display', 'none');
        $('#add_staff_details')[0].setStyle('display', 'none');
    }
    $scope.display_staff_details = function(staff) {
        show_spinner();
        $scope.staff_id = staff.id;
        $scope.url = '/staff/view_staff_details/' + $scope.staff_id+ '/';
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.staff = data.staff[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });

        $scope.hide_popup_windows();
        $('#staff_details_view')[0].setStyle('display', 'block');
        
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '65%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#staff_details_view'
        });
        
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.get_staffs = function() {
        show_spinner();
        $http.get("/staff/list_staff/").success(function(data)
        {
            hide_spinner();
            $scope.staffs = data.staffs;
            paginate($scope.staffs, $scope);

        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });        
    }
    $scope.create_designation = function() {
        if ($scope.staff.designation == 'other') {
            $scope.popup.hide_popup();
            $scope.designation_popup = new DialogueModelWindow({
                'dialogue_popup_width': '38%',
                'message_padding': '0px',
                'left': '28%',
                'top': '182px',
                'height': 'auto',
                'content_div': '#add_designation'
            });
            var height = $(document).height();
            $scope.designation_popup.set_overlay_height(height);
            $scope.designation_popup.show_content();
        }
    }
    
    $scope.validate_new_staff = function() {
        $scope.validation_error = '';
        $scope.staff.dob = $$('#dob')[0].get('value');
        $scope.staff.doj = $$('#doj')[0].get('value');
        if($scope.staff.staff_id == '' || $scope.staff.staff_id == undefined) {
            $scope.validation_error = "Please Enter the Staff Code" ;
            return false;
        } else if($scope.staff.first_name == '' || $scope.staff.first_name == undefined) {
            $scope.validation_error = "Please Enter the First Name" ;
            return false;
        } else if($scope.staff.last_name == '' || $scope.staff.last_name == undefined) {
            $scope.validation_error = "Please Enter the Last Name" ;
            return false;
        } else if($scope.staff.username == '' || $scope.staff.username == undefined) {
            $scope.validation_error = "Please Enter the Username" ;
            return false;
        } else if($scope.is_user_exists) {
            $scope.validation_error = "Username already exists" ;
            return false;
        } else if($scope.staff.password == '' || $scope.staff.password == undefined) {
            $scope.validation_error = "Please Enter the Password" ;
            return false;
        } else if($scope.confirm_password == '' || $scope.confirm_password == undefined) {
            $scope.validation_error = "Please Enter the Confirm Password" ;
            return false;
        } else if($scope.staff.password != $scope.confirm_password) {
            $scope.validation_error = "Password not matches with Confirm Password" ;
            return false;
        } else if($scope.staff.dob == '' || $scope.staff.dob == undefined) {
            $scope.validation_error = "Please Enter DOB";
            return false;
        } else if($scope.staff.address == '' || $scope.staff.address == undefined) {
            $scope.validation_error = "Please Enter Address";
            return false;
        } else if($scope.staff.mobile_number == ''|| $scope.staff.mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.staff.mobile_number)) || $scope.staff.mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.staff.land_number == ''|| $scope.staff.land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.staff.land_number)) || $scope.staff.land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.staff.email == '' || $scope.staff.email == undefined) || (!(validateEmail($scope.staff.email)))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;
        } else if($scope.staff.blood_group == '' || $scope.staff.blood_group == undefined) {
            $scope.validation_error = "Please Enter Blood Group";
            return false; 
        } else if($scope.staff.doj == '' || $scope.staff.doj == undefined) {
            $scope.validation_error = "Please Enter Date of Join";
            return false;
        } else if($scope.staff.designation == '' || $scope.staff.designation == undefined) {
            $scope.validation_error = "Please Enter Designation";
            return false; 
        } else if($scope.staff.qualifications == '' || $scope.staff.qualifications == undefined) {
            $scope.validation_error = "Please enter qualifications";
            return false; 
        } else if($scope.staff.experiance == '' || $scope.staff.experiance == undefined) {
            $scope.validation_error = "Please enter experiance";
            return false;
        } else if($scope.staff.role == '' || $scope.staff.role == undefined) {
            $scope.validation_error = "Please enter role";
            return false;
        } else if($scope.staff.certificates_submitted == '' || $scope.staff.certificates_submitted == undefined) {
            $scope.validation_error = "Please enter certificates submitted";
            return false;
         } else if($scope.staff.id_proof == '' || $scope.staff.id_proof == undefined) {
             $scope.validation_error = "Please enter id proofs submitted";
            return false; 
        } else if($scope.staff.guardian_name == '' || $scope.staff.guardian_name == undefined) {
            $scope.validation_error = "Please Enter the Guardian Name" ;
            return false;
        
        } else if($scope.staff.guardian_address == '' || $scope.staff.guardian_address == undefined) {
            $scope.validation_error = "Please Enter Guardian Address";
            return false;
        } else if($scope.staff.relationship == '' || $scope.staff.relationship == undefined) {
            $scope.validation_error = "Please Enter Relationship";
            return false;
        } else if($scope.staff.guardian_mobile_number == ''|| $scope.staff.guardian_mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.staff.guardian_mobile_number)) || $scope.staff.guardian_mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.staff.guardian_land_number == ''|| $scope.staff.guardian_land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.staff.guardian_land_number)) || $scope.staff.guardian_land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.staff.guardian_email != '' && $scope.staff.guardian_email != undefined) && (!(validateEmail($scope.staff.guardian_email)))){
                $scope.validation_error = "Please enter a Valid Email Id";
                return false;
        } else if($scope.staff.reference_name == '' || $scope.staff.reference_name == undefined) {
            $scope.validation_error = "Please Enter the Reference Name" ;
            return false;
        } else if($scope.staff.reference_address == '' || $scope.staff.reference_address == undefined) {
            $scope.validation_error = "Please Enter Reference Address";
            return false;
        } else if($scope.staff.reference_mobile_number == ''|| $scope.staff.reference_mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.staff.reference_mobile_number)) || $scope.staff.reference_mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.staff.reference_land_number == ''|| $scope.staff.reference_land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.staff.reference_land_number)) || $scope.staff.reference_land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.staff.reference_email != '' && $scope.staff.reference_email != undefined) && (!(validateEmail($scope.staff.reference_email)))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;                                                       
        } 
        return true;
        
    } 
    $scope.validate_new_designation = function() {
        $scope.validation_error = '';
        if($scope.designation == '' || $scope.designation == undefined) {
            $scope.validation_error = "Please Enter a Designation" ;
            return false;
        }  return true;
     }  
    $scope.add_new_designation = function(){  
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '38%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_designation'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.save_new_designation= function() {

        if($scope.validate_new_designation()) {
        
            params = { 
                'designation':$scope.designation,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/staff/add_designation/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                hide_spinner();
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;

                } else {
                    if ($scope.designation_popup) {
                        $scope.designation_popup.hide_popup();
                        get_designation($scope, $http);
                        $scope.staff.designation = data.id;
                        $scope.popup.show_content();

                    } else {
                        $scope.popup.hide_popup();
                        document.location.href ='/staff/get_designation/';
                    }
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    } 

    $scope.add_new_staff = function(){  

        show_spinner();
        reset_staff($scope);
        $scope.url = '/staff/get_designation/';
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.designations = data.designations;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        $scope.hide_popup_windows();
        $('#add_staff_details')[0].setStyle('display', 'block');
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '79%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_staff_details'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.is_username_exists = function() {
        var is_exists_url = '/staff/is_username_exists/?username='+$scope.staff.username;
        $http.get(is_exists_url).success(function(data){
            $scope.is_exist_message = '';
            if (data.result == 'error') {
                $scope.is_exist_message = data.message;
                $scope.is_user_exists = true;
            } else {
                $scope.is_user_exists = false;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.save_new_staff = function() {
        if($scope.validate_new_staff()) {
            params = { 
                'staff': angular.toJson($scope.staff),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            var fd = new FormData();
            console.log($scope.photo_img);
            if ($scope.photo_img != undefined)
                fd.append('photo_img', $scope.photo_img.src)
            for(var key in params){
                fd.append(key, params[key]);          
            }
            var url = "/staff/add_staff/";
            $http.post(url, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined
                }
            }).success(function(data, status){
                hide_spinner();
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                }
                else {
                    document.location.href ="/staff/list_staff/";
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}

function EditDesignationController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, designation_id){
        $scope.csrf_token = csrf_token;
        $scope.designation_id = designation_id;
        $scope.url = '/staff/edit_designation/' + $scope.designation_id+ '/';
        $http.get($scope.url).success(function(data)
        {   
            $scope.designation = data.designation[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        
    }
    $scope.validate_edit_designation = function() {
        
        $scope.validation_error = '';

        if($scope.designation.designation == '' || $scope.designation.designation == undefined) {
            $scope.validation_error = "Please Enter designation Name" ;
            return false;
        } return true;   
     }

    $scope.save_designation = function() {
        $scope.is_valid = $scope.validate_edit_designation();

        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
           
            params = { 
                'designation': angular.toJson($scope.designation),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method : 'post',
                url : $scope.url,
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                hide_spinner();
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                    
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href = '/staff/get_designation/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}

function EditStaffController($scope, $http, $element, $location, $timeout) {
    
    $scope.init = function(csrf_token, staff_id){
        $scope.url = '/staff/get_designation/';
        get_designation($scope, $http);
        $scope.csrf_token = csrf_token;
        $scope.staff_id = staff_id;
        show_spinner();
        $scope.edit_staff_url = '/staff/edit_staff_details/' + $scope.staff_id+ '/';
        $http.get($scope.edit_staff_url).success(function(data)
        {
            hide_spinner();
            $scope.staff = data.staff[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        
        new Picker.Date($$('#dob'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#doj'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.validate_edit_staff = function() {
        $scope.validation_error = '';
        $scope.staff.dob = $$('#dob')[0].get('value');
        $scope.staff.doj = $$('#doj')[0].get('value');
        if($scope.staff_id == '' || $scope.staff_id == undefined) {
            $scope.validation_error = "Please Enter the id" ;
            return false;
        } else if($scope.staff.first_name == '' || $scope.staff.first_name == undefined) {
            $scope.validation_error = "Please Enter the First Name" ;
            return false;
        }  else if($scope.staff.last_name == '' || $scope.staff.last_name == undefined) {
            $scope.validation_error = "Please Enter the First Name" ;
            return false;
        } else if($scope.staff.dob == '' || $scope.staff.dob == undefined) {
            $scope.validation_error = "Please Enter DOB";
            return false;
        } else if($scope.staff.address == '' || $scope.staff.address == undefined) {
            $scope.validation_error = "Please Enter Address";
            return false;
        } else if($scope.staff.mobile_number == ''|| $scope.staff.mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.staff.mobile_number)) || $scope.staff.mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.staff.land_number == ''|| $scope.staff.land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.staff.land_number)) || $scope.staff.land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.staff.email != '' && $scope.staff.email != undefined) && (!(validateEmail($scope.staff.email)))){
                $scope.validation_error = "Please enter a Valid Email Id";
                return false;
        } else if($scope.staff.blood_group == '' || $scope.staff.blood_group == undefined) {
            $scope.validation_error = "Please Enter Blood Group";
            return false; 
        } else if($scope.staff.doj == '' || $scope.staff.doj == undefined) {
            $scope.validation_error = "Please Enter Date of Join";
            return false;
        } else if($scope.staff.designation == '' || $scope.staff.designation == undefined) {
            $scope.validation_error = "Please Enter Designation";
            return false; 
        } else if($scope.staff.qualifications == '' || $scope.staff.qualifications == undefined) {
            $scope.validation_error = "Please enter qualifications";
            return false; 
        }  else if($scope.staff.experiance == '' || $scope.staff.experiance == undefined) {
            $scope.validation_error = "Please enter experiance";
            return false;
        } else if($scope.staff.certificates_submitted == '' || $scope.staff.certificates_submitted == undefined) {
            $scope.validation_error = "Please enter certificates submitted";
            return false;
         } else if($scope.staff.id_proofs_submitted == '' || $scope.staff.id_proofs_submitted == undefined) {
             $scope.validation_error = "Please enter id proofs submitted";
            return false; 
        } else if($scope.staff.guardian_name == '' || $scope.staff.guardian_name == undefined) {
            $scope.validation_error = "Please Enter the Guardian Name" ;
            return false;
        } else if($scope.staff.guardian_address == '' || $scope.staff.guardian_address == undefined) {
            $scope.validation_error = "Please Enter Guardian Address";
            return false;
        } else if($scope.staff.relationship == '' || $scope.staff.relationship == undefined) {
            $scope.validation_error = "Please Enter Relationship";
            return false;
        } else if($scope.staff.guardian_mobile_number == ''|| $scope.staff.guardian_mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.staff.guardian_mobile_number)) || $scope.staff.guardian_mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.staff.guardian_land_number == ''|| $scope.staff.guardian_land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.staff.guardian_land_number)) || $scope.staff.guardian_land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.staff.guardian_email != '' && $scope.staff.guardian_email != undefined) && (!(validateEmail($scope.staff.guardian_email)))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;
        } else if($scope.staff.reference_name == '' || $scope.staff.reference_name == undefined) {
            $scope.validation_error = "Please Enter the Reference Name" ;
            return false;
        } else if($scope.staff.reference_address == '' || $scope.staff.reference_address == undefined) {
            $scope.validation_error = "Please Enter Reference Address";
            return false;
        } else if($scope.staff.reference_mobile_number == ''|| $scope.staff.reference_mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.staff.reference_mobile_number)) || $scope.staff.reference_mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.staff.reference_land_number == ''|| $scope.staff.reference_land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.staff.reference_land_number)) || $scope.staff.reference_land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.staff.reference_email != '' && $scope.staff.reference_email != undefined) && (!(validateEmail($scope.staff.reference_email)))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;                                                       
        } return true;
    }  
    $scope.edit_staff = function() {
        if($scope.validate_edit_staff()){
            params = { 
                'staff': angular.toJson($scope.staff),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            var fd = new FormData();
            if ($scope.photo_img != undefined)
                fd.append('photo_img', $scope.photo_img.src) 
            for(var key in params){
                fd.append(key, params[key]);          
            }
            show_spinner();
            $http.post($scope.edit_staff_url, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined
                }
            }).success(function(data, status) {
                hide_spinner();
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href = '/staff/list_staff/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }    
    }
}