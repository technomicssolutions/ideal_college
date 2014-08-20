
function get_attendance_list($scope, $http) {
    var height = $(document).height();
    height = height + 'px';
    
    $('#overlay').css('height', height);
    $('#spinner').css('height', height);
    $http.get('/attendance/batches/').success(function(data)
    {
        $scope.batches = data.batches;
        $('#overlay').css('height', '0px');
        $('#spinner').css('height', '0px');
        $scope.current_month = data.current_month;
        $scope.current_year = data.current_year;
        $scope.current_date = data.current_date;
        $scope.is_holiday = data.is_holiday;        
    }).error(function(data, status)
    {
        $('#overlay').css('height', '0px');
        $('#spinner').css('height', '0px');
        console.log(data || "Request failed");
    });
}

function AttendanceController($scope, $http, $element){
    $scope.batch = {
        'batch_id': '',
        'batch_name': '',
        'current_month': '',
    }
    $scope.students = {}
    $scope.is_edit = false;   
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_attendance_list($scope, $http);
         $scope.show_buttons = true;
    }
    $scope.get_batch_details = function() {
        if ($scope.batch == null) {
            $scope.students = [];
        } else {

            $scope.students = $scope.batch.students;
            if ($scope.students.length == 0) {
                $scope.validation_error = 'No Students';
            }else
            {
                $scope.validation_error = '';
            }
            $scope.period_nos = $scope.batch.period_nos;
            for (var i=0; i < $scope.students.length; i++){
                for (var j=0; j < $scope.students[i].counts.length; j++) {            
                    if ($scope.students[i].counts[j].is_presented == "true" || $scope.students[i].counts[j].is_presented == true) {
                        $scope.students[i].counts[j].is_presented = true;
                    } else {
                        $scope.students[i].counts[j].is_presented = false;
                    }
                }
            } 
            if($scope.is_holiday == "true" || angular.isUndefined($scope.is_holiday)){
                    $scope.show_buttons = false;
                }
                else{
                    $scope.show_buttons = true;    
            }     
        }
    }
    $scope.appliedClass = function(day) {
        if (day.is_holiday == 'true'){
            return "red_color";
        } 
        else if(day.is_future_date == 'true') {
          return "blue_color";  
        }
    }

    $scope.attendance_validation = function() {
        if($scope.batch.batch_id == '' || $scope.batch.batch_id == undefined) {
            $scope.validation_error = 'Please choose batch';
            return false;
        } else if($scope.is_holiday == true || $scope.is_holiday == "true"){
            $scope.validation_error = 'Attendance cannot be marked on holidays';
            return false;
        } return true;
    }
    $scope.edit_attendance = function() {
        $scope.is_edit = true;
    }   

    $scope.save_attendance = function() {
        if($scope.attendance_validation()) {
            var height = $(document).height();
            height = height + 'px';
           
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);

            for (var i=0; i < $scope.students.length; i++){
                for (var j=0; j < $scope.students[i].counts.length; j++) { 
                    if ($scope.students[i].counts[j].is_presented == true) {
                        $scope.students[i].counts[j].is_presented = 'true';
                    } else {
                        $scope.students[i].counts[j].is_presented = 'false';
                    }
                    
                }
            }
            params = { 
                'batch': angular.toJson($scope.batch),
                'students': angular.toJson($scope.students),
                'current_month': $scope.current_month,
                'current_year': $scope.current_year,
                'current_date': $scope.current_date,
                'is_holiday': $scope.is_holiday,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method : 'post',
                url : '/attendance/add_attendance/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                hide_spinner();
                document.location.href = '/attendance/add_attendance/';
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            }).error(function(data, status){
                console.log('error - ', data);
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            });
        }
    }
}

