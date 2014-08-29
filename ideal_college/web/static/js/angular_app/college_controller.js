function EditSemesterController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, semester_id){
        $scope.csrf_token = csrf_token;
        $scope.semester_id = semester_id;
        $scope.url = '/college/edit_semester/' + $scope.semester_id+ '/';
        $http.get($scope.url).success(function(data)
        {
            $scope.semester = data.semester[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        
    }
    $scope.validate_edit_semester = function() {
        $scope.validation_error = '';
        if($scope.semester.semester == '' || $scope.semester.semester == undefined) {
            $scope.validation_error = "Please Enter semester Name" ;
            return false;
        } return true;   
     }

    $scope.save_semester = function() {
        $scope.is_valid = $scope.validate_edit_semester();
        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
           
            params = { 
                'semester': angular.toJson($scope.semester),
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
                    document.location.href = '/college/list_semester/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}

function EditBranchController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, branch_id){

        $scope.csrf_token = csrf_token;
        $scope.branch_id = branch_id;
        $scope.url = '/college/edit_branch/' + $scope.branch_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.branch = data.branch[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        get_branch_list($scope, $http);
    }
    $scope.validate_edit_branch = function() {

        
        $scope.validation_error = '';

        if($scope.branch.branch == '' || $scope.branch.branch == undefined) {
            $scope.validation_error = "Please Enter batch Name" ;
            return false;
        } return true;   
     }

    $scope.save_branch = function() {
        $scope.is_valid = $scope.validate_edit_branch();
        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
           
            params = { 
                'branch': angular.toJson($scope.branch),
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
                    document.location.href = '/college/list_branch/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}

function EditBatchController($scope, $http, $element, $location, $timeout) {
    
    $scope.init = function(csrf_token, batch_id){
        $scope.csrf_token = csrf_token;
        $scope.batch_id = batch_id;
        $scope.url = '/college/edit_batch/' + $scope.batch_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.batch = data.batch[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });

         new Picker.Date($$('#batch_start'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            pickOnly: 'years',
            format:'%Y',
            canAlwaysGoUp: ['years']
        });
        new Picker.Date($$('#batch_end'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            pickOnly: 'years',
            format:'%Y',
            canAlwaysGoUp: ['years']
        });
        
        
    }
    $scope.validate_edit_batch = function() {
        $scope.validation_error = '';
        if($scope.batch.batch_start == '' || $scope.batch.batch_start == undefined) {
            $scope.validation_error = "Please Enter Start Year" ;
            return false;
        } else if($scope.batch.batch_end == '' || $scope.batch.batch_end == undefined) {
            $scope.validation_error = "Please Enter End Year" ;
            return false;
        } 
        return true;   
     }

    $scope.save_batch = function() {

        $scope.batch.batch_start = $$('#batch_start')[0].get('value');
        $scope.batch.batch_end = $$('#batch_end')[0].get('value');
        $scope.is_valid = $scope.validate_edit_batch();
        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
            params = { 
                'batch': angular.toJson($scope.batch),
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
                    document.location.href = '/college/list_batch/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}

function EditCourseController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, course_id){
        $scope.csrf_token = csrf_token;
        $scope.course_id = course_id;
        $scope.get_semester();
        $scope.semester_list = [];
        $scope.url = '/college/edit_course/' + $scope.course_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {   
            hide_spinner();
            $scope.course = data.course[0];
            for(var i = 0; i < $scope.course.semester_details.length; i++){
                for(var j = 0; j < $scope.semesters.length; j++){
                    if($scope.semesters[j].id == $scope.course.semester_details[i].semester_id){
                        $scope.semesters[j].selected = true;
                        $scope.semester_list.push($scope.semesters[j].id);
                    }           
                }
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        
    }
    $scope.get_semester = function(){
        var url = '/college/list_semester/';
        show_spinner();
        $http.get(url).success(function(data) {
            hide_spinner();
            $scope.semesters = data.semesters;            
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate_edit_course = function() {

        
        $scope.validation_error = '';     
        if($scope.course.course == '' || $scope.course.course == undefined) {
            $scope.validation_error = "Please Enter course Name" ;
            return false;
        } else if($scope.semester_list == '') {
            $scope.validation_error = "Please Choose Semesters" ;
            return false;
        } 
        return true;   
     }

    $scope.save_course = function() {
        $scope.is_valid = $scope.validate_edit_course();

        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
            for(var i = 0; i < $scope.course.semester_details.length; i++){
                for(var j = 0; j < $scope.semesters.length; j++){
                    if($scope.semesters[j].id == $scope.course.semester_details[i].semester_id){
                        if($scope.semesters[j].selected = true)
                            $scope.semesters[j].selected = "true"
                    }           
                }
            }

            params = { 
                'course': angular.toJson($scope.course),
                'semester_list': angular.toJson($scope.semester_list),
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
                    document.location.href = '/college/list_course/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
  
    }
}

function EditCollegeController($scope, $http, $element, $location, $timeout) {
    $scope.init = function(csrf_token, college_id){
        $scope.csrf_token = csrf_token;
        $scope.college_id = college_id;
        $scope.url = '/college/edit_college/' + $scope.college_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.college = data.college[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        
    }
     $scope.validate_edit_college = function() {

        
        $scope.validation_error = '';

        if($scope.college.college_name == '' || $scope.college.college_name == undefined) {
            $scope.validation_error = "Please Enter College Name" ;
            return false;
        }   
        else if($scope.college.address == '' || $scope.college.address == undefined) {
            $scope.validation_error = "Please Enter the Address" ;
            return false;
        } else if($scope.college.registration_number == '' || $scope.college.registration_number == undefined) {
            $scope.validation_error = "Please Enter Registration Number";
            return false;                                           
        } else {
            return true;
        } 
     }


    $scope.save_college = function() {
        $scope.is_valid = $scope.validate_edit_college();
        if ($scope.is_valid) {
            $scope.error_flag=false;
            $scope.message = '';
           
            params = { 
                'college': angular.toJson($scope.college),
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
                    document.location.href = '/college/list_college/';
                }
            }).error(function(data, status){
                $scope.error_flag=true;
                $scope.message = data.message;

            });
        }
    }
}

function CollegeController($scope, $element, $http, $timeout, share, $location)
{
    $scope.is_distant = false;
    $scope.is_registration_only = false;
    $scope.init = function(csrf_token)
    {
        $scope.is_distant = false;
        $scope.is_registration_only = false;
        $scope.popup = '';
        $scope.error_flag = false;
        $scope.csrf_token = csrf_token;
        get_course_list($scope, $http);
        get_branch_list($scope, $http);
    }
    $scope.get_registartion_type = function() {
        console.log($scope.course_type);
        if ($scope.course_type == 'Distant') {
            $scope.is_distant = true;
            if ($scope.registration_type == 'Registration Only') {
                $scope.is_registration_only = true;
            } else {
                $scope.is_registration_only = false;
            }
        } else {
            $scope.is_distant = false;
            $scope.is_registration_only = false;
        }
    }
    validate_new_college = function($scope) {
        $scope.validation_error = '';
        if($scope.college_name == '' || $scope.college_name == undefined) {
            $scope.validation_error = "Please Enter College Name" ;
            return false;
        }   
        else if($scope.address == '' || $scope.address == undefined) {
            $scope.validation_error = "Please Enter the Address" ;
            return false;
        } else if($scope.registration_number == '' || $scope.registration_number == undefined) {
            $scope.validation_error = "Please Enter Registration Number";
            return false;                                           
        } else {
            return true;
        } 
    }
    validate_new_branch = function($scope) {
        $scope.validation_error = '';
        if($scope.branch_name == '' || $scope.branch_name == undefined) {
            $scope.validation_error = "Please Enter Branch Name" ;
            return false;
        }   
        else if($scope.address == '' || $scope.address == undefined) {
            $scope.validation_error = "Please Enter the Address" ;
            return false;
                                                  
        } else {
            return true;
        } 
     }

    validate_new_batch = function($scope) {
        $scope.validation_error = '';
        if($scope.course == '' || $scope.course == undefined ){
            $scope.validation_error = "Please Enter Course" ;
            return false;
        } else if($scope.batch_start == '' || $scope.batch_start == undefined) {
            $scope.validation_error = "Please Enter Start Year" ;
            return false;
        } else if($scope.batch_end == '' || $scope.batch_end == undefined) {
            $scope.validation_error = "Please Enter End Year" ;
            return false;
        } else if($scope.batch_end < $scope.batch_start) {
            $scope.validation_error = "Please Check the Strat Year and End Year" ;
            return false;
        } return true;
    }
    validate_new_course = function($scope) {
        $scope.validation_error = '';     
        if($scope.course == '' || $scope.course == undefined) {
            $scope.validation_error = "Please Enter a Course" ;
            return false;
        } else if($scope.university == '' || $scope.university == undefined){
            $scope.validation_error = "Please choose university" ;
            return false;
        } else if($scope.course_type == '' || $scope.course_type == undefined){
            $scope.validation_error = "Please choose Course Type" ;
            return false;
        } else if(($scope.is_distant == true) && ($scope.registration_type == '' || $scope.registration_type == undefined)){
            $scope.validation_error = "Please choose registration type" ;
            return false;
        } else if($scope.semesters == '' || $scope.semesters == undefined){
            $scope.validation_error = "You have to add semesters for creating new course" ;
            return false;
        } else if ($scope.registration_type != 'Registration Only') {
            if($scope.semester_list == '' || $scope.semester_list == undefined){
                $scope.validation_error = "Please Choose a semester" ;
                return false;
            }
        } return true;
    }
    $scope.hide_semesters = function(){
        if ($scope.registration_type == 'Registration Only') {
            $scope.is_registration_only = true;
        } else {
            $scope.is_registration_only = false;
        }
    }
    validate_new_semester = function($scope) {
        $scope.validation_error = '';
        if($scope.semester_name== '' || $scope.semester_name == undefined) {
            $scope.validation_error = "Please Enter Semester" ;
            return false;
        } return true;
    }
    $scope.add_new_college = function(){  
        $scope.popup = new DialogueModelWindow({
                
            'dialogue_popup_width': '38%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_college'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.save_new_college = function() {
        if(validate_new_college($scope)) {
            params = { 
                'college_name': $scope.college_name,
                'address': $scope.address,
                'registration_number': $scope.registration_number,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/college/add_new_college/",
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
                    $scope.popup.hide_popup();                   
                    document.location.href ='/college/list_college/';
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message; 
            });
        }
    } 

    $scope.add_new_branch = function(){         
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '38%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_branch'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.save_new_branch = function() {
        if(validate_new_branch($scope)) {
            params = { 
                'name': $scope.branch_name,
                'address': $scope.address,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/college/add_new_branch/",
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
                    $scope.popup.hide_popup();
                    document.location.href ='/college/list_branch/';
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    } 
    $scope.add_new_batch = function(){  

        new Picker.Date($$('#batch_start'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            pickOnly: 'years',
            format:'%Y',
            canAlwaysGoUp: ['years']
        });
        new Picker.Date($$('#batch_end'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            pickOnly: 'years',
            format:'%Y',
            canAlwaysGoUp: ['years']
        });
        $scope.popup = new DialogueModelWindow({
                
            'dialogue_popup_width': '38%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_batch'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
        $scope.branch = '';
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.save_new_batch = function() {
        $scope.batch_start = $$('#batch_start')[0].get('value');
        $scope.batch_end = $$('#batch_end')[0].get('value');
        if(validate_new_batch($scope)) {
            params = { 
                'course':$scope.course,
                'branch': $scope.branch,
                'batch_start':$scope.batch_start,
                'batch_end':$scope.batch_end,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/college/add_new_batch/",
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
                    $scope.popup.hide_popup();
                    document.location.href ='/college/list_batch/';
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    } 
    $scope.add_new_course = function(){  
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '38%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_course'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
        get_semester_list($scope, $http);
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.save_new_course = function() {
        if(validate_new_course($scope)) {
            if ($scope.semester_list == undefined) 
                $scope.semester_list = []
            params = { 
                'course':$scope.course,
                'semester_list': angular.toJson($scope.semester_list),
                'university': $scope.university,
                'course_type': $scope.course_type,
                'registration_type': $scope.registration_type,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/college/add_new_course/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                hide_spinner();
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.validation_error = data.message;
                } else {
                    $scope.popup.hide_popup();
                    document.location.href ='/college/list_course/';
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.validation_error = data.message;
            });
        }
    } 

    $scope.add_new_semseter = function(){  
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '38%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_semester'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
    $scope.save_new_semester = function() {
        if(validate_new_semester($scope)) {
            params = { 
                'name': $scope.semester_name,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/college/add_new_semester/",
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
                    $scope.popup.hide_popup();
                    document.location.href ='/college/list_semester/';
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    } 


    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }
}

function BranchController($scope, $http, $element) {
    $scope.popup = '';
    $scope.init = function(csrf_token, branch_id) {
        $scope.csrf_token = csrf_token;
        $scope.branch_id = branch_id;
        if ($scope.branch_id) {
            show_spinner();
            $http.get('/college/edit_course_branch/'+$scope.branch_id+'/').success(function(data)
            {
                hide_spinner();
                $scope.branch_name = data.branch_name;
            }).error(function(data, status)
            {
                hide_spinner();
                console.log(data || "Request failed");
            });
        }
    }
    $scope.save_new_branch = function() {
        add_new_branch($scope, $http);
    }
    $scope.add_new_branch = function() {
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '40%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_new_branch'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
}



