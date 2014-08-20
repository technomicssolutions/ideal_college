function FeesPaymentController($scope, $element, $http, $timeout, share, $location)
{
    $scope.payment_installment = {
        'installment_id': '',
        'course_id': '',
        'batch_id': '',
        'student_id': '',
        'head_id': '',
        'paid_date': '',
        'total_amount': '',
        'paid_amount': '',
        'paid_installment_amount': '',
        'balance': '',
    }
    $scope.course = 'select';
    $scope.batch = 'select';
    $scope.payment_installment.student = 'select';
    $scope.head = '';
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        var paid_date = new Picker.Date($$('#paid_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_course_list($scope, $http);
    }
    $scope.get_batch = function(){
        get_course_batch_list($scope, $http);
    }
    $scope.get_student = function(){
        get_course_batch_student_list($scope, $http);
    }
    $scope.get_fees_head = function(){
        $scope.url = '/fees/get_fee_structure_head/'+ $scope.course+ '/'+ $scope.batch+ '/'+$scope.payment_installment.student+'/';
        if ($scope.course !='select' && $scope.batch != 'select' && $scope.payment_installment.student != 'select')
            show_spinner();
            $http.get($scope.url).success(function(data)
            {
                hide_spinner();
                $scope.heads = data.heads;
                $scope.installments = [];
                $scope.payment_installment.amount = '';
                $scope.payment_installment.due_date = '';
                $scope.payment_installment.fine = '';
                $('#balance').val(0);
                $('#total_fee_amount').val(0);
                if ($scope.heads.length == 0) {
                    $scope.no_head_error = 'No fees structure for this batch';
                } else {
                    $scope.no_head_error = '';
                }
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
    }
    $scope.get_installment = function() {
        if ($scope.head.installments.length == 0) {
            $scope.no_installment_error = 'Payment completed';
        } else {
            $scope.no_installment_error = '';
        }
        $scope.installments = $scope.head.installments;
        $('#due_date').val('');
        $('#fine_amount').val(0);
        $('#fee_amount').val(0);
        $('#total_fee_amount').val(0);
    }
    $scope.calculate_total_amount = function() {
        calculate_total_fee_amount();
    }
    $scope.get_fees = function() {
        $scope.payment_installment.paid_date = $scope.installment.paid_date;
        $scope.payment_installment.due_date = $scope.installment.due_date;
        $scope.payment_installment.amount = $scope.installment.amount;
        $scope.payment_installment.fine = $scope.installment.fine_amount;
        $scope.payment_installment.paid_installment_amount = $scope.installment.paid_installment_amount;
        $('#due_date').val($scope.installment.due_date);
        $('#fine_amount').val($scope.installment.fine_amount);
        $('#fee_amount').val($scope.installment.amount);
        $('#balance').val($scope.installment.balance);
        $('#balance_amount').val($scope.installment.balance);
        calculate_total_fee_amount();
    }
    $scope.validate_fees_payment = function() {
        $scope.validation_error = '';
        if($scope.course == 'select') {
            $scope.validation_error = "Please Select a course " ;
            return false
        } else if($scope.batch == 'select') {
            $scope.validation_error = "Please Select a batch " ;
            return false;
        } else if($scope.payment_installment.student == 'select') {
            $scope.validation_error = "Please select a student" ;
            return false;
        } else if($scope.head == '' || $scope.head == undefined) {
            $scope.validation_error = "Please enter a head name" ;
            return false;
        } else if($scope.installment == '' || $scope.installment == undefined) {
            $scope.validation_error = "Please enter an installment" ;
            return false;
        } else if ($scope.payment_installment.paid_amount == '' || $scope.payment_installment.paid_amount == undefined) {
            $scope.validation_error = "Please enter paid amount" ;
            return false;
        } else if ($scope.payment_installment.paid_amount != Number($scope.payment_installment.paid_amount)) {
            $scope.validation_error = "Please enter valid paid amount" ;
            return false;
        } else if ($scope.payment_installment.paid_amount != $scope.payment_installment.balance) {
            $scope.validation_error = "Please check the balance amount with paid amount" ;
            return false;
        } return true; 
    }
    $scope.save_fees_payment = function() {

        $scope.payment_installment.course_id = $scope.course;
        $scope.payment_installment.batch_id = $scope.batch;
        $scope.payment_installment.installment_id = $scope.installment.id;
        $scope.payment_installment.head_id = $scope.head.id;
        $scope.payment_installment.paid_date = $$('#paid_date')[0].get('value');
        $scope.payment_installment.total_amount = $$('#total_fee_amount')[0].get('value');
        $scope.payment_installment.balance = $$('#balance_amount')[0].get('value');
        if($scope.validate_fees_payment()) {
            params = { 
                'fees_payment': angular.toJson($scope.payment_installment),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/fees/fees_payment/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                hide_spinner();
                if (data.result == 'error'){
                    $scope.validation_error = data.message;
                } else {              
                    document.location.href ="/fees/fees_payment/";
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}
function FeesController($scope, $element, $http, $timeout, share, $location)
{
    $scope.student_id = 'select';
    $scope.course = 'select';
    $scope.batch = 'select';
    $scope.fees_type = '';
    $scope.filtering_option = '';
    $scope.url = '';
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        $scope.popup = '';
        get_course_list($scope, $http);
    }
    $scope.get_batch = function(){
        $scope.filtering_option = '';
        get_course_batch_list($scope, $http);
    }
    $scope.get_student = function(){
        $scope.filtering_option = '';
        get_course_batch_student_list($scope, $http);
    }
    $scope.hide_popup_windows = function(){
        $('#fees_structure_details_view')[0].setStyle('display', 'none');
    }
    $scope.select_page = function(page){
        select_page(page, $scope.fees_details.students, $scope, 2);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.outstanding_fees_details = function(){ 
        $scope.url = '';
        if ($scope.student_id == '' || $scope.student_id == undefined) {
            $scope.student_id = 'select';
            $scope.fees_details = [];
        }
        if (($scope.fees_type != '' || $scope.fees_type != undefined) && ($scope.filtering_option != '' || $scope.filtering_option != undefined)) {
            if ($scope.course != '' && $scope.batch != '') {
                if ($scope.filtering_option == 'student_wise' && $scope.student_id != 'select') {
                    $scope.url = '/fees/get_outstanding_fees_details/?course='+$scope.course+ '&batch='+ $scope.batch+ '&student_id='+$scope.student_id+'&filtering_option='+$scope.filtering_option+'&fees_type='+$scope.fees_type;
                } else if($scope.filtering_option == 'batch_wise') {
                    $scope.url = '/fees/get_outstanding_fees_details/?course='+$scope.course+ '&batch='+ $scope.batch+ '&filtering_option='+$scope.filtering_option+'&fees_type='+$scope.fees_type;
                }
            }
        }
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            if (data.result == 'ok') 
                $scope.fees_details = data.fees_details[0];
                console.log($scope.fees_details.students);
                if($scope.fees_details.students)
                    paginate($scope.fees_details.students, $scope, 2);
            else {
                $scope.no_student_error = data.message;
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }    
    $scope.close_popup = function(){
        $scope.popup.hide_popup();
    }   
}

function EditFeeStructureController($scope, $http, $element) {
    
    $scope.init = function(csrf_token, fees_structure_id){
        $scope.csrf_token = csrf_token;
        $scope.fees_structure_id = fees_structure_id;
        get_fee_structure_details($scope, $http, $scope.fees_structure_id);
    }

    $scope.edit_fee_structure_validation = function() {
        if ($scope.fees_structure.fees_head.length == 0) {
            $scope.validation_error = 'Please add fees details';
            return false;
        } else if ($scope.fees_structure.fees_head.length > 0) {
            for (var i=0; i<$scope.fees_structure.fees_head.length; i++) {
                total_installment_amount = 0;
                if ($scope.fees_structure.fees_head[i].installments.length > 0) {
                    for (var j=0; j<$scope.fees_structure.fees_head[i].installments.length; j++) {
                        if ($scope.fees_structure.fees_head[i].installments[j].amount == Number($scope.fees_structure.fees_head[i].installments[j].amount))
                            total_installment_amount = parseFloat(total_installment_amount) + parseFloat($scope.fees_structure.fees_head[i].installments[j].amount);
                    }
                }
                if($scope.fees_structure.fees_head[i].head == '' || $scope.fees_structure.fees_head[i].head == undefined) {
                    $scope.validation_error = "Please enter head in the row "+(i + 1);
                    return false;                                           
                } else if($scope.fees_structure.fees_head[i].amount == '' || $scope.fees_structure.fees_head[i].amount == undefined || $scope.fees_structure.fees_head[i].amount == 0) {
                    $scope.validation_error = "Please enter amount for the head "+$scope.fees_structure.fees_head[i].head;
                    return false;                                           
                } else if($scope.fees_structure.fees_head[i].amount != Number($scope.fees_structure.fees_head[i].amount)) {
                    $scope.validation_error = "Please enter valid amount for the head "+$scope.fees_structure.fees_head[i].head;
                    return false;                                           
                } else if($scope.fees_structure.fees_head[i].no_installments == '' || $scope.fees_structure.fees_head[i].no_installments == undefined || $scope.fees_structure.fees_head[i].no_installments == 0) {
                    $scope.validation_error = "Please enter no of installments for the head "+$scope.fees_structure.fees_head[i].head;
                    return false;                                           
                } else if($scope.fees_structure.fees_head[i].no_installments != Number($scope.fees_structure.fees_head[i].no_installments)) {
                    $scope.validation_error = "Please enter valid no of installments for the head "+$scope.fees_structure.fees_head[i].head;
                    return false;                                           
                } else if($scope.fees_structure.fees_head[i].no_installments != $scope.fees_structure.fees_head[i].installments.length) {
                    $scope.validation_error = "Please check the no.installments for the head "+$scope.fees_structure.fees_head[i].head;
                    return false;                                           
                } else if($scope.fees_structure.fees_head[i].no_installments > 0) {
                    for (var j=0; j<$scope.fees_structure.fees_head[i].no_installments; j++) {
                        console.log($scope.fees_structure.fees_head[i].installments[j].fine_amount);
                        if ($scope.fees_structure.fees_head[i].installments[j].due_date == '' || $scope.fees_structure.fees_head[i].installments[j].due_date == undefined) {
                            $scope.validation_error = 'Please enter Due Date for the head '+$scope.fees_structure.fees_head[i].head+' installment in the row '+(j + 1);
                            $scope.fees_structure.fees_head[i].shrink = false;
                            return false;
                        } else if ($scope.fees_structure.fees_head[i].installments[j].amount == '' || $scope.fees_structure.fees_head[i].installments[j].amount == undefined || $scope.fees_structure.fees_head[i].installments[j].amount == 0) {
                            $scope.validation_error = 'Please enter installment amount for the head '+$scope.fees_structure.fees_head[i].head+ ' installment in the row '+(j + 1);
                            $scope.fees_structure.fees_head[i].shrink = false;
                            return false;
                        } else if ($scope.fees_structure.fees_head[i].installments[j].amount != Number($scope.fees_structure.fees_head[i].installments[j].amount)) {
                            $scope.validation_error = 'Please enter valid installment amount for the head '+$scope.fees_structure.fees_head[i].head+ ' installment in the row '+(j + 1);
                            $scope.fees_structure.fees_head[i].shrink = false;
                            return false;
                        } else if (parseFloat($scope.fees_structure.fees_head[i].installments[j].fine_amount) != Number($scope.fees_structure.fees_head[i].installments[j].fine_amount)) {
                            $scope.validation_error = 'Please enter valid fine amount for the head '+$scope.fees_structure.fees_head[i].head+' installment in the row '+(j + 1);
                            $scope.fees_structure.fees_head[i].shrink = false;
                            return false;
                        }
                    }
                    if ($scope.fees_structure.fees_head[i].amount != total_installment_amount) { 
                        $scope.validation_error = 'Please check the Amount and Total of Installments amount for the head in the row '+(i + 1);
                        return false;
                    } 
                }
            }
        }
        return true;
    }
    $scope.add_new_head = function() {
        $scope.fees_structure.fees_head.push({
            'head': '',
            'amount': 0,
            'no_installments': 0,
            'installments': [],
            'shrink':true,
        })
    }
    $scope.add_fee_structure_installments = function(fee_head){
        var installments = fee_head.no_installments;
        var fee_head_id = $scope.fees_structure.fees_head.indexOf(fee_head);
        var diff = installments - fee_head.installments.length;
        if (diff > 0) {
            for (i=0; i <diff; i++){
                id_name = 'due_date' + fee_head_id + fee_head.installments.length;
                fee_head.installments.push({
                    'due_date_id': id_name ,
                    'amount': 0,
                    'fine_amount': '',
                    'due_date': '',
                });
                id_name = '';
            }
        } else {
            var diff = fee_head.installments.length - installments ;
            for (i=diff; i >0; i--){
                last_index = fee_head.installments.indexOf(fee_head.installments[fee_head.installments.length - 1]);
                fee_head.installments.splice(last_index, 1);
            }
        }
    }
    $scope.remove_head = function(fee_head) {
        var fee_head_id = $scope.fees_structure.fees_head.indexOf(fee_head);
        fee_head.shrink = 'false';
        $scope.fees_structure.removed_heads.push(fee_head);
        $scope.fees_structure.fees_head.splice(fee_head_id, 1);
    }
    $scope.remove_installment = function(installment, fee_head) {
        var installment_id = fee_head.installments.indexOf(installment);
        fee_head.removed_installments.push(installment);
        fee_head.installments.splice(installment_id, 1);
    }
    $scope.show_installment_details = function(fee_head){
        if (fee_head.shrink) {
            fee_head.shrink = false;
        } else {
            fee_head.shrink = true;
        }
    }
    $scope.attach_date_picker = function(installment) {
        var id_name = '#';
        id_name = id_name + installment.due_date_id;
        new Picker.Date($$(id_name), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.save_edit_fee_structure = function() {
        for (var i=0; i< $scope.fees_structure.fees_head.length; i++) {
            console.log($scope.fees_structure.fees_head[i].installments.length);
            if ($scope.fees_structure.fees_head[i].installments.length > 0) {
                for (var j=0; j< $scope.fees_structure.fees_head[i].installments.length; j++) {
                    id_name = '#' + $scope.fees_structure.fees_head[i].installments[j].due_date_id;
                    $scope.fees_structure.fees_head[i].installments[j].due_date = $$(id_name)[0].get('value');
                }
            }
        }
        if ($scope.edit_fee_structure_validation()) {
            for (var i=0; i<$scope.fees_structure.fees_head.length; i++) {
                if ($scope.fees_structure.fees_head[i].shrink == true) {
                    $scope.fees_structure.fees_head[i].shrink = 'true';
                } else {
                    $scope.fees_structure.fees_head[i].shrink = 'false';
                }
            }
            var height = $(document).height();
            height = height + 'px';
            $('#overlay').css('height', height);
            $('#spinner').css('height', height);
            $scope.validation_error = '';
            params = {
                'fee_structure_id': $scope.fees_structure_id,
                'fee_structure': angular.toJson($scope.fees_structure),
                'csrfmiddlewaretoken': $scope.csrf_token,
            }
            show_spinner();
            url = '/fees/edit_fees_structure_details/' + $scope.fees_structure_id+'/';
            $http({
                method : 'post',
                url : url,
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                hide_spinner();
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
               document.location.href = '/fees/fees_structures/'
            }).error(function(data, status){
                $('#overlay').css('height', '0px');
                $('#spinner').css('height', '0px');
                console.log('error - ', data);
            });
        }
    }
}

function FeesStructureController($scope, $http, $element) {

    var total_installment_amount;
    $scope.fee_structure = {
        'course': '',
        'batch': '',
        'fees_head_details': [],
    }
    $scope.fees_head_details = [];
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        get_course_list($scope, $http);
        $scope.visible_list = [];
    }
    $scope.get_fees_structure = function(){
        $scope.url = '/fees/fees_structures/?course='+$scope.course+"&batch="+$scope.batch;
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.fees_structures = data.fees_structures;
            paginate($scope.fees_structures, $scope);
            if($scope.fees_structures.length == 0){
                $scope.message = "No Fees Structure Created Yet."
            } else {
                $scope.message = '';
            }
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
    $scope.select_page = function(page){
        select_page(page, $scope.fees_structures, $scope);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.add_fee_structure_installments = function(fee_head){
        var installments = fee_head.no_installment;
        var fee_head_id = $scope.fees_head_details.indexOf(fee_head);
        var diff = installments - fee_head.installments.length;
        if (diff > 0) {
            for (i=0; i <diff; i++){
                id_name = 'due_date' + fee_head_id + i;
                fee_head.installments.push({
                    'due_date_id': id_name ,
                    'amount': 0,
                    'fine_amount': '',
                    'due_date': '',
                });
                id_name = '';
            }
        } else {
            var diff = fee_head.installments.length - installments ;
            for (i=diff; i >0; i--){
                last_index = fee_head.installments.indexOf(fee_head.installments[fee_head.installments.length - 1]);
                fee_head.installments.splice(last_index, 1);
            }
        }
    }
    $scope.attach_date_picker = function(installment) {
        var id_name = '#';
        id_name = id_name + installment.due_date_id;
        new Picker.Date($$(id_name), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
    }
    $scope.remove_head = function(fee_head) {
        var fee_head_id = $scope.fees_head_details.indexOf(fee_head);
        $scope.fees_head_details.splice(fee_head_id, 1);
    }
    $scope.remove_installment = function(installment, fee_head) {
        var installment_id = fee_head.installments.indexOf(installment);
        fee_head.installments.splice(installment_id, 1);
    }
    $scope.get_batch = function(){
        get_course_batch_list($scope, $http);
    }
    $scope.add_new_head = function() {
        $scope.fees_head_details.push({
            'head': '',
            'amount': 0,
            'no_installment': 0,
            'installments': [],
            'shrink':true,
        })
    }
    $scope.show_installment_details = function(fee_head){
        if (fee_head.shrink) {
            fee_head.shrink = false;
        } else {
            fee_head.shrink = true;
        }
    }
    $scope.validate_new_fees_structure = function() {
        if($scope.fee_structure.course == '' || $scope.fee_structure.course == undefined) {
            $scope.validation_error = "Please Select the course" ;
            return false;
        } else if($scope.fee_structure.batch == '' || $scope.fee_structure.batch == undefined) {
            $scope.validation_error = "Please Select batch";
            return false;                                           
        } else if ($scope.fees_head_details.length == 0) {
            $scope.validation_error = 'Please add fees details';
            return false;
        } else if ($scope.fees_head_details.length > 0) {
            for (var i=0; i<$scope.fees_head_details.length; i++) {
                total_installment_amount = 0;
                if ($scope.fees_head_details[i].installments.length > 0) {
                    for (var j=0; j<$scope.fees_head_details[i].no_installment; j++) {
                        if ($scope.fees_head_details[i].installments[j].amount == Number($scope.fees_head_details[i].installments[j].amount))
                            total_installment_amount = parseFloat(total_installment_amount) + parseFloat($scope.fees_head_details[i].installments[j].amount);
                    }
                }
                if($scope.fees_head_details[i].head == '' || $scope.fees_head_details[i].head == undefined) {
                    $scope.validation_error = "Please enter head in the row "+(i + 1);
                    return false;                                           
                } else if($scope.fees_head_details[i].amount == '' || $scope.fees_head_details[i].amount == undefined || $scope.fees_head_details[i].amount == 0) {
                    $scope.validation_error = "Please enter amount for the head "+$scope.fees_head_details[i].head;
                    return false;                                           
                } else if($scope.fees_head_details[i].amount != Number($scope.fees_head_details[i].amount)) {
                    $scope.validation_error = "Please enter valid amount for the head "+$scope.fees_head_details[i].head;
                    return false;                                           
                } else if($scope.fees_head_details[i].no_installment == '' || $scope.fees_head_details[i].no_installment == undefined  || $scope.fees_head_details[i].no_installment == 0) {
                    $scope.validation_error = "Please enter no of installments for the head "+$scope.fees_head_details[i].head;
                    return false;                                           
                } else if($scope.fees_head_details[i].no_installment != Number($scope.fees_head_details[i].no_installment)) {
                    $scope.validation_error = "Please enter valid no of installments for the head "+$scope.fees_head_details[i].head;
                    return false;                                           
                }  else if($scope.fees_head_details[i].no_installment != $scope.fees_head_details[i].installments.length) {
                    $scope.validation_error = "Please enter valid no of installments for the head "+$scope.fees_head_details[i].head;
                    return false;                                           
                } else if($scope.fees_head_details[i].no_installment > 0) {
                    for (var j=0; j<$scope.fees_head_details[i].no_installment; j++) {
                        if ($scope.fees_head_details[i].installments[j].due_date == '' || $scope.fees_head_details[i].installments[j].due_date == undefined) {
                            $scope.validation_error = 'Please enter Due Date for the head '+$scope.fees_head_details[i].head+' ,installment in the row '+(j + 1);
                            $scope.fees_head_details[i].shrink = false;
                            return false;
                        } else if ($scope.fees_head_details[i].installments[j].amount == '' || $scope.fees_head_details[i].installments[j].amount == undefined || $scope.fees_head_details[i].installments[j].amount == 0) {
                            $scope.validation_error = 'Please enter installment amount for the head '+$scope.fees_head_details[i].head+ ' ,installment in the row '+(j + 1);
                            $scope.fees_head_details[i].shrink = false;
                            return false;
                        } else if ($scope.fees_head_details[i].installments[j].amount != Number($scope.fees_head_details[i].installments[j].amount)) {
                            $scope.validation_error = 'Please enter valid installment amount for the head '+$scope.fees_head_details[i].head+ ' ,installment in the row '+(j + 1);
                            $scope.fees_head_details[i].shrink = false;
                            return false;
                        } else if ($scope.fees_head_details[i].installments[j].fine_amount == '' || $scope.fees_head_details[i].installments[j].fine_amount == undefined) {
                            $scope.validation_error = 'Please enter fine amount for the head '+$scope.fees_head_details[i].head+' ,installment in the row '+(j + 1);
                            $scope.fees_head_details[i].shrink = false;
                            return false;
                        } else if ($scope.fees_head_details[i].installments[j].fine_amount != Number($scope.fees_head_details[i].installments[j].fine_amount)) {
                            $scope.validation_error = 'Please enter valid fine amount for the head '+$scope.fees_head_details[i].head+' ,installment in the row '+(j + 1);
                            $scope.fees_head_details[i].shrink = false;
                            return false;
                        }
                    }
                    if ($scope.fees_head_details[i].amount != total_installment_amount) { 
                        $scope.validation_error = 'Please check the Amount and Total of Installments amount for the head '+$scope.fees_head_details[i].head;
                        return false;
                    } 
                }
            }
        }
        return true;
     }

    $scope.create_fees_structure = function() {
        
        for (var i=0; i<$scope.fees_head_details.length; i++) {
            if ($scope.fees_head_details[i].installments.length > 0) {
                for (var j=0; j<$scope.fees_head_details[i].no_installment; j++) {
                    id_name = '#' + $scope.fees_head_details[i].installments[j].due_date_id;
                    $scope.fees_head_details[i].installments[j].due_date = $$(id_name)[0].get('value');
                }
            }
        }
        $scope.fee_structure.course = $scope.course
        
        if($scope.validate_new_fees_structure()) {
            for (var i=0; i<$scope.fees_head_details.length; i++) {
                if ($scope.fees_head_details[i].shrink == true) {
                    $scope.fees_head_details[i].shrink = 'true';
                } else {
                    $scope.fees_head_details[i].shrink = 'false';
                }
            }
            $scope.fee_structure.fees_head_details = $scope.fees_head_details;
            params = { 
                'fee_structure': angular.toJson($scope.fee_structure),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/fees/new_fees_structure/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {   
                hide_spinner();
                if (data.result == 'error'){
                    $scope.validation_error = data.message;
                } else {
                    document.location.href ='/fees/fees_structures/';
                }
            }).error(function(data, success){
                
            });
        }          
    }
    $scope.display_fees_structure_details = function(fees_structure) {  
        $scope.fees_structure_id = fees_structure.id;
        $scope.url = '/fees/edit_fees_structure_details/' + $scope.fees_structure_id+ '/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.fees_structure = data.fees_structure[0];
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });

        $scope.hide_popup_windows();
        $('#fees_structure_details_view')[0].setStyle('display', 'block');
        
        $scope.popup = new DialogueModelWindow({                
            'dialogue_popup_width': '90%',
            'message_padding': '0px',
            'left': '28%',
            'top': '182px',
            'height': 'auto',
            'content_div': '#fees_structure_details_view'
        });
        
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
    }
    $scope.hide_popup_windows = function(){
        $('#fees_structure_details_view')[0].setStyle('display', 'none');
    }
    $scope.check_fees_structure_exists = function() {
        console.log($scope.course, $scope.fee_structure.batch);
        if ($scope.course != null && $scope.fee_structure.batch != null) {
            $http.get('/fees/is_fees_structure_exists/'+$scope.course+'/'+$scope.fee_structure.batch+'/').success(function(data){
                if (data.result == 'error') {
                    $scope.fees_structure_exists = true;
                    $scope.validation_error = data.message;
                } else {
                    $scope.fees_structure_exists = false;     
                    $scope.validation_error = '';   
                }           
            }).error(function(data, status){
                console.log('Request failed' || data);
            });
        }
    }
}
function EditFeesHeadController($scope, $http, $element) {

    $scope.init = function(csrf_token, fees_head_id) {
        get_fees_head_details($scope, $http, fees_head_id);
        $scope.csrf_token = csrf_token;
        $scope.fees_head_id = fees_head_id;
    }
    $scope.validate_fees_head = function() {
        
        $scope.validation_error = '';
        if($scope.fee_head.head == '' || $scope.fee_head.head == undefined) {
            $scope.validation_error = 'Please enter the Head Name';
            return false;
        } else if ($scope.fee_head.amount == '' || $scope.fee_head.amount == 0 || $scope.fee_head.amount == undefined) {
            $scope.validation_error = 'Please enter the Amount';
            return false;
        } else if ($scope.fee_head.amount != Number($scope.fee_head.amount)) {
            $scope.validation_error = 'Please enter valid Amount';
            return false;
        } return true;
     }
    $scope.save_fees_head = function() {
        if($scope.validate_fees_head()) {       
            console.log($scope.fee_head);  
            params = { 
                'fee_head_details': angular.toJson($scope.fee_head),
                'fees_head_id': $scope.fees_head_id,
                "csrfmiddlewaretoken" : $scope.csrf_token
            }     
            show_spinner();   
            $http({
                method: 'post',
                url: "/fees/add_fees_head/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                hide_spinner();
                if (data.result == 'error'){
                    $scope.validation_error = data.message;
                } else {                    
                    document.location.href ='/fees/fees_heads/';
                }
            }).error(function(data, success){
                
            });
        }
    }
}

function FeesHeadController($scope, $http, $element) {
    var total_installment_amount;
    $scope.fee_head = {
        'head': '',
        'amount': 0,
    }
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
        $scope.get_fees_heads()
    }
    $scope.select_page = function(page){
        select_page(page, $scope.fees_heads, $scope, 2);
    }
    $scope.range = function(n) {
        return new Array(n);
    }
    $scope.validate_fees_head = function() {
        $scope.validation_error = '';
        if($scope.fee_head.head == '' || $scope.fee_head.head == undefined) {
            $scope.validation_error = 'Please enter the Head Name';
            return false;
        } else if ($scope.fee_head.amount == '' || $scope.fee_head.amount == 0 || $scope.fee_head.amount == undefined) {
            $scope.validation_error = 'Please enter the Amount';
            return false;
        } else if ($scope.fee_head.amount != Number($scope.fee_head.amount)) {
            $scope.validation_error = 'Please enter valid Amount';
            return false;
        } return true;
     }
    $scope.save_fees_head = function() {
        if($scope.validate_fees_head()) {         
            params = { 
                'fee_head_details': angular.toJson($scope.fee_head),
                "csrfmiddlewaretoken" : $scope.csrf_token
            }     
            show_spinner();   
            $http({
                method: 'post',
                url: "/fees/add_fees_head/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                hide_spinner();
                if (data.result == 'error'){
                    $scope.validation_error = data.message;
                } else {                    
                    document.location.href ='/fees/fees_heads/';
                }
            }).error(function(data, success){
                
            });
        }
    }
    $scope.get_fees_heads = function(){
        $scope.url = '/fees/fees_heads/';
        show_spinner();
        $http.get($scope.url).success(function(data)
        {
            hide_spinner();
            $scope.fees_heads = data.fees_heads;
            paginate($scope.fees_heads, $scope, 2);
        }).error(function(data, status)
        {
            console.log(data || "Request failed");
        });
    }
}

function CommonFeesPayment($scope, $http, $element) {
    $scope.init = function(csrf_token) {
        $scope.csrf_token = csrf_token;
    }
    $scope.fees_payment = {
        'student_id': '',
        'head_id': '',
        'paid_date': '',
        'total_amount': '',
        'paid_amount': '',
        'balance': '',
    }
    $scope.course = 'select';
    $scope.batch = 'select';
    $scope.fees_payment.student = 'select';
    $scope.head = '';
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        var paid_date = new Picker.Date($$('#paid_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_course_list($scope, $http);
    }
    $scope.get_batch = function(){
        get_course_batch_list($scope, $http);
    }
    $scope.get_student = function(){
        get_course_batch_student_list($scope, $http);
    }
    $scope.get_fees_head = function(){
        $scope.url = '/fees/get_common_fees_head/'+ $scope.course+ '/'+ $scope.batch+ '/'+$scope.fees_payment.student+'/';
        if ($scope.course !='select' && $scope.batch != 'select' && $scope.fees_payment.student != 'select')
        show_spinner();       
            $http.get($scope.url).success(function(data)
            {
                hide_spinner();
                $scope.heads = data.heads;
                $scope.fees_payment.amount = '';
                $('#balance').val(0);
                $('#total_fee_amount').val(0);
                if ($scope.heads.length == 0) {
                    $scope.no_head_error = 'Payment completed';
                } else {
                    $scope.no_head_error = '';
                }
            }).error(function(data, status)
            {
                console.log(data || "Request failed");
            });
    }
    $scope.get_head_details = function() {
        $scope.fees_payment.amount = $scope.head.amount;
        $scope.fees_payment.paid_head_amount = $scope.head.paid_head_amount;
        $scope.fees_payment.balance = $scope.head.balance;
    }
    $scope.validate_fees_payment = function() {
        $scope.validation_error = '';
        if($scope.course == 'select') {
            $scope.validation_error = "Please Select a course " ;
            return false
        } else if($scope.batch == 'select') {
            $scope.validation_error = "Please Select a batch " ;
            return false;
        } else if($scope.fees_payment.student == 'select') {
            $scope.validation_error = "Please select a student" ;
            return false;
        } else if($scope.head == '' || $scope.head == undefined) {
            $scope.validation_error = "Please select a head name" ;
            return false;
        } else if ($scope.fees_payment.paid_amount == '' || $scope.fees_payment.paid_amount == undefined) {
            $scope.validation_error = "Please enter paid amount" ;
            return false;
        } else if ($scope.fees_payment.paid_amount != Number($scope.fees_payment.paid_amount)) {
            $scope.validation_error = "Please enter valid paid amount" ;
            return false;
        } else if ($scope.fees_payment.paid_amount != $scope.fees_payment.balance) {
            $scope.validation_error = "Please check the balance amount with paid amount" ;
            return false;
        } return true; 
    }
    $scope.save_fees_payment = function() {

        $scope.fees_payment.course_id = $scope.course;
        $scope.fees_payment.batch_id = $scope.batch;
        $scope.fees_payment.head_id = $scope.head.id;
        $scope.fees_payment.paid_date = $$('#paid_date')[0].get('value');
        if($scope.validate_fees_payment()) {
            params = { 
                'fees_payment': angular.toJson($scope.fees_payment),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            show_spinner();
            $http({
                method: 'post',
                url: "/fees/common_fees_payment/",
                data: $.param(params),
                headers: {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                hide_spinner();
                if (data.result == 'error'){
                    $scope.validation_error = data.message;
                } else {              
                    document.location.href ="/fees/common_fees_payment/";
                }
            }).error(function(data, success){
                $scope.error_flag=true;
                $scope.message = data.message;
            });
        }
    }
}

function FeesReportController($scope, $http, $element) {
    
    $scope.student_id = 'select';
    $scope.course = 'select';
    $scope.batch = 'select';
    $scope.fees_type = '';
    $scope.filtering_option = '';
    $scope.url = '';
    $scope.init = function(csrf_token)
    {
        $scope.csrf_token = csrf_token;
        $scope.error_flag = false;
        get_course_list($scope, $http);
    }
    $scope.get_batch = function(){
        $scope.filtering_option = '';
        get_course_batch_list($scope, $http);
    }
    $scope.get_student = function(){
        $scope.filtering_option = '';
        get_course_batch_student_list($scope, $http);
    }
    $scope.view_report = function(){
        if ($scope.course == 'select' || $scope.course == '' || $scope.course == null) {
            $scope.validation_error = 'Please choose course';
        } else if ($scope.batch == 'select' || $scope.batch == '' || $scope.batch == null) {
            $scope.validation_error = 'Please choose batch';
        } else if ($scope.fees_type == '' || $scope.fees_type == undefined) {
            $scope.validation_error = 'Please choose fees type';
        } else if ($scope.filtering_option == '' || $scope.filtering_option == undefined) {
            $scope.validation_error = 'Please choose report type';
        } else if ($scope.filtering_option == 'student_wise' && ($scope.student_id == 'select')) {
            $scope.validation_error = 'Please choose student';
        } else {
            document.location.href = '/report/outstanding_fees_report/?course='+$scope.course+'&batch='+$scope.batch+'&student='+$scope.student_id+'&filtering_option='+$scope.filtering_option+'&fees_type='+$scope.fees_type+'&report_type=outstanding_fees';
        }
    }
}