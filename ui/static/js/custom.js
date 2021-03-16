(function($) {
    "use strict"; // Start of use strict

    function matchStart(params, data) {
        params.term = params.term || '';
        if(params.term == ''){
            return data;    
        } 

        if (data.text.toUpperCase().indexOf(params.term.toUpperCase()) == 0) {
            return data;
        }
        return false;
    }

    $('.select-2').select2();

    $(".select-2-matchstart").select2({
        matcher: function(params, data) {
            return matchStart(params, data);
        },
    });
    //============================================================
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

    //=========================================================
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

    //=============================================================
    var review_table = $('#review_table').DataTable({        
        "fnDrawCallback": function () {
            if(this.DataTable().data().length>0){
                $('#review_table>tbody>tr>td:nth-child(6)').editable({
                    url: '/update_attr_rev',
                    type: 'text', 
                    mode: 'inline',
                    showbuttons: false,
                    pk: function(e){
                        return $(this.parentElement).find("td:nth-child(1)").text()
                    },
                    success: function(response, newValue) {                        
                        if(response=="error") {
                            alert("update is failed")
                        }
                    }        
                });    
            }            
        }   
    });


    /*
    var review_csv = document.getElementById('review_csv');

    review_csv.onchange = function(e) {
      var ext = this.value.match(/\.([^\.]+)$/)[1];
      switch (ext) {
        case 'csv':          
          break;
        default:
          alert('Other files are Not allowed, Please select only csv file.');
          this.value = '';
      }
    };
    */

})(jQuery); // End of use strict