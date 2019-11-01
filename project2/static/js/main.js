$(document).ready(function () {
    /* alert-dismissable dismiss automatically in 3s */
    window.setTimeout(function() {
        $(".alert-dismissable").fadeTo(1000, 0).slideUp(1000, function(){
            $(this).remove(); 
        });
    }, 3000);  
});
