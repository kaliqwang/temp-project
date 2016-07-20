$(document).ready(function() {

    $('[data-toggle="tooltip"]').tooltip();

    $('#submit-login-form').click(function(e){
        e.preventDefault();
        $("#login-form").submit();
    });

    $('#submit-announcement-create-form').click(function(e){
        e.preventDefault();
        var error = false;
        var $inputs = $('input.form-control, textarea.form-control');
        if(!$('#announcement-create-form')[0].checkValidity()) {
            $inputs.each(function() {
                if ($(this).val().length == 0) {
                    $(this).parent().addClass('has-error');
                    $(this).siblings().children().css('border-color', '#a94442');
                    error = true;
                } else {
                    $(this).parent().removeClass('has-error');
                    $(this).siblings().children().css('border-color', '#ccc');
                }
            });
        }
        if (!error) {
            $('#announcement-create-form').submit();
        }
    });

    $('#submit-event-create-form').click(function(e){
        e.preventDefault();
        $('#event-create-form').submit()
    });

    $('#submit-poll-create-form').click(function(e){
        e.preventDefault();
        $('#poll-create-form').submit()
    });

});
