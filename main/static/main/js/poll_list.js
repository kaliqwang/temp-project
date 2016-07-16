
$(document).ready(function() {
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
        $voted_polls = $('#poll-list').children('.voted');
        $closed_polls.each(function() {
            setWidths($(this));
        });
        $voted_polls.each(function() {
            setWidths($(this));
        });
    }
    setProgressBars();
    // These functions are for Users only
    // Puts the poll on resubmit-mode, prefills radio button with user's previous vote on voted polls, and add class to user's previous vote
    function prefillVote($poll) {
        $poll.addClass('resubmit');
        $.ajax({
            type: 'GET',
            url: '/votes/' + ($poll).attr('id'),
            async: false,
            success: function(votepk) {
                $.ajax({
                    type: 'GET',
                    url: '/api/votes/' + votepk,
                    async:false,
                    success: function(vote) {
                        $choice=$poll.find('input[data-choice=' + vote.choice + ']');
                        $choice.attr('checked', true);
                        $choice.addClass('picked');
                    }
                });
            }
        });
    }
    //checks if poll is closed
    function checkClosed($poll) {
        $.ajax({
            type: 'GET',
            url: '/api/polls/' + $poll.attr('id'),
            success: function(poll) {
                if (poll.is_open) {
                    return true;
                } else {
                    return false;
                }
            }
        });
    }
    $('#poll-list').on('click', '.resubmit-mode', function() {
        prefillVote($(this).closest('.poll-wrapper'));
    });
    $('#poll-list').on('click', '.submit-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        if (checkClosed($poll) == false) {
            $('#error-alert').removeClass('hide');
        } else {
            var $submit_button = $(this);
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
                    $submit_button.hide();
                    $submit_button.next().next().removeClass('hide');

                    $total_vote_count = parseInt($poll.attr('data-votes'),10) + 1;
                    $poll.attr('data-votes', $total_vote_count);
                    $poll.removeClass('resubmit');
                    $.when(addVote($choice)).then(setWidths($poll));
                },
                error: function() {
                    $('#error-alert').removeClass('hide');
                }
            });
        }
    });
    //Adjusts progress-bar and label of new choice
    function addVote($new_choice) {
        $progress_bar = $new_choice.parent().next().find('.progress-bar');
        $vote_count = parseInt($progress_bar.attr('data-votes'), 10) + 1;
        $label = $progress_bar.parent().prev();

        $progress_bar.attr('data-votes', $vote_count);
        $label.html($new_choice.attr('value') + ' | ' + $vote_count);
    }
    //Adjusts progress-bar and label of new choice and previous choice
    function changeVote($new_choice, $prev_choice) {
        addVote($new_choice);
        $progress_bar = $prev_choice.parent().next().find('.progress-bar');
        $vote_count = parseInt($progress_bar.attr('data-votes'), 10) - 1;
        $label = $progress_bar.parent().prev();

        $progress_bar.attr('data-votes', $vote_count);
        $label.html($prev_choice.attr('value') + ' | ' + $vote_count);
    }
    $('#poll-list').on('click', '.resubmit-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        if (checkClosed($poll) == false) {
            console.log("this is happening");
            $('#error-alert').removeClass('hide');
        } else {
            var $choice = $poll.find("input[name=" + $poll.attr('id') + "]:checked");
            var $prev_choice = $choice.parents('.choices-container').find('.picked');
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
                        //puts new choice of vote and adjusts progress bars
                        type: 'PUT',
                        url: '/api/votes/' + voteID,
                        data: vote,
                        success: function() {
                            $prev_choice.removeClass('picked');
                            $poll.removeClass('resubmit');
                            $choice.addClass('picked');
                            $.when(changeVote($choice, $prev_choice)).then(setWidths($poll));
                        },
                        error: function() {
                            $('#error-alert').removeClass('hide');
                        }
                    });
                },
                error: function() {
                    $('#error-alert').removeClass('hide');
                }
            });
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
    });

    $('#poll-list').on('click', '.cancel-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        $poll.removeClass("edit");
    });
    //removes choice if clicked
    $('#poll-list').on('click', '.input-group-btn', function(e) {
        e.preventDefault();
        $input_choice = $(this).prev();
        if (!$input_choice.attr('data-choice')) {
            $input_choice.closest('.choice-container').remove();
        } else {
            $.ajax({
                type: 'DELETE',
                url: '/api/choices/' + $input_choice.attr('data-choice'),
                success: function() {
                    $input_choice.closest('.choice-container').remove();
                },
            });
        }
    });
    // adds choice if clicked
    $('.add-choice').click(function(e) {
        e.preventDefault();
        var ChoiceField = $('#choicetemplate').html();
        $(this).closest('.poll-wrapper').find('.choices-container').append(ChoiceField);

    })
    $('#poll-list').on('click', '.save-poll', function(e) {
        e.preventDefault();

        var $poll = $(this).closest('.poll-wrapper');
        var $choices = $poll.find('.choices-container').find('.input-group').children('input');

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
            success: function(newPoll) {
                $poll.find('.content.noedit > a > h2').text(newPoll.content);

                $choices.each(function() {
                    var $choice = $(this).parents('.choice').find('label');
                    var choice = {
                        poll: $poll.attr('id'),
                        content: $(this).val(),
                    }
                    $.ajax({
                        type: 'PUT',
                        url: '/api/choices/' + $(this).attr('data-choice'),
                        data: choice,
                        success: function(newChoice) {
                            $choice.html(newChoice.content);
                            $poll.removeClass('edit');
                        },
                        error: function() {
                            $('#error-alert').removeClass('hide');
                        },
                    });
                });
                $poll.removeClass('edit');
            },
            error: function() {
                $('#error-alert').removeClass('hide');
            }
        });
    });
    function setStatus($poll, status) {
        var currentDate = new Date();
        var poll = {
            author: $poll.find('.author').text(),
            category: $poll.find('.category').text(),
            date_created: $poll.find('.date_created').text(),
            date_closed: currentDate.toJSON(),
            content: $poll.find('.content > a > h2').text(),
            rank: $poll.find('.rank').text(),
            is_open: status,
        };
        $.ajax({
            type: 'PUT',
            url: '/api/polls/' + $poll.attr('id'),
            data: poll,
            success: function(newPoll) {
                $('#sucess-alert').removeClass('hide');
            },
            error: function() {
                $('#error-alert').removeClass('hide');
            }
        });
    }
    $('#poll-list').on('click', '.close-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        setStatus($poll, false);


    });
        $('#poll-list').on('click', '.reopen-poll', function(e) {
            e.preventDefault();
            var $poll = $(this).closest('.poll-wrapper');
            setStatus($poll, true);
    });
});
