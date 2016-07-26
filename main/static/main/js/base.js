$(document).ready(function() {

    /********************** CSRF Protection Boilerplate ***********************/

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /****************************** On Page Load ******************************/

    // Activate tooltips
    $('[data-toggle="tooltip"]').tooltip({
        animation: false,
    });

    /***************************** Event Handlers *****************************/

    // Announcement Create
    $('#submit-announcement-create-form').click(function(e){e.preventDefault();
        var error = false;
        $('.validate-required > input,textarea').each(function() {
            if ($(this).val().trim() == '') {
                error = true;
                $(this).parent().addClass('has-error');
            } else {
                $(this).parent().removeClass('has-error');
            }
        });
        if (!error) {
            $('#image-links-add').remove();
            $('#youtube-videos-add').remove();
            $('#announcement-create-form').submit();
        }
    });

    // Announcement Update
    $('#submit-announcement-update-form').click(function(e){e.preventDefault();
        var error = false;
        $('.validate-required > input,textarea').each(function() {
            if ($(this).val().trim() == '') {
                error = true;
                $(this).parent().addClass('has-error');
            } else {
                $(this).parent().removeClass('has-error');
            }
        });
        console.log('Error: ' + error);
        if (!error) {
            $('#image-links-add').remove();
            $('#youtube-videos-add').remove();
            $('#youtube-videos-existing').remove();
            $('#announcement-update-form').submit();
        }
    });

    // Event Create
    $('#submit-event-create-form').click(function(e){e.preventDefault();
        $('#event-create-form').submit()
    });

    // Event Update
    $('#submit-event-update-form').click(function(e){e.preventDefault();
        $('#event-update-form').submit()
    });

    // Authentication
    $('#submit-login-form').click(function(e){e.preventDefault();
        $("#login-form").submit();
    });

    // Student Registration
    $("#submit-student-register-form").click(function(e){e.preventDefault();
        $("#student-register-form").submit();
    });

    /**************************** To Test / Debug *****************************/

    $("#submit-poll-create-form").click(function(e){
        e.preventDefault();
        var error = false;
        if(!$("#poll-create-form")[0].checkValidity()) {
            $content = $('#poll-content > input');
            if ($content.val().trim() == ''){
                $content.parent().addClass('has-error');
                error = true;
            } else {
                $content.parent().removeClass('has-error');
            }
            $(".choice-input").each(function() {
                if($(this).val().trim() == ''){
                    $(this).parent().addClass('has-error');
                    error = true;
                } else {
                    $(this).parent().removeClass('has-error');
                }
            });
        } else {
            var uniqueValues = [];
            $(".choice-input").each(function() {
                if (uniqueValues.indexOf($(this).val().trim()) != -1) {
                    $(this).parent().addClass('has-error');
                    error = true;
                } else {
                    $(this).parent().removeClass('has-error');
                    uniqueValues.push($(this).val().trim());
                }
            });
        }
        if(!error){
            $("#poll-create-form").submit();
        }
    });

    // $("#submit-poll-update-form").click(function(e){
    //     e.preventDefault();
    //     var error = false;
    //     if(!$("#poll-update-form")[0].checkValidity()) {
    //         $content = $('#poll-content > input');
    //         if ($content.val().trim() == ''){
    //             $content.parent().addClass('has-error');
    //             error = true;
    //         } else {
    //             $content.parent().removeClass('has-error');
    //         }
    //         $(".choice-input").each(function() {
    //             if($(this).val().trim() == ''){
    //                 $(this).parent().addClass('has-error');
    //                 error = true;
    //             } else {
    //                 $(this).parent().removeClass('has-error');
    //             }
    //         });
    //     } else {
    //         var uniqueValues = [];
    //         $(".choice-input").each(function() {
    //             if (uniqueValues.indexOf($(this).val().trim()) != -1) {
    //                 $(this).parent().addClass('has-error');
    //                 error = true;
    //             } else {
    //                 $(this).parent().removeClass('has-error');
    //                 uniqueValues.push($(this).val().trim());
    //             }
    //         });
    //     }
    //     if(!error){
    //         $("#poll-update-form").submit();
    //     }
    // });

    $("#submit-category-list-form").click(function(e){
        e.preventDefault();
        var error = false;
        if(!$("#category-list-form")[0].checkValidity()) {
            $(".category-name-input").each(function() {
                if($(this).val().trim() == ''){
                    $(this).parent().addClass('has-error');
                    error = true;
                } else {
                    $(this).parent().removeClass('has-error');
                }
            });
        } else {
            var uniqueValues = [];
            $(".category-name-input").each(function() {
                if (uniqueValues.indexOf($(this).val().trim()) != -1) {
                    $(this).parent().addClass('has-error');
                    error = true;
                } else {
                    $(this).parent().removeClass('has-error');
                    uniqueValues.push($(this).val().trim());
                }
            });
        }
        if(!error){
            $("#category-list-form").submit();
        }
    });

});
