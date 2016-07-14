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

    $('#announcement-list').on('click', '.remove-announcement', function(e) {
        e.preventDefault();
        var $announcement = $(this).closest('.announcement-wrapper');

        $.ajax({
            type: 'DELETE',
            url: '/api/announcements/' + $announcement.attr('id'),
            success: function() {
                $announcement.remove();
            }
        });
    });
    //set data-status of all mmedia to 0 meaning they can be selected
    $('#announcement-list').on('click', '.edit-announcement', function(e) {
        e.preventDefault();
        var $announcement = $(this).closest('.announcement-wrapper');
        var $images = $announcement.find('.images');
        $announcement.addClass("edit");
        $images.children().attr('data-status', 0);
    });
    //set data-status of all mmedia to 3 meaning they can no longer be selected
    $('#announcement-list').on('click', '.cancel-announcement', function(e) {
        e.preventDefault();
        var $announcement = $(this).closest('.announcement-wrapper');
        var $images = $announcement.find('.images');
        $announcement.removeClass("edit");
        $images.children().removeClass('selected');
        $images.children().attr('data-status', 3);
        mediaArray = [];
    });

    //Put media into array when x button is clicked. If save-announcement pressed, for each object in array, call ajax function.

    /*$('#announcement-list').on('click', '.remove-media', function(e) {
        e.preventDefault();
        var $media = $(this).closest('.mmedia');
        mediaArray.push($media);
        //mediaArray.push($media.attr('data-id') + '/' + $media.attr('id'));
        $media.fadeOut();

    });*/

    //error when category is null
    $('#announcement-list').on('click', '.save-announcement', function(e) {
        e.preventDefault();
        var $announcement = $(this).closest('.announcement-wrapper');

        var announcement = {
            author: $announcement.find('.author').text(),
            title: $announcement.find('.title > input').val(),
            category: $announcement.find('.category').text(),
            date_created: $announcement.find('.date_created').text(),
            content: $announcement.find('.content > textarea').val(),
            rank: $announcement.find('.rank').text(),
            image_files: [],
            image_links: [],
            youtube_videos: [],
        };

        $.ajax({
            type: 'PUT',
            url: '/api/announcements/' + $announcement.attr('id'),
            data: announcement,
            success: function(newAnnouncement) {
                $announcement.find('.title > a > h2').text(newAnnouncement.title);
                $announcement.find('.content.noedit').text(newAnnouncement.content);
                $announcement.removeClass('edit');
            },
            error: function() {
                alert('Error updating announcement.');
            }
        });

        mediaArray.forEach(function(media) {
            $.ajax({
                type: 'DELETE',
                url: '/api/' + media.attr('data-id') + '/' + media.attr('id'),
                success: function() {
                    media.fadeOut();
                },
                error: function() {
                    alert('Error deleting media.');
                }
            });
        });
    });
    $('#announcement-list').on('click', '.mmedia', function(e) {
        e.preventDefault();
        var $message = $(this).find('span.remove');

        if ($(this).attr('data-status') == 0) {
            $(this).attr('data-status', 1);
            $(this).addClass('selected');
            mediaArray.push($(this));
            $message.html('Restore');

        } else if ($(this).attr('data-status') == 1) {
            $(this).removeClass('selected');
            $(this).attr('data-status', 0);
            mediaArray.splice(mediaArray.indexOf($(this), 1));
            $message.html('Remove');

        }
    });
    $('iframe').on('click', function(e) {
        e.preventDefault();
        var $message = $(this).find('span.remove');
        console.log('clicked');
        if ($(this).attr('data-status') == 0) {
            $(this).attr('data-status', 1);
            $(this).addClass('selected');
            mediaArray.push($(this));
            $message.html('Restore');

        } else if ($(this).attr('data-status') == 1) {
            $(this).removeClass('selected');
            $(this).attr('data-status', 0);
            mediaArray.splice(mediaArray.indexOf($(this), 1));
            $message.html('Remove');

        }
    });
});
