$(document).ready(function(){

    
    $("#jsend").mouseenter(function(){
        $(this).hide();
        $("#jsin").fadeIn("slow");
    });
    
    $('#jsin').mouseleave(function(){
        $(this).hide();
        $('#jsend').fadeIn("slow");
    });
    


});