function AttendanceDetailsController($scope, $element, $http) {

    $scope.year = [];
    $scope.batch_month = '';
    $scope.batch_year = '';
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        get_attendance_list($scope, $http);
        $scope.monthly_attendance = false
        $scope.show_batch_select = false
        $scope.daily_attendance = false;
        $scope.show_buttons = false;
        $scope.show_data = false;
        new Picker.Date($$('#attendance_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    var date = new Date();
    var current_year = date.getFullYear(); 
    var start_year = current_year - 4;
    current_year = current_year + 4;
    for(var i=start_year; i<=current_year; i++){
        
        $scope.year.push(i);
    }
    $scope.attendance_validation = function() {
        $scope.validation_error = "";
        if($scope.attendance_view == "1" || $scope.attendance_view == undefined){
            if($scope.batch_id == '' || $scope.batch_id == undefined) {
                $scope.validation_error = 'Please choose the Batch';
                return false;
            } else if($scope.batch_month == '' || $scope.batch_month == undefined) {
                $scope.validation_error = 'Please choose the Month';
                return false;
            } else if($scope.batch_year == '' || $scope.batch_year == undefined) {
                $scope.validation_error = 'Please choose the Year';
                return false;
            } return true;
        }
        else if($scope.attendance_view == "2"){
            $scope.attendance_date = $$('#attendance_date')[0].get('value');
            if($scope.attendance_date == '' || $scope.attendance_date == undefined) {
                $scope.validation_error = 'Please choose the Date';
                return false;
            } return true;
        }

    }
    $scope.appliedClass = function(day) {
        if (day.is_holiday == 'true'){
            return "red_color";
        } 
        else if(day.is_future_date == 'true') {
          return "blue_color";  
        }
    }
    $scope.edit_attendance = function() {
        $scope.is_edit = true;
    }
    $scope.attendance_view_by = function(){
        $scope.validation_error = "";
        if($scope.attendance_view == "1"){            
            $scope.show_batch_select = true;
            $scope.monthly_attendance = true;
            $scope.daily_attendance = false;
            $scope.show_buttons = false;
            $scope.show_data = false;
            $scope.batch_id = "";
        }
        else if($scope.attendance_view == "2"){            
            $scope.show_batch_select = true;       
            $scope.daily_attendance = true;
            $scope.show_buttons = true;
            $scope.monthly_attendance = false;  
            $scope.show_data = false;         
            $scope.batch_id = "";
        }
    }
    $scope.get_attendance_details = function() {
        if ($scope.attendance_validation()) {
            $scope.validation_error = "";
            var height = $(document).height();
            height = height + 'px';
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);
            $scope.validation_error = '';
            $scope.show_data = true;  
            if($scope.attendance_view == "1" || $scope.attendance_view == undefined){
                var url = '/attendance/attendance_details/?batch_id='+$scope.batch_id+'&batch_year='+$scope.batch_year+'&batch_month='+$scope.batch_month;                
            }
            else{
                $scope.attendance_date = $$('#attendance_date')[0].get('value');
                $scope.date_array = $scope.attendance_date.split('/')
                var url = '/attendance/attendance_details/?batch_id='+$scope.batch_id+'&batch_year='+$scope.date_array[2]+'&batch_month='+$scope.date_array[1]+'&batch_day='+$scope.date_array[0];
            }
            
            show_spinner();
            $http.get(url).success(function(data)
            {
                hide_spinner();
                $scope.batch = data.batch[0];
                if($scope.attendance_view == "2")
                    $scope.day_details = data.batch[0].day_details[0];
                $scope.students = data.batch[0].students;
                $scope.columns = data.batch[0].column_count;
                if ($scope.students.length == 0) {
                    $scope.validation_error = 'No Students';
                }
                for (var i=0; i < $scope.students.length; i++){
                    for (var j=0; j < $scope.students[i].counts.length; j++) { 
                        if ($scope.students[i].counts[j].is_presented == "true") {
                            $scope.students[i].counts[j].is_presented = true;
                        } else {
                            $scope.students[i].counts[j].is_presented = false;
                        }
                        
                    }
                }               
                if($scope.day_details == undefined || $scope.day_details.is_future_date == "true" || $scope.day_details.is_holiday == "true"){
                    $scope.show_buttons = false;
                }
                else{
                    $scope.show_buttons = true;    
                }
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            }).error(function(data, status)
            {
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
                console.log(data || "Request failed");
            });
        }
    }
    $scope.save_attendance = function() {
        if($scope.attendance_validation()) {
            var height = $(document).height();
            height = height + 'px';
           
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);

            for (var i=0; i < $scope.students.length; i++){
                for (var j=0; j < $scope.students[i].counts.length; j++) { 
                    if ($scope.students[i].counts[j].is_presented == true) {
                        $scope.students[i].counts[j].is_presented = 'true';
                    } else {
                        $scope.students[i].counts[j].is_presented = 'false';
                    }
                    
                }
            }
            $scope.attendance_date = $$('#attendance_date')[0].get('value');
            $scope.date_array = $scope.attendance_date.split('/')
            params = { 
                'batch': angular.toJson($scope.batch),
                'students': angular.toJson($scope.students),             
                'current_date': $scope.date_array[0], 
                'current_month': $scope.date_array[1],  
                'current_year': $scope.date_array[2],   
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method : 'post',
                url : '/attendance/add_attendance/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {

                hide_spinner();
                document.location.href = '/attendance/attendance_details/';
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            }).error(function(data, status){
                console.log('error - ', data);
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            });
        }
    }
    $scope.clear_batch_details = function() {
        $scope.attendance_view = 1;
        if ($scope.attendance_validation()) {
            $scope.popup = new DialogueModelWindow({
                
                'dialogue_popup_width': '20%',
                'message_padding': '0px',
                'left': '28%',
                'top': '182px',
                'height': 'auto',
                'content_div': '#clear_batch_details_message'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
    $scope.clear_batch = function(){
        $scope.batch_id = '';
        $scope.show_data = false;
        $scope.show_buttons = false;
    }
    $scope.clear_ok = function() {
        document.location.href = '/attendance/clear_batch_details/?batch_id='+$scope.batch_id+'&batch_year='+$scope.batch_year+'&batch_month='+$scope.batch_month;
    }
    $scope.clear_cancel = function() {
        $scope.popup.hide_popup();
    }
}

function HolidayCalendarController($scope, $http, $element) {

    $scope.year = '';
    $scope.month = '';

    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }

    $scope.years = []
    var date = new Date();
    var current_year = date.getFullYear(); 
    var start_year = current_year - 4;
    current_year = current_year + 4;
    for(var i=start_year; i<=current_year; i++){
        
        $scope.years.push(i);
    }

    $scope.appliedClass = function(day) {
        if (day.is_holiday == true) {
            return "blue_color";
        } else{
            return "white_color";
        }
    }

    $scope.attendance_validation = function() {

        if($scope.month == '' || $scope.month == undefined) {
            $scope.validation_error = 'Please choose the Month';
            return false;
        } else if($scope.year == '' || $scope.year == undefined) {
            $scope.validation_error = 'Please choose the Year';
            return false;
        } return true;
    }
    $scope.get_attendance_details = function() {
        if ($scope.attendance_validation()) {         
            var height = $(document).height();
            height = height + 'px';
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);
            $scope.validation_error = '';
            var url = '/attendance/holiday_calendar/?year='+$scope.year+'&month='+$scope.month;
            show_spinner();
            $http.get(url).success(function(data)
            {
                hide_spinner();
                $scope.days = data.days;
                
                for (var i=0; i < $scope.days.length; i++){
                    if ($scope.days[i].is_holiday == "true") {
                        $scope.days[i].is_holiday = true;
                    } else {
                        $scope.days[i].is_holiday = false;
                    }
                }
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
            }).error(function(data, status)
            {
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
                console.log(data || "Request failed");
            });
        }
    }

    $scope.save_holiday_calendar = function(){
        if ($scope.attendance_validation()) {
            var height = $(document).height();
            height = height + 'px';
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);
            for (var i=0; i<$scope.days.length; i++){
                if ($scope.days[i].is_holiday == true) {
                    
                    $scope.days[i].is_holiday = 'true'
                } else {
                    $scope.days[i].is_holiday = 'false';
                }
            }
            params = {
                'year': $scope.year,
                'month': $scope.month,
                'holiday_calendar': angular.toJson($scope.days),
                'csrfmiddlewaretoken': $scope.csrf_token,
            }
            show_spinner();
            $http({
                method : 'post',
                url : '/attendance/holiday_calendar/',
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {

                hide_spinner();
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
               document.location.href = '/attendance/holiday_calendar/'
            }).error(function(data, status){
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
                console.log('error - ', data);
            });
        }
    }

    $scope.clear_holiday_calendar_ok = function() {
        document.location.href = '/attendance/clear_holiday_calendar/?year='+$scope.year+'&month='+$scope.month;
    }
    $scope.clear_cancel = function() {
        $scope.popup.hide_popup();
    }
    $scope.remove_holiday_calendar = function() {
        if ($scope.attendance_validation()) {
            $scope.popup = new DialogueModelWindow({
                
                'dialogue_popup_width': '20%',
                'message_padding': '0px',
                'left': '28%',
                'top': '182px',
                'height': 'auto',
                'content_div': '#clear_holiday_message'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
        }
    }
}