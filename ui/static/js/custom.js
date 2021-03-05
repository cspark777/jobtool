(function($) {
    "use strict"; // Start of use strict

    $('.select-2').select2();
    
    var job_table = $('#job_table').DataTable({        
        "order": [[ 0, "desc" ]]
    });

    $("#web_class").on("change", function(e){
        var selected_webclass = $(this).val();
        $.ajax({
                method: "GET",
                url: "/get_attrs",
                data:{"web_class": selected_webclass}
        })
        .done(function(msg) {      
            var msg_obj = JSON.parse(msg);
            $('#attr').empty();

            for(var i=0; i<msg_obj.length; i++){
                $('#attr').append("<option value='" + msg_obj[i]["attr_name"] + "'>" + msg_obj[i]["attr_name"] + "</option>");
            }
            //Metronic.unblockUI();
        })
        .fail(function(msg){
            console.log(msg);   
            //Metronic.unblockUI();       
        });
    });


    var result_table = $('#result_table').DataTable({        
        "order": [[ 7, "desc" ]]
    });

    $("#result_web_class").on("change", function(e){
        var selected_webclass = $(this).val();
        $.ajax({
                method: "GET",
                url: "/get_result_attrs",
                data:{"web_class": selected_webclass}
        })
        .done(function(msg) {      
            var msg_obj = JSON.parse(msg);
            $('#result_attr').empty();

            for(var i=0; i<msg_obj.length; i++){
                $('#result_attr').append("<option value='" + msg_obj[i]["attr_name"] + "'>" + msg_obj[i]["attr_name"] + "</option>");
            }
            //Metronic.unblockUI();
        })
        .fail(function(msg){
            console.log(msg);   
            //Metronic.unblockUI();       
        });
    });


    var review_table = $('#review_table').DataTable({        
        
    });

})(jQuery); // End of use strict