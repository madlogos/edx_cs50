$(document).ready(function () {
    /* alert-dismissable dismiss automatically in 4s */
    window.setTimeout(function() {
        $(".alert-dismissable").fadeTo(1000, 0).slideUp(1000, function(){
            $(this).remove(); 
        });
    }, 4000);  
});

$(document).ready(function(){
    $("#rating").rating();           
});
 