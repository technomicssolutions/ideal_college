function add_new_student($http, $scope){  
    $scope.hide_popup_windows();
    $('#add_student_details')[0].setStyle('display', 'block');        
    $scope.popup = new DialogueModelWindow({

        'dialogue_popup_width': '79%',
        'message_padding': '0px',
        'left': '28%',
        'top': '182px',
        'height': 'auto',
        'content_div': '#add_student_details'
    });
    var height = $(document).height();
    $scope.popup.set_overlay_height(height);
    $scope.popup.show_content();
    $scope.course = '';
    $scope.batch = '';
}
function save_new_student($http, $scope) {
    if(validate_new_student($scope)) {
        $scope.popup.hide_popup();
        $scope.dob = $$('#dob')[0].get('value');
        $scope.doj = $$('#doj')[0].get('value');
        params = { 
            'student_name':$scope.student_name,
            'roll_number': $scope.roll_number,
            'course': $scope.course,
            'batch': $scope.batch,
            'applicable_fee_heads': angular.toJson($scope.fee_heads),
            'semester': $scope.semester,           
            'qualified_exam': $scope.qualified_exam,
            'technical_qualification': $scope.technical_qualification,
            'dob': $scope.dob,
            'address': $scope.address,
            'mobile_number': $scope.mobile_number,
            'land_number': $scope.land_number,
            'email':$scope.email,
            'blood_group': $scope.blood_group,
            'doj': $scope.doj,
            'certificates_submitted': $scope.certificates_submitted,
            'certificates_remarks': $scope.certificates_remarks,
            'certificates_file': $scope.certificates_file,
            'id_proofs_submitted': $scope.id_proof,
            'id_proofs_remarks': $scope.id_proof_remarks,
            'id_proofs_file': $scope.id_proof_file,
            'guardian_name': $scope.guardian_name,
            'guardian_address':$scope.guardian_address,
            'relationship': $scope.relationship,
            'guardian_mobile_number': $scope.guardian_mobile_number,
            'guardian_land_number': $scope.guardian_land_number,
            'guardian_email': $scope.guardian_email,            
            "csrfmiddlewaretoken" : $scope.csrf_token
        }
        var fd = new FormData();
        fd.append('photo_img', $scope.photo_img.src)   
        for(var key in params){
            fd.append(key, params[key]);          
        }
        var url = "/academic/add_student/";
        show_spinner();
        $http.post(url, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined
            }
        }).success(function(data, status){
            if (data.result == 'error'){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
                var height = $(document).height();
                $scope.popup.set_overlay_height(height);
                $scope.popup.show_content();
            }
            else {
                
                document.location.href ="/academic/list_student/";
            }
            hide_spinner();
        }).error(function(data, status){
            $scope.error_flag=true;
            $scope.validation_error = data.message;
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        });
    }
}
// function get_fees_head($scope, $http) {
//     $http.get().success(function(data){
//         $scope.heads = data.heads;
//     }).error(function(data, status){
//         console.log('Request failed'|| data)
//     })
// }
function reset_student($scope) {
    $scope.student_name = '';
    $scope.roll_number = '';
    $scope.course = '';
    $scope.batch = '';
    $scope.semester = '';
    $scope.qualified_exam = '';
    $scope.technical_qualification = '';
    $scope.dob = '';
    $scope.address = '';
    $scope.mobile_number = '';
    $scope.land_number = '';
    $scope.email = '';
    $scope.blood_group = '';
    $scope.doj = '';
    $scope.certificates_submitted = '';
    $scope.certificates_remarks = '';
    $scope.certificates_file = '';
    $scope.id_proof = '';
    $scope.id_proof_remarks = '';
    $scope.id_proof_file = '';
    $scope.guardian_name = '';
    $scope.guardian_address = '';
    $scope.relationship = '';
    $scope.guardian_mobile_number = '';
    $scope.guardian_land_number = '';
    $scope.guardian_email    = '';
    $scope.photo_img = {};
}
validate_new_student = function($scope) {
    $scope.validation_error = '';
    $scope.dob = $$('#dob')[0].get('value');
    $scope.doj = $$('#doj')[0].get('value');
    if($scope.student_name == '' || $scope.student_name == undefined) {
        $scope.validation_error = "Please Enter the Name" ;
        return false;
    } else if($scope.roll_number == '' || $scope.roll_number == undefined) {
        $scope.validation_error = "Please Enter the Roll Number" ;
        return false;
    } else if($scope.roll_number!='' && !Number($scope.roll_number)) {
        $scope.validation_error = "Please Enter a valid Roll Number" ;
        return false;
    } else if($scope.course == '' || $scope.course == undefined) {
        $scope.validation_error = "Please Enter Course";
        return false;
    } else if($scope.batch == '' || $scope.batch == undefined) {
        $scope.validation_error = "Please Enter Batch";
        return false;
    } else if ($scope.fee_heads == '' || $scope.fee_heads == undefined) {
        $scope.validation_error = "Please choose Applicable Fee Heads";
        return false;
    } else if($scope.dob == '' || $scope.dob == undefined) {
        $scope.validation_error = "Please Enter DOB";
        return false;
    } else if($scope.address == '' || $scope.address == undefined) {
        $scope.validation_error = "Please Enter Address";
        return false;
    } else if($scope.mobile_number == ''|| $scope.mobile_number == undefined){
        $scope.validation_error = "Please enter the Mobile Number";
        return false;
    } else if(!(Number($scope.mobile_number)) || $scope.mobile_number.length > 15) {            
        $scope.validation_error = "Please enter a Valid Mobile Number";
        return false;
    } else if($scope.land_number == ''|| $scope.land_number == undefined){
        $scope.validation_error = "Please enter the Telephone Number";
        return false;
    } else if(!(Number($scope.land_number)) || $scope.land_number.length > 15) {            
        $scope.validation_error = "Please enter a Valid Telephone Number";
        return false;
    } else if(($scope.email != '' && $scope.email != undefined) && (!(validateEmail($scope.email)))){
        $scope.validation_error = "Please enter a Valid Email Id";
        return false;
    } else if($scope.blood_group == '' || $scope.blood_group == undefined) {
        $scope.validation_error = "Please Enter Blood Group";
        return false; 
    } else if($scope.doj == '' || $scope.doj == undefined) {
        $scope.validation_error = "Please Enter Date of Join";
        return false;
    } else if($scope.certificates_submitted == '' || $scope.certificates_submitted == undefined) {
        $scope.validation_error = "Please enter certificates submitted";
        return false;
    } else if($scope.id_proof == '' || $scope.id_proof == undefined) {
         $scope.validation_error = "Please enter id proofs submitted";
        return false; 
    } else if($scope.guardian_name == '' || $scope.guardian_name == undefined) {
        $scope.validation_error = "Please Enter the Guardian Name" ;
        return false;
    
    } else if($scope.guardian_address == '' || $scope.guardian_address == undefined) {
        $scope.validation_error = "Please Enter Guardian Address";
        return false;
    } else if($scope.relationship == '' || $scope.relationship == undefined) {
        $scope.validation_error = "Please Enter Relationship";
        return false;
    } else if($scope.guardian_mobile_number == ''|| $scope.guardian_mobile_number == undefined){
        $scope.validation_error = "Please enter the Mobile Number";
        return false;
    } else if(!(Number($scope.guardian_mobile_number)) || $scope.guardian_mobile_number.length > 15) {            
        $scope.validation_error = "Please enter a Valid Mobile Number";
        return false;
    } else if($scope.guardian_land_number == ''|| $scope.guardian_land_number == undefined){
        $scope.validation_error = "Please enter the Telephone Number";
        return false;
    } else if(!(Number($scope.guardian_land_number)) || $scope.guardian_land_number.length > 15) {            
        $scope.validation_error = "Please enter a Valid Telephone Number";
        return false;
    } else if(($scope.guardian_email != '' && $scope.guardian_email != undefined) && (!(validateEmail($scope.guardian_email)))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;                                                          
    } else {
        return true;
    }     
}   
function EditStudentController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, student_id){
        $scope.csrf_token = csrf_token;
        $scope.student_id = student_id;
        $scope.url = '/academic/edit_student_details/' + $scope.student_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            $scope.student = data.student[0];
            if ($scope.student.course_id)
                $scope.get_batch($scope.student.course_id);
            if ($scope.student.course && $scope.student.batch) {
                $scope.course = $scope.student.course;
                $scope.batch = $scope.student.batch;
                get_fee_structure_head_details($scope, $http);
            }
            hide_spinner();
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
        get_course_list($scope, $http);
        get_semester_list($scope, $http);
    }
    $scope.get_batch = function(course){
        show_spinner(); 
        if (course)
            $scope.url_batch = '/college/get_batch/'+ course+ '/';
        else
            $scope.url_batch = '/college/get_batch/'+ $scope.course+ '/';
        $http.get($scope.url_batch).success(function(data)
        {
            $scope.batches = data.batches;
            hide_spinner();
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate_edit_student = function() {
        $scope.validation_error = '';
        $scope.dob = $$('#dob')[0].get('value');
        $scope.doj = $$('#doj')[0].get('value');
        if($scope.student.student_name == '' || $scope.student.student_name == undefined) {
            $scope.validation_error = "Please Enter the Name" ;
            return false;
        } else if($scope.student.roll_number == '' || $scope.student.roll_number == undefined) {
            $scope.validation_error = "Please Enter the Roll Number" ;
            return false;
        } else if($scope.student.course == '' || $scope.student.course == undefined) {
            $scope.validation_error = "Please Enter Course";
            return false;
        } else if($scope.student.batch == '' || $scope.student.batch == undefined) {
            $scope.validation_error = "Please Enter Batch";
            return false;
        } else if($scope.student.fee_heads_list == '' || $scope.student.fee_heads_list == undefined) {
            $scope.validation_error = "Please choose Fees Heads";
            return false;
        } else if($scope.student.dob == '' || $scope.student.dob == undefined) {
            $scope.validation_error = "Please Enter DOB";
            return false;
        } else if($scope.student.address == '' || $scope.student.address == undefined) {
            $scope.validation_error = "Please Enter Address";
            return false;
        } else if($scope.student.mobile_number == ''|| $scope.student.mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.student.mobile_number)) || $scope.student.mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.student.land_number == ''|| $scope.student.land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.student.land_number)) || $scope.student.land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.student.email != '' && $scope.student.email != undefined) && (!(validateEmail($scope.student.email)))){
                $scope.validation_error = "Please enter a Valid Email Id";
                return false;
        } else if($scope.student.blood_group == '' || $scope.student.blood_group == undefined) {
            $scope.validation_error = "Please Enter Blood Group";
            return false; 
        } else if($scope.student.doj == '' || $scope.student.doj == undefined) {
            $scope.validation_error = "Please Enter Date of Join";
            return false;
        } else if($scope.student.certificates_submitted == '' || $scope.student.certificates_submitted == undefined) {
            $scope.validation_error = "Please enter certificates submitted";
            return false;
        } else if($scope.student.id_proofs_submitted == '' || $scope.student.id_proofs_submitted == undefined) {
             $scope.validation_error = "Please enter id proofs submitted";
            return false; 
        } else if($scope.student.guardian_name == '' || $scope.student.guardian_name == undefined) {
            $scope.validation_error = "Please Enter the Guardian Name" ;
            return false;
        } else if($scope.student.guardian_address == '' || $scope.student.guardian_address == undefined) {
            $scope.validation_error = "Please Enter Guardian Address";
            return false;
        } else if($scope.student.relationship == '' || $scope.student.relationship == undefined) {
            $scope.validation_error = "Please Enter Relationship";
            return false;
        } else if($scope.student.guardian_mobile_number == ''|| $scope.student.guardian_mobile_number == undefined){
            $scope.validation_error = "Please enter the Mobile Number";
            return false;
        } else if(!(Number($scope.student.guardian_mobile_number)) || $scope.student.guardian_mobile_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Mobile Number";
            return false;
        } else if($scope.student.guardian_land_number == ''|| $scope.student.guardian_land_number == undefined){
            $scope.validation_error = "Please enter the Telephone Number";
            return false;
        } else if(!(Number($scope.student.guardian_land_number)) || $scope.student.guardian_land_number.length > 15) {            
            $scope.validation_error = "Please enter a Valid Telephone Number";
            return false;
        } else if(($scope.student.guardian_email != '' && $scope.student.guardian_email != undefined) && (!(validateEmail($scope.student.guardian_email)))){
            $scope.validation_error = "Please enter a Valid Email Id";
            return false;                                                    
        } else {
            return true;
        }  
    }   
    $scope.edit_student = function() {
        if ($scope.validate_edit_student()){
            $scope.error_flag=false;
            $scope.message = '';
            show_spinner();
            if ($scope.student.uid == null) {
                $scope.student.uid = '';
            }
            $scope.student.fee_heads = angular.toJson($scope.student.fee_heads_list);
            params = { 
                'student': angular.toJson($scope.student),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            var fd = new FormData();
            if ($scope.photo_img != undefined)
                fd.append('photo_img', $scope.photo_img.src)   
            for(var key in params){
                fd.append(key, params[key]);          
            }
            show_spinner();
            $http.post($scope.url, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined
                }
            }).success(function(data, status){
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                }
                else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href = '/academic/list_student/';
                }
                hide_spinner();
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}
function StudentListController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token){
        get_course_list($scope, $http);
        $scope.page_interval = 10;
        $scope.visible_list = [];
        $scope.students = [];
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.popup = '';      
        $scope.pages = 1;
        $scope.student_id = '';
        $scope.students_listing = false;
        $scope.student_selected = true;
        var date_pick = new Picker.Date($$('#dob'), {
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
        reset_student($scope);
    }
    $scope.get_batch = function(){   
        if($scope.course != null){
            show_spinner();     
            var url = '/college/get_batch/'+ $scope.course+ '/';
            $http.get(url).success(function(data)
            {
                $scope.batches = data.batches;
                hide_spinner();
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
        }
    }
    $scope.get_fees_head = function() {
        get_fee_structure_head_details($scope, $http);
    }
    $scope.get_students = function(){
        var url = '/academic/list_student/?batch_id='+ $scope.batch;
        if($scope.batch != null){
            show_spinner();
            $http.get(url).success(function(data)
            {
                $scope.students = data.students;
                console.log($scope.students);
                paginate(data.students, $scope);
                hide_spinner();
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
        }
    }
    $scope.select_student = function(student){
        $scope.student_name = student.student_name;
        $scope.student_id = student.id;
        $scope.students_listing = false;
        $scope.student_selected = true;
    }
    $scope.get_student_details = function() {
        course_batch_student_list($scope, $http);
    }
    $scope.add_new_student  = function(){
        add_new_student($http, $scope);
    }
    $scope.save_new_student = function(){
        save_new_student($http, $scope);
    }
    $scope.generate_id_card = function(){
        console.log($scope.filtering_option);
        if ($scope.course == 'select' || $scope.course == '' || $scope.course == null) {
            $scope.validation_error = 'Please choose course';
        } else if ($scope.batch == 'select' || $scope.batch == '' || $scope.batch == null) {
            $scope.validation_error = 'Please choose batch';
        } else if (($scope.student_name == undefined || $scope.student_name == "" )&& $scope.filtering_option == "student_wise") {
            $scope.validation_error = 'Please choose student';
        } else if (($scope.student_id == undefined || $scope.student_id == "" )&& $scope.filtering_option == "student_wise") {
            $scope.validation_error = 'Please choose student';
        }  else if ($scope.filtering_option != "student_wise" && $scope.filtering_option != "batch_wise") {
            $scope.validation_error = 'Please choose report type';
        } else {
           document.location.href = '/report/id_card/?course='+$scope.course+'&batch='+$scope.batch+'&student='+$scope.student_id+'&filtering_option='+$scope.filtering_option+'&report_type=id_card';
        }
    }
    $scope.hide_popup_windows = function(){
        $('#add_student_details')[0].setStyle('display', 'none');
    }    
    $scope.display_student_details = function(student) {
        show_spinner();
        $scope.student_id = student.id;
        $scope.url = '/academic/view_student_details/' + $scope.student_id+ '/';
        $http.get($scope.url).success(function(data)
        {
            $scope.student = data.student[0];
            hide_spinner();
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        $scope.hide_popup_windows();
        $('#student_details_view')[0].setStyle('display', 'block');
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '78%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#student_details_view'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.select_page = function(page){
        select_page(page, $scope.students, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
}