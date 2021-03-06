$(document).ready(function() {

    /**************************** CSRF Protection *****************************/

    var csrftoken = Cookies.get('csrftoken');
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

    // var $fadeIn = $('#sidebar, #masthead-top-left');
    // $fadeIn.delay('fast').fadeIn('fast');

    // Retrieve sidebar status
    // TODO: do sidebar differently? No margin push? simply .show() .hide() sidebar?

    if (localStorage.sidebarStatus == 0) {
        $('body').removeClass('show-sidebar');
    }

    // Activate sidebar toggle button
    $('#toggle-sidebar').on('click', function(e){e.preventDefault();
        if (localStorage.sidebarStatus == 0) {
            $('body').addClass('show-sidebar');
            localStorage.sidebarStatus = 1;
            if ($(window).width() < 551) {
              $('#overlay-back').show();
            }
        } else {
            $('body').removeClass('show-sidebar');
            localStorage.sidebarStatus = 0;
            $('#overlay-back').hide();
        }
    });
    $('#toggle-right-sidebar').on('click', function(e){e.preventDefault();

      // Have to check if announcement sidebar is open/closed window.width, and overlay state
      if ($(window).width() < 551 && $('#poll-sidebar-container').css('display') == "none" && $('#overlay-back').css('display') == "none") {
        $('#overlay-back').show();
      } else if ($(window).width() < 551 && $('#announcement-sidebar-container').css('display') == "none" && $('#overlay-back').css('display') == "none") {
              $('#overlay-back').show();
      } else {
        $('#overlay-back').hide();
      }


      $('#announcement-sidebar-container').toggle();
      $('#poll-sidebar-container').toggle();
    });

    // Activate tooltips
    $('[data-toggle="tooltip"]').tooltip({
        animation: false,
    });

    // Autoresize Textareas
    autosize($('textarea'));

    // Autofocus on username input
    $('#login-modal').on('shown.bs.modal', function(){
        $('#login-form').find('input[name="username"]').focus();
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
        return false;
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
        return false;
    });

    // Event Create
    $('#submit-event-create-form').click(function(e){e.preventDefault();
        $('#event-create-form').submit();
        return false;
    });

    // Event Update
    $('#submit-event-update-form').click(function(e){e.preventDefault();
        $('#event-update-form').submit();
        return false;
    });

    // Authentication
    $('#submit-login-form').click(function(e){e.preventDefault();
        $("#login-form").submit();
        return false;
    });

    // Student Registration
    $("#submit-student-register-form").click(function(e){e.preventDefault();
        $("#student-register-form").submit();
        return false;
    });

    /**************************** To Test / Debug *****************************/

    // $("#submit-poll-create-form").click(function(e){
    //     e.preventDefault();
    //     var error = false;
    //     if(!$("#poll-create-form")[0].checkValidity()) {
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
    //         $("#poll-create-form").submit();
    //     }
    // });

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
        return false;
    });

    function shadeColor(color, percent) {
        var f=parseInt(color.slice(1),16),t=percent<0?0:255,p=percent<0?percent*-1:percent,R=f>>16,G=f>>8&0x00FF,B=f&0x0000FF;
        return "#"+(0x1000000+(Math.round((t-R)*p)+R)*0x10000+(Math.round((t-G)*p)+G)*0x100+(Math.round((t-B)*p)+B)).toString(16).slice(1);
    }
});
