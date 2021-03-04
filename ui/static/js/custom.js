(function($) {
    "use strict"; // Start of use strict

    $('.select-2').select2();

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
                $('#attr').append("<option value='" + msg_obj[i]["sku"] + "'>" + msg_obj[i]["attr_name"] + "</option>");
            }
            //Metronic.unblockUI();
        })
        .fail(function(msg){
            console.log(msg);   
            //Metronic.unblockUI();       
        });
    });

})(jQuery); // End of use strict