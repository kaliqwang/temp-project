
$(document).ready(function() {
    var mediaArray = [];
    // using jQuery
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

    $('#poll-list').on('click', '.remove-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');

        $.ajax({
            type: 'DELETE',
            url: '/api/polls/' + $poll.attr('id'),
            success: function() {
                $poll.remove();
            }
        });
    });
    //set data-status of all mmedia to 0 meaning they can be selected
    $('#poll-list').on('click', '.edit-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        $poll.addClass("edit");

    });
    //set data-status of all mmedia to 3 meaning they can no longer be selected
    $('#poll-list').on('click', '.cancel-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        $poll.removeClass("edit");
    });

    //Put media into array when x button is clicked. If save-poll pressed, for each object in array, call ajax function.

    /*$('#poll-list').on('click', '.remove-media', function(e) {
        e.preventDefault();
        var $media = $(this).closest('.mmedia');
        mediaArray.push($media);
        //mediaArray.push($media.attr('data-id') + '/' + $media.attr('id'));
        $media.fadeOut();

    });*/

    //error when category is null
    $('#poll-list').on('click', '.save-poll', function(e) {
        e.preventDefault();

        var $poll = $(this).closest('.poll-wrapper');
        var poll = {
            author: $poll.find('.author').text(),
            category: $poll.find('.category').text(),
            date_created: $poll.find('.date_created').text(),
            content: $poll.find('.content > input').val(),
            rank: $poll.find('.rank').text(),
            is_open: $poll.find('.is_open').text(),
        };
        $.ajax({
            type: 'PUT',
            url: '/api/polls/' + $poll.attr('id'),
            data: poll,
            success: function(newpoll) {
                $poll.find('.content.noedit > a > h2').text(newpoll.content);
                $poll.removeClass('edit');
            },
            error: function() {
                alert('Error updating poll.');
            }
        });
    });
});
