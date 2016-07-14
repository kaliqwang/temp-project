
$(document).ready(function() {
    //These functions are for Users only
    function checkVoted() {
        $open_polls = $('#poll-list').children('.open');
        $open_polls.each(function() {
            $poll = $(this);
            $.ajax({
                type: 'GET',
                url: '/votes/' + ($poll).attr('id'),
                async: false,
                success: function(data) {
                    ($poll).find('.resubmit-poll').removeClass('hide');

                },
                error: function() {
                    ($poll).find('.submit-poll').removeClass('hide');
                }
            });
        });
    }
    checkVoted();
    $('#poll-list').on('click', '.submit-poll', function(e) {
        e.preventDefault();

        var $poll = $(this).closest('.poll-wrapper');
        var $poll_content = $poll.find('.content > input').val();
        var $choice = $poll.find("input[name=" + $poll.attr('id') + "]:checked");

        var vote = {
            voter: $poll.parent().attr('data-user'),
            choice: $choice.attr('data-choice'),
            poll: $poll.attr('id'),
        }
        $.ajax({
            type: 'POST',
            url: '/api/votes/',
            data: vote,
            success: function() {
                alert("vote successfully submitted!");
                ($poll).find('.submit-poll').addClass('hide');
                ($poll).find('.resubmit-poll').removeClass('hide');

            },
            error: function() {
                alert("Please select a choice");
            }
        });
    });
    $('#poll-list').on('click', '.resubmit-poll', function(e) {
        e.preventDefault();

        var $poll = $(this).closest('.poll-wrapper');
        var $poll_content = $poll.find('.content > input').val();
        var $choice = $poll.find("input[name=" + $poll.attr('id') + "]:checked");
        var voteID;
        var vote = {
            voter: $poll.parent().attr('data-user'),
            choice: $choice.attr('data-choice'),
            poll: $poll.attr('id'),
        }
        //gets the id of vote previously submitted
        $.ajax({
            type: 'GET',
            url: '/votes/' + $poll.attr('id'),
            success: function(data) {
                voteID = data;
                $.ajax({
                    //puts new choice of vote
                    type: 'PUT',
                    url: '/api/votes/' + voteID,
                    data: vote,
                    success: function() {
                        alert("vote successfully resubmitted!");

                    },
                    error: function() {
                        alert("Please select a choice");
                    }
                });
            },
            error: function() {
                alert("no vote found");
            }
        });

    });
    //These functions are for Everyone
    //calculates and sets widths of progress bars
    function setWidths(poll) {

        totalVotes = poll.attr('data-votes');
        $bars = poll.find('.progress-bars').children('.progress').children();

        $bars.each(function() {
            votes = $(this).attr('data-votes')
            $(this).css("width", votes/totalVotes*100 + "%");
        });

    }
    function setProgressBars() {
        $closed_polls = $('#poll-list').children('.closed');
        $closed_polls.each(function() {
            setWidths($(this));
        });
    }
    setProgressBars();
    //A test to see how fast changing the text of header is
    // function changeHead() {
    //     $('#poll-list').find('h1').html('How fast does this change');
    // }
    // changeHead();



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
    //These functions are for ADMINS only
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

    $('#poll-list').on('click', '.edit-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        $poll.addClass("edit");
        //$poll.find('.choice').children('.choice').attr('disabled', true);
        //$poll.find('.choice').children('label').attr('contenteditable', true);
    });

    $('#poll-list').on('click', '.cancel-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        $poll.removeClass("edit");
        //$poll.find('.choice').children('.choice').attr('disabled', false);
        //$poll.find('.choice').children('label').attr('contenteditable', false);
    });

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
    $('#poll-list').on('click', '.close-poll', function(e) {
        e.preventDefault();
        var currentDate = new Date();
        var $poll = $(this).closest('.poll-wrapper');
        var poll = {
            author: $poll.find('.author').text(),
            category: $poll.find('.category').text(),
            date_created: $poll.find('.date_created').text(),
            date_closed: currentDate.toJSON(),
            content: $poll.find('.content > input').val(),
            rank: $poll.find('.rank').text(),
            is_open: false,
        };

        $.ajax({
            type: 'PUT',
            url: '/api/polls/' + $poll.attr('id'),
            data: poll,
            success: function(newpoll) {
                alert('poll successfully closed');
            },
            error: function() {
                alert('Error updating poll.');
            }
        });
    });
        $('#poll-list').on('click', '.reopen-poll', function(e) {
            e.preventDefault();

            var $poll = $(this).closest('.poll-wrapper');
            var poll = {
                author: $poll.find('.author').text(),
                category: $poll.find('.category').text(),
                date_created: $poll.find('.date_created').text(),
                date_closed: null,
                content: $poll.find('.content > a > h2').text(),
                rank: $poll.find('.rank').text(),
                is_open: true,
            };

            $.ajax({
                type: 'PUT',
                url: '/api/polls/' + $poll.attr('id'),
                data: poll,
                success: function(newpoll) {
                    alert('poll successfully reopened');
                },
                error: function() {
                    alert('Error reopening poll.');
                }
            });

    });
});
