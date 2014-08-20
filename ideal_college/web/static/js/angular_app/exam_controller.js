function get_exams($scope, $http, from) {
        $scope.validation_error = ""   
        $scope.visible_list = [];
        if ($scope.course != null && $scope.batch != null && $scope.semester != null) {
            $scope.url = '/exam/get_exam/'+ $scope.course+ '/'+ $scope.batch+ '/'+ $scope.semester+ '/';
            show_spinner();
            $http.get($scope.url).success(function(data)
            {
                hide_spinner();
                if (from == 'mark') {
                    if (data.students.length > 0) {
                        if(data.students[0].exam_marks == ''){
                            $scope.edit_marks = false;    
                            $scope.validation_error = "No data to display"
                        } else {
                            $scope.students = data.students
                            paginate($scope.students, $scope, 2);
                            $scope.exams = data.students[0].exam_list;
                            $scope.edit_marks = true;    
                            $scope.validation_error = "";
                        } 
                    } else {
                        $scope.validation_error = "No students in this batch";
                    }  
                } else {
                    console.log(data);
                    if (data.exam_details.length == 0){
                        $scope.validation_error = 'No exams scheduled';
                    } else {
                        $scope.exams = data.exam_details;
                    }
                }        
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
        }
}
function ExamController($scope, $element, $http, $timeout, share, $location)
{
    $scope.init = function(csrf_token)
    {
        $scope.popup = '';
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.edit_marks = false;
        $scope.display_marks = false;
        $scope.exam = {
            'exam': '',
            'total_mark': '',
            'no_subjects':'',
            'id' :'',
            'subjects': ''               
        }
        $scope.subjects = [];
        get_course_list($scope, $http);
        var date_pick = new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        var date_pick = new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        $scope.visible_list = [];
    }
    $scope.attach_subject_datepicker = function(){
        for(var i=0;i<$scope.subjects.length;i++){
            var date_pick = new Picker.Date($$('#subject_date_'+i), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
            });
        }
    }
    $scope.attach_subject_start_time_picker = function(index){
        var date_pick = new Picker.Date($$('#subject_start_time_'+index), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%X',
            ampm: true,
            timePickerOnly: true
        });
    }
    $scope.attach_subject_end_time_picker = function(index){
        var date_pick = new Picker.Date($$('#subject_end_time_'+index), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%X',
            ampm: true,
            timePickerOnly: true
        });
    }
    $scope.calculate_total_marks = function(){
        var total = 0;
        for(var i=0; i<$scope.subjects.length; i++) {
            total = total + parseFloat($scope.subjects[i].total_mark);
        }
        $scope.exam_total = total;
    }

    $scope.hide_popup_windows = function(){
        $('#add_exam_schedule_details')[0].setStyle('display', 'none'); 
    }

    $scope.add_new_exam_schedule = function() {
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        $scope.hide_popup_windows();
        $('#add_exam_schedule_details')[0].setStyle('display', 'block');
        $scope.popup = new DialogueModelWindow({

            'dialogue_popup_width': '68%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_exam_schedule_details'
        });

        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }

    $scope.add_subjects = function(){
        var subjects = $scope.no_subjects;
        var diff = $scope.no_subjects - $scope.subjects.length;
        if (diff > 0) {
            for (i=0; i <diff; i++){
                $scope.subjects.push({
                    'subject_name': '',
                    'start_time': '', 
                    'end_time': '',
                    'total_mark': '',
                    'pass_mark': '',
                                 
                });
            }
        } else {
            diff = $scope.subjects.length - $scope.no_subjects;
            for (i=diff; i >0; i--){
                last_index = $scope.subjects.indexOf($scope.subjects[$scope.subjects.length - 1]);
                $scope.subjects.splice(last_index, 1);
            }
        }
    }
    $scope.validate_exam_schedule = function() {

        $scope.validation_error = '';
        $scope.start_date = $$('#start_date')[0].get('value');
        $scope.end_date = $$('#end_date')[0].get('value');
        if($scope.exam_name == '' || $scope.exam_name == undefined) {
            $scope.validation_error = "Please Enter a exam name " ;
            return false;
        }else if($scope.course == '' || $scope.course == undefined) {
            $scope.validation_error = "Please Select a course " ;
            return false;
        }else if($scope.batch == '' || $scope.batch == undefined) {
            $scope.validation_error = "Please Select a batch name" ;
            return false;
        }else if($scope.start_date == '' || $scope.start_date == undefined) {
            $scope.validation_error = "Please Select a start date" ;
            return false;
        }else if($scope.end_date == '' || $scope.end_date == undefined) {
            $scope.validation_error = "Please Select a end date" ;
            return false;
        }else if($scope.no_subjects == '' || $scope.no_subjects == undefined || !Number($scope.no_subjects)) {
            $scope.validation_error = "Please Enter no of subjects" ;
            return false;
        }else if($scope.no_subjects.length > 0){
            for(var i=0;i<$scope.no_subjects.length;i++){
                if($scope.subjects[i].subject_name == '' || $scope.subjects[i].subject_name == undefined) {
                    $scope.validation_error = "Please Enter  subject name" ;
                    return false;
                }else if($scope.subjects[i].start_time == '' || $scope.subjects[i].start_time == undefined) {
                    $scope.validation_error = "Please Enter start time" ;
                    return false;
                }else if($scope.subjects[i].end_time == '' || $scope.subjects[i].end_time == undefined) {
                    $scope.validation_error = "Please Enter end time" ;
                    return false;
                }else if($scope.subjects[i].total_mark == '' || $scope.subjects[i].total_mark == undefined || !Number($scope.subjects[i].total_mark)) {
                    $scope.validation_error = "Please Enter total marks" ;
                    return false;
                }else if($scope.subjects[i].pass_mark == '' || $scope.subjects[i].pass_mark == undefined || !Number($scope.subjects[i].pass_mark)) {
                    $scope.validation_error = "Please Enter pass mark" ;
                    return false;
                }else if($scope.subjects[i].date == '' || $scope.subjects[i].date == undefined) {
                    $scope.validation_error = "Please Enter subject date" ;
                    return false;
                }
            }
        }
        return true;   
    }
    $scope.save_new_exam_schedule = function() {
        for(var i=0;i<$scope.subjects.length;i++){
            $scope.subjects[i].date = $$('#subject_date_'+i)[0].get('value');
            $scope.subjects[i].end_time = $$('#subject_end_time_'+i)[0].get('value');
            $scope.subjects[i].start_time = $$('#subject_start_time_'+i)[0].get('value');
        }
        if($scope.validate_exam_schedule()) {
            $scope.start_date = $$('#start_date')[0].get('value');
            $scope.end_date = $$('#end_date')[0].get('value');
            params = { 
                'exam_name':$scope.exam_name,
                'course': $scope.course,
                'batch': $scope.batch,
                'semester': $scope.semester,
                'start_date': $scope.start_date,
                'end_date': $scope.end_date,
                'exam_total': $scope.exam_total,
                'no_subjects': $scope.no_subjects,                   
                'subjects': angular.toJson($scope.subjects),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/exam/save_new_exam_schedule/",
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
                    document.location.href ='/exam/schedule_exam/';                    
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
    $scope.display_exam_schedule = function(exam) {
        $scope.exam_schedule_id = exam.id;
        $scope.url = '/exam/view_exam_schedule/' + $scope.exam_schedule_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.exam_schedule = data.exam_schedule[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        $scope.hide_popup_windows();
        $('#exam_schedule_details_view')[0].setStyle('display', 'block');
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '90%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#exam_schedule_details_view'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.get_batch = function(){
        $scope.edit_marks = false;
        $scope.display_marks = false;       
        $scope.url = '/college/get_batch/'+ $scope.course+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.batches = data.batches;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        var url = '/college/get_semester/?id='+$scope.course;
        show_spinner();
        $http.get(url).success(function(data) {
            hide_spinner();
            $scope.semesters = data.semesters;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.get_exam_schedules = function() {
        $scope.message = '';
        $scope.url = '/exam/schedule_exam/?course='+ $scope.course+ '&batch='+ $scope.batch;
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.exams = data.exams;
            if($scope.exams.length == 0){
                $scope.message = "No exams Scheduled yet";
            } else {
                paginate($scope.exams, $scope);
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    } 
    $scope.select_page = function(page){
        select_page(page, $scope.exams, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.close_popup = function(){
        $scope.edit_marks = false;
        $scope.display_marks = false;
        $scope.popup.hide_popup();
    }
}

function EditExamController($scope, $element, $http, $timeout, share, $location)
{
    $scope.init = function(csrf_token, exam_schedule_id)
    {
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.exam_schedule_id = exam_schedule_id;
        $scope.get_exam_schedule_details();
        new Picker.Date($$('#start_date'), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
        });
        new Picker.Date($$("#end_date"), {
                timePicker: false,
                positionOffset: {x: 5, y: 0},
                pickerClass: 'datepicker_bootstrap',
                useFadeInOut: !Browser.ie,
                format:'%d/%m/%Y',
        });
        $scope.attached_date_picker = false;
    }
    $scope.get_exam_schedule_details = function(){
        $scope.url = '/exam/view_exam_schedule/' + $scope.exam_schedule_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.exam_schedule = data.exam_schedule[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.attach_subject_start_time_picker = function(index){
        var date_pick = new Picker.Date($$('#subject_start_time_'+index), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%X',
            ampm: true,
            timePickerOnly: true
        });
    }
    $scope.attach_subject_end_time_picker = function(index){
        var date_pick = new Picker.Date($$('#subject_end_time_'+index), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%X',
            ampm: true,
            timePickerOnly: true
        });
    }
    $scope.attach_date_picker = function() {   
        if(!$scope.attached_date_picker)     {
            for(i=0; i<$scope.exam_schedule.subjects.length; i++){
                var id_name = '#';
                id_name = id_name + 'subject_date_'+i;
                new Picker.Date($$(id_name), {
                    timePicker: false,
                    positionOffset: {x: 5, y: 0},
                    pickerClass: 'datepicker_bootstrap',
                    useFadeInOut: !Browser.ie,
                    format:'%d/%m/%Y',
                });
            } 
        }        
    }
    $scope.validate_exam_schedule = function() {
        $scope.validation_error = '';
        if($scope.exam_schedule.exam_name == '' || $scope.exam_schedule.exam_name == undefined) {
            $scope.validation_error = "Please Enter a exam name ";
            return false;
        }else if($scope.exam_schedule.course == '' || $scope.exam_schedule.course == undefined) {
            $scope.validation_error = "Please Select a course ";
            return false;
        }else if($scope.exam_schedule.batch == '' || $scope.exam_schedule.batch == undefined) {
            $scope.validation_error = "Please Select a batch name";
            return false;
        }else if($scope.exam_schedule.start_date == '' || $scope.exam_schedule.start_date == undefined) {
            $scope.validation_error = "Please Select a start date";
            return false;
        }else if($scope.exam_schedule.end_date == '' || $scope.exam_schedule.end_date == undefined) {
            $scope.validation_error = "Please Select a end date";
            return false;
        }else if($scope.exam_schedule.no_subjects == '' || $scope.exam_schedule.no_subjects == undefined || !Number($scope.exam_schedule.no_subjects)) {
            console.log($scope.exam_schedule.no_subjects);
            $scope.validation_error = "Please Enter no of subjects";
            return false;
        }else if($scope.exam_schedule.no_subjects > 0){
            for(var i=0;i<$scope.exam_schedule.subjects.length;i++){
                if($scope.exam_schedule.subjects[i].subject_name == '' || $scope.exam_schedule.subjects[i].subject_name == undefined) {
                    $scope.validation_error = "Please Enter  subject name";
                    return false;
                }else if($scope.exam_schedule.subjects[i].start_time == '' || $scope.exam_schedule.subjects[i].start_time == undefined) {
                    $scope.validation_error = "Please Enter start time" ;
                    return false;
                }else if($scope.exam_schedule.subjects[i].end_time == '' || $scope.exam_schedule.subjects[i].end_time == undefined) {
                    $scope.validation_error = "Please Enter end time" ;
                    return false;
                }else if($scope.exam_schedule.subjects[i].total_mark == '' || $scope.exam_schedule.subjects[i].total_mark == undefined || !Number($scope.exam_schedule.subjects[i].total_mark)) {
                    $scope.validation_error = "Please Enter total marks" ;
                    return false;
                }else if($scope.exam_schedule.subjects[i].pass_mark == '' || $scope.exam_schedule.subjects[i].pass_mark == undefined || !Number($scope.exam_schedule.subjects[i].pass_mark)) {
                    $scope.validation_error = "Please Enter pass mark" ;
                    return false;
                }else if($scope.exam_schedule.subjects[i].date == '' || $scope.exam_schedule.subjects[i].date == undefined) {
                    $scope.validation_error = "Please Select a subject date" ;
                    return false;
                }
            }
        }
        return true;   
    }
    $scope.save_exam_schedule = function() {
        for(var i=0;i<$scope.exam_schedule.subjects.length;i++){
            $scope.exam_schedule.subjects[i].date = $$('#subject_date_'+i)[0].get('value');
            $scope.exam_schedule.subjects[i].end_time = $$('#subject_end_time_'+i)[0].get('value');
            $scope.exam_schedule.subjects[i].start_time = $$('#subject_start_time_'+i)[0].get('value');
        }
        $scope.exam_schedule.start_date = $$('#start_date')[0].get('value');
        $scope.exam_schedule.end_date = $$('#end_date')[0].get('value');
        if($scope.validate_exam_schedule()) {            
            params = { 
                'exam_name':$scope.exam_schedule.exam_name,
                'course': $scope.exam_schedule.course,
                'batch': $scope.exam_schedule.batch,
                'semester': $scope.exam_schedule.semester,
                'start_date': $scope.exam_schedule.start_date,
                'end_date': $scope.exam_schedule.end_date,
                'exam_total': $scope.exam_schedule.exam_total,
                'no_subjects': $scope.exam_schedule.no_subjects,                   
                'subjects': angular.toJson($scope.exam_schedule.subjects),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/exam/edit_exam_schedule/"+$scope.exam_schedule_id+"/",
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
                    document.location.href ='/exam/schedule_exam/';
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
    $scope.add_subject = function(){
        $scope.exam_schedule.subjects.push({
            "subject_id": "", 
            "subject_name": "", 
            "pass_mark": "", 
            "total_mark": "", 
            "end_time": "", 
            "date": "", 
            "start_time": ""
        })
        $scope.attached_date_picker = false;
        $scope.attach_date_picker();
        $scope.exam_schedule.no_subjects = $scope.exam_schedule.no_subjects + 1;
    }
    $scope.remove_subject = function(subject){
        index = $scope.exam_schedule.subjects.indexOf(subject);
        $scope.exam_schedule.subjects.splice(index, 1);
        $scope.exam_schedule.no_subjects = $scope.exam_schedule.no_subjects - 1;
    }
    $scope.calculate_total_marks = function(){
        var total = 0;
        for(var i=0; i<$scope.exam_schedule.subjects.length; i++) {
            total = total + parseFloat($scope.exam_schedule.subjects[i].total_mark);
        }
        $scope.exam_schedule.exam_total = total;
    }    
}

function MarksController($scope, $element, $http, $timeout, share, $location)
{
    $scope.init = function(csrf_token)
    {
        $scope.popup = '';
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.edit_marks = false;
        $scope.display_marks = false;
        $scope.exam = {
            'exam': '',
            'total_mark': '',
            'no_subjects':'',
            'id' :'',
            'subjects': ''               
        }
        $scope.subjects = [];
        $scope.visible_list = [];
        get_course_list($scope, $http);
        var date_pick = new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });

        var date_pick = new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.clear_data = function(){
        $scope.visible_list = [];
        $scope.semester = '';
    }
    $scope.get_batch = function(){
        $scope.edit_marks = false;
        $scope.display_marks = false;
        $scope.visible_list = []; 
        $scope.url = '/college/get_batch/'+ $scope.course+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.batches = data.batches;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
        var url = '/college/get_semester/?id='+$scope.course;
        show_spinner();
        $http.get(url).success(function(data) {
            hide_spinner();
            $scope.semesters = data.semesters;
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.validate_marks = function(marks) {        
        $scope.validation_error = '';
        $scope.flag = 0;
        if (marks != undefined) {
            for(var i = 0; i < marks.length; i++){
                for(var j = 0; j < marks[i].exam_marks.length; j++){                        
                    for(var k = 0; k < marks[i].exam_marks[j].subjects.length; k++){                    
                        if(!Number(marks[i].exam_marks[j].subjects[k].mark) && marks[i].exam_marks[j].subjects[k].mark.length > 0 )
                            $scope.flag = 1;                    
                        else if((Number(marks[i].exam_marks[j].subjects[k].mark) > Number(marks[i].exam_marks[j].subjects[k].maximum) ) && marks[i].exam_marks[j].subjects[k].mark != '' ){
                            $scope.validation_error = "Invalid entry, maximum mark is "+marks[i].exam_marks[j].subjects[k].maximum ;
                            return false; 
                        }                       
                    }                                           
                }
            }
        }
        if($scope.course == '' || $scope.course== undefined) {
            $scope.validation_error = "Please select course " ;
            return false;
        } else if($scope.batch == '' || $scope.batch== undefined) {
            $scope.validation_error = "Please select batch " ;
            return false;
        } else if($scope.semester == '' || $scope.semester== undefined) {
            $scope.validation_error = "Please select semester " ;
            return false;
        } else if($scope.flag == 1){
            $scope.validation_error = "Invalid entry in mark field " ;  
            return false;             
        } else if($scope.validation_error == ''){
            return true     
        } else {
            return false;
        }
    }

    $scope.save_marks = function(marks) {
        console.log(marks);
        if($scope.validate_marks(marks)){   
            params = { 
                'course': $scope.course,
                'batch': $scope.batch,
                'semester': $scope.semester,
                'student': angular.toJson(marks),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/exam/save_marks/",
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
                    $scope.close_popup();
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }  
    }              
    $scope.hide_popup_windows_mark = function(){
        $('#add_marks')[0].setStyle('display', 'none');
        $('#view_marks')[0].setStyle('display', 'none');
    }
    $scope.close_popup = function(){
        $scope.edit_marks = false;
        $scope.display_marks = false;
        $scope.popup.hide_popup();
        get_course_list($scope, $http);
        $scope.batch = '';
        $scope.semester = '';
        $scope.visible_list = [];
    }  
    $scope.view_marks = function() {
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '90%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#view_marks'
        });
        $scope.close_popup();
        $scope.hide_popup_windows_mark();
        $('#view_marks')[0].setStyle('display', 'block');        
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    
    $scope.get_marks_details = function(){        
        $scope.url = '/exam/view_marks/' + $scope.course+ '/'+ $scope.batch+ '/'+ $scope.student+ '/'+ $scope.exam+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.exam_marks = data.exam_marks[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.add_marks = function() {
        $scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '90%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#add_marks'
        });
        $scope.close_popup();
        $scope.hide_popup_windows_mark();
        $('#add_marks')[0].setStyle('display', 'block');       
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }     

    $scope.get_exams = function(){    
        get_exams($scope, $http, 'mark')
    } 
    $scope.select_page = function(page){
        select_page(page, $scope.students, $scope, 2);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
}

function ExamReportController($scope, $http){
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_course_list($scope, $http);
    }
    $scope.get_batch = function() {
        get_course_batch_list($scope, $http);
    }
    $scope.get_semesters = function() {
        get_semester_list($scope, $http);
    }
    $scope.get_exams = function() {
        get_exams($scope, $http, 'exam_report')
    }
    $scope.view_report = function() {
        if ($scope.course == '' || $scope.course == null || $scope.course == undefined) {
            $scope.validation_error = 'Please choose course';
        } else if ($scope.batch == '' || $scope.batch == null || $scope.batch == undefined) {
            $scope.validation_error = 'Please choose batch';
        } else if ($scope.semester == '' || $scope.semester == null || $scope.semester == undefined) {
            $scope.validation_error = 'Please choose semester';
        } else if ($scope.exam == '' || $scope.exam == null || $scope.exam == undefined) {
            $scope.validation_error = 'Please choose exam';
        } else {
            document.location.href = '/report/exam_schedule_report/?report_type=exam_schedule&exam_id='+$scope.exam;
        }
    }
}