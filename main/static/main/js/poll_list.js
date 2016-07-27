
$(document).ready(function() {
    var $pollList = $('#poll-list');
    //checks if poll is closed
    function checkClosed($poll) {
        $.ajax({
            type: 'GET',
            url: '/api/polls/' + $poll.attr('id').substring(5),
            success: function(poll) {
                if (poll.is_open) {
                    return true;
                } else {
                    return false;
                }
            }
        });
    }
    //submits vote, adjusts progress-bars, shows correct buttons and progress bars, hides choices,
    $pollList.on('click', '.submit-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        if (checkClosed($poll) == false) {
            ($poll).find('.alert-danger').removeClass('hide').delay(5000).fadeOut();
        } else {
            var $submit_button = $(this);
            var $choice = $poll.find("input[name=" + $poll.attr('id') + "]:checked");
            try {
                var vote = {
                voter: $poll.parent().parent().attr('data-user'),
                choice: $choice.attr('id').substring(7),
                poll: $poll.attr('id').substring(5),
                }
                $.ajax({
                    type: 'POST',
                    url: '/api/votes/',
                    data: vote,
                    success: function() {
                        $submit_button.addClass('hidden');
                        $submit_button.next().removeClass('hidden');
                        if ($poll.hasClass('submitted')) {
                            $prev_choice = $poll.find('.picked');
                            $prev_choice.removeClass('picked');
                            subtractVote($prev_choice);
                        } else {
                            //Increase the total votes of poll by 1 and marks poll and choice
                            $total_vote_count = parseInt($poll.attr('data-votes'),10) + 1;
                            $poll.attr('data-votes', $total_vote_count);
                            $poll.addClass('submitted');
                            $choice.addClass('picked');
                        }
                        //Sets progress bars, shows progress bars, hides choices

                        $.when(addVote($choice)).then(setWidths($poll));
                        $poll.find('.progress-bars').removeClass('hidden');
                        $poll.find('.poll-choices').addClass('hidden');
                    },
                });
            } catch(err) {
                $('#alert-danger').removeClass('hidden').delay(4000).fadeOut(function() {
                    $(this).addClass('hidden');
                    $(this).show();
                });
            }
        }
    });
    $pollList.on('click', 'resubmit-poll', function(e) {
        e.preventDefault();
    })
    //Shows correct choices and buttons, hides progress bars
    $pollList.on('click', '.change-vote', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        var $submit_button = $(this).prev();
        if (checkClosed($poll) == false) {
            ($poll).find('.alert-danger').removeClass('hide').delay(5000).fadeOut();
        } else {
            prefillVote($poll);
            $submit_button.removeClass('hidden');
            $submit_button.next().addClass('hidden');
            $poll.find('.progress-bars').addClass('hidden');
            $poll.find('.poll-choices').removeClass('hidden');
        }
    });
    /**************************** Helper Functions ****************************/
    //calculates and sets widths of progress bars
    function setWidths(poll) {
        totalVotes = poll.attr('data-votes');
        $bars = poll.find('.progress-bars').children('.progress').children();

        $bars.each(function() {
            votes = $(this).attr('data-votes')
            $(this).css("width", votes/totalVotes*100 + "%");
        });
    }
    //sets widths of all closed and voted progress bars
    function setProgressBars() {
        $closed_polls = $('#polls-closed').children();
        $voted_polls = $('#polls-voted').children();
        $closed_polls.each(function() {
            setWidths($(this));
        });
        $voted_polls.each(function() {
            setWidths($(this));
        });
    }
    setProgressBars();
    //Adjusts progress-bar and label of new choice
    function addVote($new_choice) {
        $progress_bar = $('#progress-' + $new_choice.attr('id').substring(7));
        $vote_count = parseInt($progress_bar.attr('data-votes'), 10) + 1;
        $label = $progress_bar.parent().prev();

        $progress_bar.attr('data-votes', $vote_count);
        $label.html($new_choice.attr('value') + ' | ' + $vote_count);
    }
    //Adjusts progress-bar and label of previous choice
    function subtractVote($prev_choice) {
        $progress_bar = $('#progress-' + $prev_choice.attr('id').substring(7));
        $vote_count = parseInt($progress_bar.attr('data-votes'), 10) - 1;
        $label = $progress_bar.parent().prev();

        $progress_bar.attr('data-votes', $vote_count);
        $label.html($prev_choice.attr('value') + ' | ' + $vote_count);
    }
    //Finds choice previously chosen by user. Needed to adjust progress bars in voted poll.
    function prefillVote($poll) {
        $.ajax({
            type: 'GET',
            url: '/get_vote/' + ($poll).attr('id').substring(5),
            success: function(votepk) {
                $.ajax({
                    type: 'GET',
                    url: '/api/votes/' + votepk,
                    success: function(vote) {
                        $choice=$poll.find('input[id = choice-' + vote.choice + ']');
                        $choice.attr('checked', true);
                        //to handle when user changes vote of voted poll because there are no choices with class picked
                        if (!$choice.hasClass('picked')){
                            $choice.addClass('picked');
                        }
                    }
                });
            }
        });
    }
});
