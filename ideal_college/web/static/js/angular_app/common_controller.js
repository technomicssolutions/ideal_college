/************************** Common JS F************/

function show_spinner (){
    $('#spinner_overlay').css('display', 'block');
    $('#spinner').css('display', 'block');
}

function hide_spinner (){
    $('#spinner_overlay').css('display', 'none');
    $('#spinner').css('display', 'none');
}

function paginate(list, $scope, page_interval) {
    if(!page_interval)
        var page_interval = 20;
    $scope.current_page = 1;
    $scope.pages = list.length / page_interval;
    if($scope.pages > parseInt($scope.pages))
        $scope.pages = parseInt($scope.pages) + 1;
    $scope.visible_list = list.slice(0, page_interval);
}
    
function select_page(page, list, $scope, page_interval) {
    if(!page_interval)
        var page_interval = 20;
    var last_page = page - 1;
    var start = (last_page * page_interval);
    var end = page_interval * page;
    $scope.visible_list = list.slice(start, end);
    $scope.current_page = page;
}

function get_semester_list($scope, $http) {
    $http.get('/college/list_semester/').success(function(data)
    {
        $scope.semesters = data.semesters;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}
function get_branch_list($scope, $http) {
    $http.get('/college/branch_list/').success(function(data)
    {
        $scope.branch_list = data.branch_list;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function add_new_branch($scope, $http) {
    if ($scope.branch_name == '' || $scope.branch_name == undefined) {
        $scope.validation_error = 'Please enter the Branch Name';
    } else {
        $scope.validation_error = '';
        params = {
            'csrfmiddlewaretoken': $scope.csrf_token,
            'branch_name': $scope.branch_name,
            'branch_id': $scope.branch_id,
        }
        show_spinner();
        $http({
            method: 'post',
            url: "/college/save_new_branch/",
            data: $.param(params),
            headers: {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
            hide_spinner();
            if (data.result == 'error'){
                $scope.validation_error = data.message;
            } else {
                if ($scope.popup)
                    $scope.popup.hide_popup();
                document.location.href ='/college/branch_list/';
            }
        }).error(function(data, success){
            
        }); 
    }
}
function validateEmail(email) { 
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}
function get_designation($scope, $http) {
    $http.get($scope.url).success(function(data)
    {
        $scope.designations = data.designations;
    }).error(function(data, status){
        console.log(data || "Request failed");
    });
}
function get_fee_structure_details($scope, $http, fees_structure_id) {
    var url = '/fees/edit_fees_structure_details/'+fees_structure_id+'/';
    $http.get(url).success(function(data){
        $scope.fees_structure = data.fees_structure[0];
        $scope.no_installments = data.fees_structure[0].no_installments;
        $scope.fees_structure.removed_heads = [];
        if ($('#edit_fee_structure').length > 0) {
            for (var i=0; i<$scope.fees_structure.fees_head.length; i++) {
                for(var j=0; j<$scope.fees_structure.fees_head[i].installments.length; j++){
                    if ($scope.fees_structure.fees_head[i].installments[j].is_not_late_payment == 'true') {
                        $scope.fees_structure.fees_head[i].installments[j].is_not_late_payment = true;
                    } else {
                        $scope.fees_structure.fees_head[i].installments[j].is_not_late_payment = false;
                    }
                } 
            }
        }
    }).error(function(data, status){
       console.log(data || "Request failed");
    })
}
function get_course_list($scope, $http) {
    $http.get('/college/list_course/').success(function(data)
    {
        $scope.courses = data.courses;
    }).error(function(data, status)
    {
        console.log(data || "Request failed");
    });
}

function get_course_batch_list($scope, $http) {
    if ($scope.course != null) {
        $http.get('/college/get_batch/'+ $scope.course+ '/').success(function(data)
        {
            $scope.batches = data.batches;
            $scope.no_head_error = '';
            $scope.no_student_error = '';
            $scope.no_installment_error = '';
            if ($scope.batches.length == 0) {
                $scope.no_batch_error = 'No batch in this course';
                if ($$('#fee_structure').length > 0)
                    $scope.validation_error = 'No batch in this course';
            } else {
                $scope.no_batch_error = '';
                $scope.validation_error = '';
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    } else {
        $scope.batches = [];
    }
}

function get_course_batch_student_list($scope, $http) {
    if (($scope.course != 'select') && (($scope.batch != 'select'))) {
        $http.get('/academic/get_student/'+ $scope.course+ '/'+ $scope.batch+ '/').success(function(data)
        {
            $scope.students = data.students;
            $scope.no_head_error = '';
            $scope.no_installment_error = '';
            if ($scope.students.length == 0) {
                $scope.no_student_error = 'No students in this batch';
            } else {
                $scope.no_student_error = '';
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
}

function date_conversion(date_val) {
    var date_value = date_val.split('/');
    var converted_date = new Date(date_value[2],date_value[1]-1, date_value[0]);
    return converted_date;
}

function calculate_total_fee_amount() {
    var due_date = date_conversion($$('#due_date')[0].get('value'));
    var paid_date = date_conversion($$('#paid_date')[0].get('value'));
    console.log($('#balance').val());
    var balance_amount = $('#balance').val();
    if (paid_date > due_date) {
        $('#total_fee_amount').val(parseFloat($('#fee_amount').val()) + parseFloat($('#fine_amount').val()));

        $('#balance_amount').val(parseFloat(balance_amount) + parseFloat($('#fine_amount').val()));
    } else {
        $('#total_fee_amount').val(parseFloat($$('#fee_amount')[0].get('value')));
        $('#balance_amount').val(balance_amount);
    }
}

function get_fees_head_details($scope, $http, fees_head_id) {
    $http.get('/fees/edit_fees_head/'+fees_head_id+'/').success(function(data){
        $scope.fee_head = data.fees_head[0];
    }).error(function(data, status){
        console.log(data || 'Request failed');
    });
}

function get_fee_structure_head_details($scope, $http) {
    $http.get('/fees/get_applicable_fee_structure_head/'+$scope.course+'/'+$scope.batch+'/').success(function(data){
        $scope.heads = data.heads;
    }).error(function(data, status){
        console.log(data || 'Request failed');
    });
}
/************************** End Common JS Functions *****************************/

